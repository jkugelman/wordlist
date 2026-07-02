# wordlist

John Kugelman's crossword wordlist, alongside mirrored copies of two third-party lists. All three are served over `raw.githubusercontent.com`, which sends an `Access-Control-Allow-Origin` header — so browser-based tools (for example [Grawlix](https://grawlix.wtf)) can fetch them directly, which the authors' own hosts don't allow.

## Contents & licensing

| File | Source | License |
| --- | --- | --- |
| `jkugelman-wordlist.txt` | John Kugelman (this repo) | MIT — see [`LICENSE`](LICENSE) |
| `spreadthewordlist.txt` | [Spread the Word(list)](https://www.spreadthewordlist.com) — Brooke Husic & Enrique Henestroza Anguiano | CC BY-NC-SA 4.0 |
| `peter-broda-wordlist.txt` | [Peter Broda's Wordlist](http://www.peterbroda.me/crosswords/wordlist/) — Peter Broda | No stated license — mirrored unmodified with attribution |

`LICENSE` (MIT) covers only `jkugelman-wordlist.txt` and this repo's own tooling. The other two lists are third-party works redistributed unmodified under their own terms — see [`THIRD-PARTY-NOTICES`](THIRD-PARTY-NOTICES).

## Automated updates

`spreadthewordlist.txt` is refreshed nightly by [`.github/workflows/update-stwl.yml`](.github/workflows/update-stwl.yml): it downloads the current "lowercase + compiler" build from spreadthewordlist.com and, when it differs, commits it as the GitHub Actions bot (`github-actions[bot]`). The other lists are updated manually.
