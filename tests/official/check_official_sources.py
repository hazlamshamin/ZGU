from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import tempfile
import unicodedata
import unittest
import urllib.request
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCES = json.loads((HERE / "sources.json").read_text(encoding="utf-8"))


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).replace("\u00ad", "")
    text = text.replace("’", "'").replace("‘", "'")
    text = text.replace("“", '"').replace("”", '"')
    text = text.replace("–", "-").replace("—", "-")
    text = re.sub(r"-\s*\n\s*", "-", text)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s*-\s*", "-", text)
    text = re.sub(r"\s+([.,:;])", r"\1", text)
    text = re.sub(r"\(\s+", "(", text)
    text = re.sub(r"\s+\)", ")", text)
    return text.strip()


def download(url: str) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Gaya-UKM-CSL-sourcetest/1.0"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


class OfficialGuideSourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if shutil.which("pdftotext") is None:
            raise RuntimeError("pdftotext is required for the official source check")

    def assert_excerpts_exist(self, language: str) -> None:
        source = SOURCES[language]
        payload = download(source["url"])
        digest = hashlib.sha256(payload).hexdigest()
        self.assertEqual(digest, source["sha256"])

        expected_path = (HERE / source["expected"]).resolve()
        expected_lines = [
            line
            for line in expected_path.read_text(encoding="utf-8").splitlines()
            if line
        ]

        with tempfile.TemporaryDirectory(prefix=f"gaya-ukm-{language}-") as temp_name:
            pdf_path = Path(temp_name) / f"{language}.pdf"
            pdf_path.write_bytes(payload)
            extracted = subprocess.run(
                ["pdftotext", "-layout", str(pdf_path), "-"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout

        normalized_pdf = normalize(extracted)
        for excerpt in expected_lines:
            with self.subTest(language=language, excerpt=excerpt):
                needle = normalize(excerpt).rstrip(".")
                if needle not in normalized_pdf:
                    self.fail(
                        f"{language} official PDF does not contain reference excerpt: {excerpt}"
                    )

    def test_malay_reference_excerpts_come_from_official_pdf(self) -> None:
        self.assert_excerpts_exist("malay")

    def test_english_reference_excerpts_come_from_official_pdf(self) -> None:
        self.assert_excerpts_exist("english")


if __name__ == "__main__":
    unittest.main()
