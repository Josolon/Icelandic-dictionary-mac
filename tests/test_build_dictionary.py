import tempfile
import textwrap
import unittest
from pathlib import Path

import build_dictionary


class BuildDictionaryTests(unittest.TestCase):
    def write_file(self, directory: Path, name: str, content: str) -> Path:
        path = directory / name
        path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")
        return path

    def test_builds_xml_with_morphology_indexes_from_wiktextract(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            definitions_path = self.write_file(
                root,
                "definitions.jsonl",
                """
                {"word":"hundur","lang":"Icelandic","lang_code":"is","pos":"noun","senses":[{"glosses":["hundategund af ætt úlfdýra"]}]}
                {"word":"dog","lang":"English","lang_code":"en","pos":"noun","senses":[{"glosses":["not included"]}]}
                """,
            )
            morphology_path = self.write_file(
                root,
                "morphology.csv",
                """
                lemma;form;tag
                hundur;hundur;NFET
                hundur;hunds;EFET
                hundur;hundi;ÞGFET
                """,
            )
            output_path = root / "Icelandic.xml"

            exit_code = build_dictionary.main(
                [
                    "--definitions",
                    str(definitions_path),
                    "--morphology",
                    str(morphology_path),
                    "--output",
                    str(output_path),
                    "--title",
                    "Open-source Icelandic dictionary",
                ]
            )

            self.assertEqual(exit_code, 0)
            xml_output = output_path.read_text(encoding="utf-8")
            self.assertIn('<d:index d:value="hunds"/>', xml_output)
            self.assertIn('<d:index d:value="hundi"/>', xml_output)
            self.assertIn("<h1>hundur</h1>", xml_output)
            self.assertIn("<li>hundategund af ætt úlfdýra</li>", xml_output)
            self.assertIn("<h2>Beyging</h2>", xml_output)
            self.assertNotIn("not included", xml_output)

    def test_reads_generic_csv_definition_and_bin_style_morphology_columns(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            definitions_path = self.write_file(
                root,
                "definitions.csv",
                """
                headword,part_of_speech,definition
                kona,noun,kvenmaður
                """,
            )
            morphology_path = self.write_file(
                root,
                "bin.csv",
                """
                ord;bmynd;mark
                kona;kona;NFET
                kona;konu;ÞFET
                """,
            )
            output_path = root / "Icelandic.xml"

            exit_code = build_dictionary.main(
                [
                    "--definitions",
                    str(definitions_path),
                    "--definitions-format",
                    "csv",
                    "--morphology",
                    str(morphology_path),
                    "--output",
                    str(output_path),
                ]
            )

            self.assertEqual(exit_code, 0)
            xml_output = output_path.read_text(encoding="utf-8")
            self.assertIn('<d:index d:value="konu"/>', xml_output)
            self.assertIn("<h2>noun</h2>", xml_output)
            self.assertIn("<li>kvenmaður</li>", xml_output)


if __name__ == "__main__":
    unittest.main()
