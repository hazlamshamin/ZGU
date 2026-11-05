from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
STYLES = PROJECT_ROOT / "styles"
FIXTURES = PROJECT_ROOT / "tests" / "fixtures"
EXPECTED = PROJECT_ROOT / "tests" / "expected"
CSL_NAMESPACE = "http://purl.org/net/xbiblio/csl"
NS = {"csl": CSL_NAMESPACE}
STYLE_FILES = ("gaya-ukm-malay.csl", "gaya-ukm-english.csl")


def run_pandoc(
    source_path: Path,
    bibliography_path: Path,
    style_file: str,
    *,
    output_format: str | None = None,
    output_path: Path | None = None,
) -> str:
    pandoc = shutil.which("pandoc")
    if pandoc is None:
        raise RuntimeError("pandoc with citeproc support is required for CSL conformance tests")

    command = [
        pandoc,
        str(source_path),
        "--from=markdown-smart",
        "--citeproc",
        "--bibliography",
        str(bibliography_path),
        "--csl",
        str(STYLES / style_file),
    ]
    if output_path is not None:
        command.extend(["--output", str(output_path)])
    else:
        if output_format is None:
            raise ValueError("output_format is required when output_path is not supplied")
        command.extend(["--to", output_format, "--wrap=none"])

    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return result.stdout.replace("\r\n", "\n").strip()


def render(style_file: str, fixture_stem: str, output_format: str) -> str:
    return run_pandoc(
        FIXTURES / f"{fixture_stem}.md",
        FIXTURES / f"{fixture_stem}.json",
        style_file,
        output_format=output_format,
    )


def render_records(
    style_file: str,
    markdown: str,
    records: list[dict[str, object]],
    output_format: str = "plain",
) -> str:
    with tempfile.TemporaryDirectory(prefix="zgu-citation-") as temp_name:
        temp = Path(temp_name)
        markdown_path = temp / "input.md"
        bibliography_path = temp / "references.json"
        markdown_path.write_text(markdown, encoding="utf-8")
        bibliography_path.write_text(json.dumps(records), encoding="utf-8")

        return run_pandoc(
            markdown_path,
            bibliography_path,
            style_file,
            output_format=output_format,
        )


def render_citation(
    style_file: str,
    markdown: str,
    records: list[dict[str, object]],
) -> str:
    rendered = render_records(style_file, markdown, records)
    return rendered.splitlines()[0]


def render_bibliography(
    style_file: str,
    heading: str,
    records: list[dict[str, object]],
    citation: str | None = None,
) -> str:
    citation = citation or "; ".join(f"@{record['id']}" for record in records)
    rendered = render_records(
        style_file,
        f"[{citation}].\n\n# {heading}\n",
        records,
    )
    return rendered.split(f"{heading}\n\n", maxsplit=1)[1]
