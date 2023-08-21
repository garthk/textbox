# TextBox

Remember text for you, wholesale.

TextBox is a suite of tools to help you maintain a local archive of text that's important to you in case the hosted versions disappear unexpectedly.

Inhale:

- The links you've saved to various bookmarking platforms
- The pages you've saved to read later
- Your Twitter archive
- Broadly, any text with a URL

## Scope

I intend to make it easy to:

- Inhale content from any archive provided to satisfy your GDPR right to data portability.
- Inhale content live from a service's API.
- Search the content you've inhaled.

I don't intend to make it easy to:

- Share the content you've inhaled, because privacy and consent.

## Design Sketch

This'll change as the project teaches me what it's about, but I'm thinking:

- [PEP 420][pep-420] namespace packages (see also [PyPa's take][pypa-420]) to help people plug in data sources
- [SQLite][sqlite] for the storage
- [Datasette][datasette] as our database UI while we're getting started
- [SQLite Utils][sqlite-utils] for schema management
- [Shot-scraper] to capture images of web pages
- [Readability] to reduce cutter in captured HTML

## Project Scaffold

Specifically for Python:

- [PyPa][pypa] documents how to package your project
- [nox] automates your testing
- [mypy] checks your types

For any language:

- [EditorConfig][editorconfig] helps you avoid newline blunders
- [direnv] sets up your env and venv when you cd
- [brew bundle][brew-bundle] installs your stack
- [GNU Make][make] and [.PHONY targets][PHONY]

[PHONY]: https://www.gnu.org/software/make/manual/html_node/Phony-Targets.html
[brew-bundle]: https://docs.brew.sh/Manpage#bundle-subcommand
[datasette]: https://datasette.io/
[direnv]: https://direnv.net/
[editorconfig]: https://editorconfig.org/
[make]: https://www.gnu.org/software/make/
[mypy]: https://www.mypy-lang.org
[nox]: https://nox.thea.codes/en/stable/
[pep-420]: https://peps.python.org/pep-0440/
[pypa-420]: https://packaging.python.org/en/latest/guides/packaging-namespace-packages/
[pypa]: https://packaging.python.org/en/latest/
[readability]: https://github.com/mozilla/readability
[shot-scraper]: https://datasette.io/tools/shot-scraper
[sqlite-utils]: https://github.com/simonw/sqlite-utils
[sqlite]: https://www.sqlite.org/index.html
