#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import html
import json
from collections import OrderedDict, defaultdict
from pathlib import Path
from typing import Iterable


DEFINITION_LEMMA_ALIASES = {"lemma", "headword", "word", "term", "title"}
DEFINITION_TEXT_ALIASES = {"definition", "gloss", "meaning"}
DEFINITION_POS_ALIASES = {"pos", "part_of_speech", "word_class"}

MORPHOLOGY_LEMMA_ALIASES = {
    "lemma",
    "headword",
    "word",
    "term",
    "ord",
    "uppflettimynd",
    "stofn",
}
MORPHOLOGY_FORM_ALIASES = {"form", "surface", "wordform", "bmynd"}
MORPHOLOGY_TAG_ALIASES = {"tag", "mark", "features", "morphology", "beyging", "inflection"}


def normalize_text(value: str | None) -> str:
    return " ".join((value or "").split())


def detect_dialect(sample: str) -> csv.Dialect:
    try:
        return csv.Sniffer().sniff(sample, delimiters=",;\t")
    except csv.Error:
        return csv.excel


def detect_column(fieldnames: Iterable[str] | None, aliases: set[str], label: str) -> str:
    if not fieldnames:
        raise ValueError(f"Missing header row while looking for the {label} column")

    lookup = {name.strip().casefold(): name for name in fieldnames if name}
    for alias in aliases:
        column = lookup.get(alias.casefold())
        if column:
            return column

    available = ", ".join(fieldnames)
    raise ValueError(f"Could not find a {label} column. Available columns: {available}")


def read_csv_rows(path: Path) -> tuple[csv.DictReader, list[dict[str, str]]]:
    sample = path.read_text(encoding="utf-8-sig")[:4096]
    dialect = detect_dialect(sample)
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, dialect=dialect)
        return reader, list(reader)


def load_wiktextract_definitions(path: Path) -> dict[str, OrderedDict[str, list[str]]]:
    definitions: dict[str, OrderedDict[str, list[str]]] = defaultdict(OrderedDict)

    with path.open(encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line:
                continue

            payload = json.loads(line)
            if payload.get("lang_code") != "is" and payload.get("lang") != "Icelandic":
                continue

            lemma = normalize_text(payload.get("word"))
            if not lemma:
                continue

            pos = normalize_text(payload.get("pos")) or "unknown"
            glosses: list[str] = []
            for sense in payload.get("senses", []):
                for gloss in sense.get("glosses", []):
                    normalized = normalize_text(gloss)
                    if normalized:
                        glosses.append(normalized)

            if not glosses:
                continue

            bucket = definitions[lemma].setdefault(pos, [])
            for gloss in glosses:
                if gloss not in bucket:
                    bucket.append(gloss)

    return definitions


def load_csv_definitions(path: Path) -> dict[str, OrderedDict[str, list[str]]]:
    reader, rows = read_csv_rows(path)
    lemma_column = detect_column(reader.fieldnames, DEFINITION_LEMMA_ALIASES, "lemma")
    definition_column = detect_column(reader.fieldnames, DEFINITION_TEXT_ALIASES, "definition")
    pos_column = detect_column(reader.fieldnames, DEFINITION_POS_ALIASES, "part of speech")

    definitions: dict[str, OrderedDict[str, list[str]]] = defaultdict(OrderedDict)
    for row in rows:
        lemma = normalize_text(row.get(lemma_column))
        definition = normalize_text(row.get(definition_column))
        pos = normalize_text(row.get(pos_column)) or "unknown"
        if not lemma or not definition:
            continue

        bucket = definitions[lemma].setdefault(pos, [])
        if definition not in bucket:
            bucket.append(definition)

    return definitions


def load_definitions(path: Path, fmt: str) -> dict[str, OrderedDict[str, list[str]]]:
    if fmt == "auto":
        fmt = "wiktextract" if path.suffix.lower() in {".jsonl", ".json"} else "csv"

    if fmt == "wiktextract":
        return load_wiktextract_definitions(path)
    if fmt == "csv":
        return load_csv_definitions(path)

    raise ValueError(f"Unsupported definitions format: {fmt}")


def load_morphology(path: Path) -> dict[str, list[tuple[str, str]]]:
    reader, rows = read_csv_rows(path)
    lemma_column = detect_column(reader.fieldnames, MORPHOLOGY_LEMMA_ALIASES, "morphology lemma")
    form_column = detect_column(reader.fieldnames, MORPHOLOGY_FORM_ALIASES, "morphology form")
    tag_column = detect_column(reader.fieldnames, MORPHOLOGY_TAG_ALIASES, "morphology tag")

    morphology: dict[str, list[tuple[str, str]]] = defaultdict(list)
    seen: dict[str, set[tuple[str, str]]] = defaultdict(set)

    for row in rows:
        lemma = normalize_text(row.get(lemma_column))
        form = normalize_text(row.get(form_column))
        tag = normalize_text(row.get(tag_column))
        if not lemma or not form:
            continue

        item = (form, tag)
        if item in seen[lemma]:
            continue
        seen[lemma].add(item)
        morphology[lemma].append(item)

    return morphology


def xml_escape(value: str) -> str:
    return html.escape(value, quote=True)


def slugify(value: str) -> str:
    cleaned = [character.lower() if character.isalnum() else "-" for character in value]
    slug = "".join(cleaned).strip("-")
    return slug or "entry"


def render_dictionary_xml(
    definitions: dict[str, OrderedDict[str, list[str]]],
    morphology: dict[str, list[tuple[str, str]]],
    title: str,
) -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<d:dictionary xmlns="http://www.w3.org/1999/xhtml" xmlns:d="http://www.apple.com/DTDs/DictionaryService-1.0.rng">',
    ]

    lower_morphology = {lemma.casefold(): forms for lemma, forms in morphology.items()}

    for index, lemma in enumerate(sorted(definitions, key=str.casefold), start=1):
        parts = definitions[lemma]
        forms = morphology.get(lemma, lower_morphology.get(lemma.casefold(), []))

        index_terms: list[str] = []
        for value in [lemma, *[form for form, _ in forms]]:
            normalized = normalize_text(value)
            if normalized and normalized not in index_terms:
                index_terms.append(normalized)

        entry_id = f"{slugify(lemma)}-{index}"
        lines.append(f'  <d:entry id="{xml_escape(entry_id)}" d:title="{xml_escape(lemma)}">')
        for term in index_terms:
            lines.append(f'    <d:index d:value="{xml_escape(term)}"/>')
        lines.append(f"    <h1>{xml_escape(lemma)}</h1>")
        lines.append(f"    <p>{xml_escape(title)}</p>")

        for pos, glosses in parts.items():
            lines.append('    <section class="sense-group">')
            lines.append(f"      <h2>{xml_escape(pos)}</h2>")
            lines.append("      <ol>")
            for gloss in glosses:
                lines.append(f"        <li>{xml_escape(gloss)}</li>")
            lines.append("      </ol>")
            lines.append("    </section>")

        if forms:
            lines.append('    <section class="morphology">')
            lines.append("      <h2>Beyging</h2>")
            lines.append("      <ul>")
            for form, tag in forms:
                if tag:
                    lines.append(
                        "        <li>"
                        f"{xml_escape(form)}"
                        f' <span class="tag">{xml_escape(tag)}</span>'
                        "</li>"
                    )
                else:
                    lines.append(f"        <li>{xml_escape(form)}</li>")
            lines.append("      </ul>")
            lines.append("    </section>")

        lines.append("  </d:entry>")

    lines.append("</d:dictionary>")
    lines.append("")
    return "\n".join(lines)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build Apple Dictionary XML from open Icelandic definitions and morphology data."
    )
    parser.add_argument("--definitions", required=True, type=Path, help="Path to definitions data")
    parser.add_argument(
        "--definitions-format",
        choices=("auto", "wiktextract", "csv"),
        default="auto",
        help="Format of the definitions file",
    )
    parser.add_argument("--morphology", required=True, type=Path, help="Path to morphology CSV data")
    parser.add_argument("--output", required=True, type=Path, help="Path to write the Apple Dictionary XML")
    parser.add_argument(
        "--title",
        default="Íslensk orðabók built from open-source data",
        help="Dictionary subtitle shown inside each entry",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    definitions = load_definitions(args.definitions, args.definitions_format)
    morphology = load_morphology(args.morphology)
    xml_output = render_dictionary_xml(definitions, morphology, args.title)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(xml_output, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
