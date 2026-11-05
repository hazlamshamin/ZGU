from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
import unittest
import urllib.request
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPECTED = HERE / "expected"
SOURCE_SHA = "bbf601f30389e550ed4f69e2c2d7522ba748c116"
RAW_ROOT = f"https://raw.githubusercontent.com/mohdhairimohdzaman/GayaUKM/{SOURCE_SHA}"


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


class GayaUkmLatexCrossCheck(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        for command in ("latexmk", "pdftotext"):
            if shutil.which(command) is None:
                raise RuntimeError(f"{command} is required for the LaTeX cross-check")

    def run_case(self, language: str, bst_name: str) -> None:
        with tempfile.TemporaryDirectory(prefix="gaya-ukm-latex-") as temp_name:
            work = Path(temp_name)
            for filename in ("references.bib", f"{language}.tex"):
                shutil.copy2(HERE / filename, work / filename)

            bst_url = f"{RAW_ROOT}/{bst_name}"
            with urllib.request.urlopen(bst_url, timeout=30) as response:
                (work / bst_name).write_bytes(response.read())

            subprocess.run(
                [
                    "latexmk",
                    "-pdf",
                    "-interaction=nonstopmode",
                    f"{language}.tex",
                ],
                cwd=work,
                check=True,
                capture_output=True,
                text=True,
            )

            actual_bbl = normalize((work / f"{language}.bbl").read_text(encoding="utf-8"))
            expected_bbl = normalize(
                (EXPECTED / f"{language}.bbl").read_text(encoding="utf-8")
            )
            self.assertEqual(actual_bbl, expected_bbl)

            pdf_text = subprocess.run(
                ["pdftotext", "-layout", f"{language}.pdf", "-"],
                cwd=work,
                check=True,
                capture_output=True,
                text=True,
            ).stdout
            normalized_pdf = normalize(pdf_text)
            self.assertIn("(Brown 2008)", normalized_pdf)
            self.assertIn("(Hamzah, Mohamed & Hussain 2004)", normalized_pdf)
            self.assertIn("(Rahmat et al. 2002)", normalized_pdf)

    def test_english_bst_cross_check(self) -> None:
        self.run_case("english", "GayaUKM.bst")

    def test_malay_bst_cross_check(self) -> None:
        self.run_case("malay", "GayaUKM-ms.bst")


if __name__ == "__main__":
    unittest.main()
