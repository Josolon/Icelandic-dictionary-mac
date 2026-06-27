# Icelandic-dictionary-mac

Create Apple Dictionary XML for a native macOS Icelandic dictionary using open-source
monolingual definitions plus morphology-aware lookup indexes.

## Supported open data sources

- **Definitions:** Icelandic Wiktionary extracted with
  [wiktextract](https://github.com/tatuylonen/wiktextract), or any CSV file with
  `lemma/headword`, `part_of_speech`, and `definition` columns.
- **Morphology:** BÍN (Beygingarlýsing íslensks nútímamáls) CSV exports. The builder
  understands both generic `lemma/form/tag` headers and BÍN-style `ord/bmynd/mark`
  headers.

This repository does **not** redistribute source datasets. You supply the files
locally, which keeps licensing and attribution under your control.

## Usage

```bash
python3 build_dictionary.py \
  --definitions /path/to/iswiktionary.jsonl \
  --definitions-format wiktextract \
  --morphology /path/to/bin.csv \
  --output /path/to/Icelandic.xml
```

The generated XML uses Apple Dictionary indexes for every inflected form found in the
morphology file, so looking up a declined or conjugated form can resolve to the lemma
entry in Dictionary.app.

## Tests

```bash
python3 -m unittest discover -v
```
