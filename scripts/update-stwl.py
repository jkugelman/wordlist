#!/usr/bin/env python3
"""Fetch the current "lowercase + compiler" build of Spread the Word(list) and
write it to the given path (default: spreadthewordlist.txt).

The homepage links each build to a Google Drive file, and the Drive file id can
change if the authors re-upload, so the link is scraped by its anchor text
rather than hardcoded. Any failure — page unscrapable, download that doesn't
look like a wordlist — exits non-zero WITHOUT writing, so a bad run fails
loudly (and the workflow emails) instead of committing garbage.

Google Drive sends no usable CORS header, so browsers can't fetch it directly;
that's why the file is mirrored here. This runs server-side, where CORS does
not apply.
"""

import re
import sys
import urllib.request

HOMEPAGE = "https://www.spreadthewordlist.com/"
LINK_LABEL = "lowercase + compiler"
UA = "Mozilla/5.0 (X11; Linux x86_64) wordlist-update-bot"


def die(msg):
    sys.exit(f"update-stwl: {msg}")


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read()


def find_download_url(html):
    # href precedes the visible label inside the <a>; other attributes (class,
    # data-*, target) sit between, and the tag spans several lines — hence
    # DOTALL and the lenient [^>]* run before the closing '>'.
    m = re.search(
        r'<a\b[^>]*?href="(https://drive\.google\.com/uc\?export=download&id=[^"]+)"'
        r"[^>]*>\s*" + re.escape(LINK_LABEL) + r"\s*</a>",
        html,
        re.IGNORECASE | re.DOTALL,
    )
    if not m:
        die(f'could not find the "{LINK_LABEL}" download link on {HOMEPAGE}')
    return m.group(1)


def validate(text):
    if text.lstrip()[:15].lower().startswith(("<!doctype", "<html")):
        die("download looks like an HTML page (Drive interstitial?), not a wordlist")
    if len(text) < 1_000_000:
        die(f"download is only {len(text)} bytes; expected a multi-MB wordlist")
    sample = [ln for ln in text.splitlines() if ln][:500]
    good = sum(1 for ln in sample if re.match(r".+;\d+(;.*)?$", ln))
    if not sample or good / len(sample) < 0.9:
        die("download does not look like ENTRY;SCORE wordlist data")


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "spreadthewordlist.txt"

    html = fetch(HOMEPAGE).decode("utf-8", "replace")
    url = find_download_url(html)

    # Strict decode: corrupt bytes should fail loudly, not be silently mangled.
    try:
        text = fetch(url).decode("utf-8")
    except UnicodeDecodeError as e:
        die(f"downloaded file is not valid UTF-8: {e}")
    text = text.replace("\r\n", "\n")
    validate(text)

    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print(f"update-stwl: wrote {len(text)} bytes, {text.count(chr(10))} lines to {out}")


if __name__ == "__main__":
    main()
