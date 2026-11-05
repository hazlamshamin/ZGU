from __future__ import annotations

import json
import re
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

from tests.csl_harness import (
    CSL_NAMESPACE,
    EXPECTED,
    FIXTURES,
    NS,
    PROJECT_ROOT,
    STYLES,
    STYLE_FILES,
    render,
    render_bibliography,
    render_citation,
    render_records,
    run_pandoc,
)


class StyleContractTests(unittest.TestCase):
    def load_style(self, name: str) -> ET.Element:
        return ET.parse(STYLES / name).getroot()

    def test_styles_have_hsas_adaptation_metadata(self) -> None:
        for style_name in STYLE_FILES:
            with self.subTest(style=style_name):
                root = self.load_style(style_name)
                self.assertEqual(root.tag, f"{{{CSL_NAMESPACE}}}style")
                self.assertEqual(root.attrib["class"], "in-text")
                self.assertEqual(root.attrib["version"], "1.0")

                author = root.find(".//csl:info/csl:author/csl:name", NS)
                contributors = [
                    contributor.text
                    for contributor in root.findall(
                        ".//csl:info/csl:contributor/csl:name", NS
                    )
                ]
                category = root.find(
                    ".//csl:info/csl:category[@citation-format='author-date']", NS
                )
                summary = root.findtext(".//csl:info/csl:summary", default="", namespaces=NS)
                self.assertIsNotNone(author)
                self.assertEqual(author.text, "HSAS")
                self.assertEqual(contributors, ["Mazleha Maskin", "Fareed Sairi"])
                self.assertIsNotNone(category)
                self.assertIn("Adapted by HSAS", summary)

    def test_styles_link_the_current_official_manuals(self) -> None:
        expected_pdf = {
            "gaya-ukm-malay.csl": "2015-GayaUKM-BM.pdf",
            "gaya-ukm-english.csl": "2015-GayaUKM-BI-Final.pdf",
        }
        for style_name, pdf_name in expected_pdf.items():
            with self.subTest(style=style_name):
                root = self.load_style(style_name)
                links = [
                    link.attrib["href"]
                    for link in root.findall(".//csl:info/csl:link", NS)
                    if link.attrib.get("rel") == "documentation"
                ]
                self.assertTrue(
                    any(
                        link.startswith("https://www.ukm.my/akademik/")
                        and link.endswith(pdf_name)
                        for link in links
                    ),
                    links,
                )
                self.assertIn("https://github.com/mohdhairimohdzaman/GayaUKM", links)

    def test_styles_do_not_assert_a_license(self) -> None:
        for style_name in STYLE_FILES:
            with self.subTest(style=style_name):
                root = self.load_style(style_name)
                self.assertIsNone(root.find(".//csl:info/csl:rights", NS))

    def test_reference_layout_is_single_spaced_with_hanging_indent(self) -> None:
        for style_name in STYLE_FILES:
            with self.subTest(style=style_name):
                root = self.load_style(style_name)
                bibliography = root.find("csl:bibliography", NS)
                self.assertIsNotNone(bibliography)
                self.assertEqual(bibliography.attrib["line-spacing"], "1")
                self.assertEqual(bibliography.attrib["hanging-indent"], "true")
                self.assertEqual(bibliography.attrib["entry-spacing"], "0")

    def test_readme_documents_the_exact_hanging_indent(self) -> None:
        readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
        for fragment in ("12.5 mm", "1.25 cm", "Special > Hanging", "Single", "0 pt"):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, readme)

    def test_each_reference_renders_as_one_indented_paragraph(self) -> None:
        cases = (
            ("gaya-ukm-malay.csl", "official-malay"),
            ("gaya-ukm-english.csl", "official-english"),
        )
        for style_file, fixture_stem in cases:
            with self.subTest(style=style_file):
                bibliography = json.loads(
                    (FIXTURES / f"{fixture_stem}.json").read_text(encoding="utf-8")
                )
                html = render(style_file, fixture_stem, "html")
                entries = re.findall(
                    r'<div id="ref-[^"]+" class="csl-entry" role="listitem">',
                    html,
                )
                self.assertEqual(len(entries), len(bibliography))
                self.assertIn(
                    'class="references csl-bib-body hanging-indent"',
                    html,
                )
                self.assertIn('data-entry-spacing="0"', html)
                self.assertNotIn("<br", html)

    def test_generated_docx_uses_one_paragraph_per_reference(self) -> None:
        word_namespace = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
        word_ns = {"w": word_namespace}
        cases = (
            ("gaya-ukm-malay.csl", "official-malay"),
            ("gaya-ukm-english.csl", "official-english"),
        )
        for style_file, fixture_stem in cases:
            with self.subTest(style=style_file):
                bibliography = json.loads(
                    (FIXTURES / f"{fixture_stem}.json").read_text(encoding="utf-8")
                )
                with tempfile.TemporaryDirectory(prefix="zgu-docx-") as temp_name:
                    output_path = Path(temp_name) / "output.docx"
                    run_pandoc(
                        FIXTURES / f"{fixture_stem}.md",
                        FIXTURES / f"{fixture_stem}.json",
                        style_file,
                        output_path=output_path,
                    )
                    with zipfile.ZipFile(output_path) as archive:
                        document = ET.fromstring(archive.read("word/document.xml"))

                bibliography_paragraphs = []
                for paragraph in document.findall(".//w:p", word_ns):
                    style = paragraph.find("w:pPr/w:pStyle", word_ns)
                    if (
                        style is not None
                        and style.get(f"{{{word_namespace}}}val") == "Bibliography"
                    ):
                        bibliography_paragraphs.append(paragraph)
                self.assertEqual(len(bibliography), len(bibliography_paragraphs))
                self.assertEqual([], document.findall(".//w:br", word_ns))


class OfficialReferenceTests(unittest.TestCase):
    def assert_official_excerpts(self, actual: str, excerpt_name: str) -> None:
        excerpts = (EXPECTED / excerpt_name).read_text(encoding="utf-8").splitlines()
        for excerpt in filter(None, excerpts):
            with self.subTest(excerpt=excerpt):
                self.assertIn(excerpt, actual)

    def test_malay_official_examples_match_snapshot(self) -> None:
        actual = render("gaya-ukm-malay.csl", "official-malay", "plain")
        expected = (EXPECTED / "official-malay.txt").read_text(encoding="utf-8").strip()
        self.assertMultiLineEqual(expected, actual)
        self.assert_official_excerpts(actual, "malay-official-excerpts.txt")

    def test_english_official_examples_match_snapshot(self) -> None:
        actual = render("gaya-ukm-english.csl", "official-english", "plain")
        expected = (EXPECTED / "official-english.txt").read_text(encoding="utf-8").strip()
        self.assertMultiLineEqual(expected, actual)
        self.assert_official_excerpts(actual, "english-official-excerpts.txt")

    def test_malay_preserves_required_italics(self) -> None:
        html = render("gaya-ukm-malay.csl", "official-malay", "html")
        required = (
            "<em>Memoir Arena Wati: Enda Gulingku</em>",
            "<em>Journal Institute of Materials Malaysia</em>",
            "<em>Pengurusan Persekitaran di Malaysia: Isu dan Cabaran</em>",
            "<em>Dewan Sastera</em>",
            "<em>Proceedings of the 2nd World Engineering Congress</em>",
        )
        for fragment in required:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, html)

    def test_english_preserves_required_italics(self) -> None:
        html = render("gaya-ukm-english.csl", "official-english", "html")
        required = (
            "<em>Topology: A Geometric Account of General Topology, Homotopy Types and the Fundamental Groupoid</em>",
            "<em>Measures for Clinical Practice: Source Book</em>",
            "<em>Reader’s Digest</em>",
            "<em>Journal Institute of Materials Malaysia</em>",
            "<em>Proceedings of the 2nd World Engineering Congress</em>",
        )
        for fragment in required:
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, html)


class BibliographyExampleTests(unittest.TestCase):
    def test_general_newspaper_reference_uses_newspaper_name(self) -> None:
        cases = (
            ("gaya-ukm-english.csl", "References"),
            ("gaya-ukm-malay.csl", "Rujukan"),
        )
        record = {
            "id": "general-newspaper",
            "type": "article-newspaper",
            "container-title": "Berita Harian",
            "issued": {"date-parts": [[2005, 11, 28]]},
        }
        for style_file, heading in cases:
            with self.subTest(style=style_file):
                bibliography = render_bibliography(style_file, heading, [record])
                self.assertEqual("Berita Harian. 2005. 28 November.", bibliography)

    def test_anonymous_newspaper_uses_anon_author_marker(self) -> None:
        cases = (
            (
                "gaya-ukm-english.csl",
                "References",
                "Anon. 2011. Syarikat Itali akan sediakan radar kawalan laluan udara. Utusan Malaysia, 30 October: 3.",
            ),
            (
                "gaya-ukm-malay.csl",
                "Rujukan",
                "Anon. 2011. Syarikat Itali akan sediakan radar kawalan laluan udara. Utusan Malaysia, 30 Oktober: 3.",
            ),
        )
        for style_file, heading, expected in cases:
            with self.subTest(style=style_file):
                record = {
                    "id": "anonymous-newspaper",
                    "type": "article-newspaper",
                    "issued": {"date-parts": [[2011, 10, 30]]},
                    "title": "Syarikat Itali akan sediakan radar kawalan laluan udara",
                    "container-title": "Utusan Malaysia",
                    "page": "3",
                }
                bibliography = render_bibliography(style_file, heading, [record])
                self.assertEqual(expected, bibliography)

    def test_authorless_titles_sort_by_the_word_after_a_an_or_the(self) -> None:
        records = [
            {
                "id": "sandwich",
                "type": "book",
                "issued": {"date-parts": [[2012]]},
                "title": "A Sandwich Enzyme Immunoassay",
                "title-short": "Sandwich Enzyme Immunoassay",
            },
            {
                "id": "experimental",
                "type": "book",
                "issued": {"date-parts": [[2006]]},
                "title": "An Experimental Model Application",
                "title-short": "Experimental Model Application",
            },
            {
                "id": "contribution",
                "type": "book",
                "issued": {"date-parts": [[2006]]},
                "title": "The Contribution of Measurement",
                "title-short": "Contribution of Measurement",
            },
        ]
        cases = (
            ("gaya-ukm-english.csl", "References"),
            ("gaya-ukm-malay.csl", "Rujukan"),
        )
        for style_file, heading in cases:
            with self.subTest(style=style_file):
                bibliography = render_bibliography(style_file, heading, records).splitlines()
                titles = [
                    line.split(". ", maxsplit=2)[0]
                    for line in bibliography
                    if line.strip()
                ]
                self.assertEqual(
                    [
                        "The Contribution of Measurement",
                        "An Experimental Model Application",
                        "A Sandwich Enzyme Immunoassay",
                    ],
                    titles,
                )

    def test_missing_place_and_publisher_use_guide_abbreviations(self) -> None:
        cases = (
            (
                "gaya-ukm-english.csl",
                "References",
                "Brown, R. 2008. Topology. s.l.: s.n.",
            ),
            (
                "gaya-ukm-malay.csl",
                "Rujukan",
                "Brown, R. 2008. Topology. t.tp.: t.pt.",
            ),
        )
        record = {
            "id": "missing-publication-data",
            "type": "book",
            "author": [{"family": "Brown", "given": "R."}],
            "issued": {"date-parts": [[2008]]},
            "title": "Topology",
        }
        for style_file, heading, expected in cases:
            with self.subTest(style=style_file):
                bibliography = render_bibliography(style_file, heading, [record])
                self.assertEqual(expected, bibliography)

    def test_volume_labels_follow_each_language_guide(self) -> None:
        cases = (
            ("gaya-ukm-english.csl", "References", "Vol. 2"),
            ("gaya-ukm-malay.csl", "Rujukan", "Jil. 2"),
        )
        record = {
            "id": "volume",
            "type": "book",
            "author": [{"family": "Abu Osman Md. Tap"}],
            "issued": {"date-parts": [[2009]]},
            "title": "Matematik Pertama",
            "volume": "2",
            "publisher-place": "Kuala Lumpur",
            "publisher": "Dewan Bahasa dan Pustaka",
        }
        for style_file, heading, expected in cases:
            with self.subTest(style=style_file):
                bibliography = render_bibliography(style_file, heading, [record])
                self.assertIn(expected, bibliography)

    def test_non_book_reference_examples_keep_their_titles_upright(self) -> None:
        cases = (
            (
                "gaya-ukm-english.csl",
                {
                    "id": "report",
                    "type": "report",
                    "author": [{"family": "Hafriza Burhanudeen"}],
                    "issued": {"date-parts": [[2003]]},
                    "title": "A comparative study of linguistic strategies",
                    "genre": "Technical report",
                    "number": "UKM SK/008/2003",
                },
            ),
            (
                "gaya-ukm-english.csl",
                {
                    "id": "webpage",
                    "type": "webpage",
                    "author": [{"family": "Crane", "given": "N."}],
                    "issued": {"date-parts": [[2007]]},
                    "title": "Electronic sources: MLA style of citation",
                    "URL": "https://example.com",
                },
            ),
            (
                "gaya-ukm-english.csl",
                {
                    "id": "manuscript",
                    "type": "manuscript",
                    "author": [{"family": "Hamzah Fansuri"}],
                    "title": "Sharab al-cAshiqin",
                    "archive": "MSS. Cod. Or. 7291 (11)",
                    "publisher": "University Leiden Library",
                },
            ),
            (
                "gaya-ukm-english.csl",
                {
                    "id": "software-manual",
                    "type": "software",
                    "author": [{"family": "MSC.Nastran"}],
                    "issued": {"date-parts": [[2008]]},
                    "title": "Quick Reference Guide",
                    "publisher-place": "Santa Ana",
                    "publisher": "MSC. Software Corporation",
                },
            ),
            (
                "gaya-ukm-english.csl",
                {
                    "id": "software",
                    "type": "software",
                    "issued": {"date-parts": [[2005]]},
                    "title": "MATLAB",
                    "version": "7.1",
                    "publisher-place": "Massachusetts",
                    "publisher": "Math Works Inc.",
                },
            ),
            (
                "gaya-ukm-english.csl",
                {
                    "id": "authorless-report",
                    "type": "report",
                    "issued": {"date-parts": [[2024]]},
                    "title": "Authorless technical report",
                    "genre": "Technical report",
                },
            ),
            (
                "gaya-ukm-malay.csl",
                {
                    "id": "authorless-report",
                    "type": "report",
                    "issued": {"date-parts": [[2024]]},
                    "title": "Laporan teknik tanpa pengarang",
                    "genre": "Laporan Teknik",
                },
            ),
        )
        for style_file, record in cases:
            title = str(record["title"])
            with self.subTest(type=record["type"], title=title):
                html = render_records(
                    style_file,
                    f"[@{record['id']}].\n\n# References\n",
                    [record],
                    output_format="html",
                )
                self.assertNotIn(f"<em>{title}</em>", html)

    def test_imported_inline_title_italics_are_preserved(self) -> None:
        cases = (
            ("gaya-ukm-english.csl", "Ecology of <i>Danaus plexippus</i> in Malaysia"),
            ("gaya-ukm-malay.csl", "Ekologi <i>Danaus plexippus</i> di Malaysia"),
        )
        for style_file, title in cases:
            with self.subTest(style=style_file):
                record = {
                    "id": "species",
                    "type": "report",
                    "author": [{"family": "Nur Aina"}],
                    "issued": {"date-parts": [[2024]]},
                    "title": title,
                    "genre": "Technical report",
                    "number": "ZGU/1",
                }
                html = render_records(
                    style_file,
                    "[@species].\n\n# References\n",
                    [record],
                    output_format="html",
                )
                self.assertIn("<em>Danaus plexippus</em>", html)

    def test_official_software_manual_and_software_references(self) -> None:
        cases = (
            (
                "gaya-ukm-english.csl",
                "References",
                {
                    "id": "adams",
                    "type": "software",
                    "author": [{"family": "ADAMS.Flex 2002"}],
                    "issued": {"date-parts": [[2012]]},
                    "title": "Using ADAM/Flex",
                    "publisher-place": "Ann Arbor",
                    "publisher": "Mechanical Dynamics Incorporated",
                },
                "ADAMS.Flex 2002. 2012. Using ADAM/Flex. Ann Arbor: Mechanical Dynamics Incorporated.",
            ),
            (
                "gaya-ukm-english.csl",
                "References",
                {
                    "id": "abaqus",
                    "type": "software",
                    "issued": {"date-parts": [[2005]]},
                    "title": "ABAQUS/Explicit",
                    "version": "6.5",
                    "publisher-place": "Providence",
                    "publisher": "ABAQUS Inc.",
                },
                "ABAQUS/Explicit. 2005. Version 6.5. Providence: ABAQUS Inc.",
            ),
            (
                "gaya-ukm-malay.csl",
                "Rujukan",
                {
                    "id": "adams",
                    "type": "software",
                    "author": [{"family": "ADAMS.Flex 2002"}],
                    "issued": {"date-parts": [[2002]]},
                    "title": "Using ADAM/Flex",
                    "publisher-place": "Ann Arbor",
                    "publisher": "Mechanical Dynamics Incorporated",
                },
                "ADAMS.Flex 2002. 2002. Using ADAM/Flex. Ann Arbor: Mechanical Dynamics Incorporated.",
            ),
            (
                "gaya-ukm-malay.csl",
                "Rujukan",
                {
                    "id": "abaqus",
                    "type": "software",
                    "issued": {"date-parts": [[2005]]},
                    "title": "ABAQUS/Explicit",
                    "version": "6.5",
                    "publisher-place": "Providence",
                    "publisher": "ABAQUS Inc.",
                },
                "ABAQUS/Explicit. 2005. Version 6.5. Providence: ABAQUS Inc.",
            ),
        )
        for style_file, heading, record, expected in cases:
            with self.subTest(style=style_file, record=record["id"]):
                bibliography = render_bibliography(style_file, heading, [record])
                self.assertEqual(expected, bibliography)


class CitationPatternTests(unittest.TestCase):
    def render_citations(
        self, style_file: str, fixture_stem: str, bibliography_heading: str
    ) -> str:
        rendered = render(style_file, fixture_stem, "plain")
        marker = f"\n{bibliography_heading}\n"
        self.assertIn(marker, rendered)
        return rendered.split(marker, maxsplit=1)[0].strip()

    def assert_citation_snapshot(
        self, style_file: str, fixture_stem: str, heading: str, expected_name: str
    ) -> None:
        actual = self.render_citations(style_file, fixture_stem, heading)
        expected = (EXPECTED / expected_name).read_text(encoding="utf-8").strip()
        self.assertMultiLineEqual(expected, actual)

    def test_malay_citation_examples_match_snapshot(self) -> None:
        self.assert_citation_snapshot(
            "gaya-ukm-malay.csl",
            "citations-malay",
            "Rujukan",
            "citations-malay.txt",
        )

    def test_english_citation_examples_match_snapshot(self) -> None:
        self.assert_citation_snapshot(
            "gaya-ukm-english.csl",
            "citations-english",
            "References",
            "citations-english.txt",
        )

    def test_same_name_authors_expand_given_names(self) -> None:
        cases = (
            (
                "gaya-ukm-english.csl",
                "Khalid B.A.K.",
                "Khalid Yusoff",
                "First work",
                "Second work",
                "Citation: (Khalid B.A.K. 2010; Khalid Yusoff 2010).",
            ),
            (
                "gaya-ukm-malay.csl",
                "Khalid Ahmad",
                "Khalid Yusoff",
                "Karya pertama",
                "Karya kedua",
                "Citation: (Khalid Ahmad 2010; Khalid Yusoff 2010).",
            ),
        )
        for style_file, first_name, second_name, first_title, second_title, expected in cases:
            with self.subTest(style=style_file):
                given_by_name = {
                    first_name: first_name.removeprefix("Khalid "),
                    second_name: second_name.removeprefix("Khalid "),
                }
                first_record = {
                    "id": "same-name",
                    "type": "article-journal",
                    "author": [
                        {"family": "Khalid", "given": given_by_name[first_name]},
                    ],
                    "issued": {"date-parts": [[2010]]},
                    "title": first_title,
                    "container-title": {
                        "gaya-ukm-english.csl": "Journal",
                        "gaya-ukm-malay.csl": "Jurnal",
                    }[style_file],
                }
                second_record = {
                    **first_record,
                    "id": "same-name-2",
                    "author": [
                        {"family": "Khalid", "given": given_by_name[second_name]},
                    ],
                    "title": second_title,
                }

                citation = render_citation(
                    style_file,
                    "Citation: [@same-name; @same-name-2].\n",
                    [first_record, second_record],
                )
                self.assertEqual(expected, citation)

    def test_narrative_coauthors_use_the_guide_conjunction_workflow(self) -> None:
        cases = (
            (
                "gaya-ukm-english.csl",
                "Abdul Razak and Abu Osman [-@two].",
                "Abdul Razak and Abu Osman (2009).",
                2009,
                [
                    {"family": "Abdul Razak", "given": "A."},
                    {"family": "Abu Osman", "given": "A."},
                ],
            ),
            (
                "gaya-ukm-english.csl",
                "Shafaratul et al. [-@three].",
                "Shafaratul et al. (2011).",
                2011,
                [
                    {"family": "Shafaratul"},
                    {"family": "Second"},
                    {"family": "Third"},
                ],
            ),
            (
                "gaya-ukm-malay.csl",
                "Abdul Rahman dan Arsmah [-@two].",
                "Abdul Rahman dan Arsmah (2009).",
                2009,
                [
                    {"family": "Abdul Rahman", "given": "A."},
                    {"family": "Arsmah", "given": "I."},
                ],
            ),
            (
                "gaya-ukm-malay.csl",
                "Baharudin, Abdullah Marwi dan Hidayatul [-@three].",
                "Baharudin, Abdullah Marwi dan Hidayatul (2012).",
                2012,
                [
                    {"family": "Baharudin"},
                    {"family": "Abdullah Marwi"},
                    {"family": "Hidayatul"},
                ],
            ),
        )
        for style_file, markdown, expected, year, authors in cases:
            with self.subTest(style=style_file, expected=expected):
                record = {
                    "id": "two" if "two" in markdown else "three",
                    "type": "article-journal",
                    "author": authors,
                    "issued": {"date-parts": [[year]]},
                    "title": "Narrative fixture",
                    "container-title": "Fixture Journal",
                }
                actual = render_citation(
                    style_file,
                    f"{markdown}\n\n# References\n",
                    [record],
                )
                self.assertEqual(expected, actual)

    def test_official_software_and_manual_citations(self) -> None:
        cases = (
            ("gaya-ukm-english.csl", "ADAMS/Flex", 2012, "manual", "(ADAMS/Flex 2012)"),
            (
                "gaya-ukm-english.csl",
                "MSC.Nastran",
                2011,
                "manual",
                "(MSC.Nastran 2011)",
            ),
            (
                "gaya-ukm-english.csl",
                "ABAQUS/EXPLICIT",
                2009,
                "software",
                "(ABAQUS/EXPLICIT 2009)",
            ),
            ("gaya-ukm-english.csl", "MATLAB", 2008, "software", "(MATLAB 2008)"),
            (
                "gaya-ukm-malay.csl",
                "ADAMS/Flex",
                2012,
                "manual",
                "(ADAMS/Flex 2012)",
            ),
            (
                "gaya-ukm-malay.csl",
                "MSC.Nastran",
                2011,
                "manual",
                "(MSC.Nastran 2011)",
            ),
            (
                "gaya-ukm-malay.csl",
                "ABAQUS / EXPLICIT",
                2009,
                "software",
                "(ABAQUS / EXPLICIT 2009)",
            ),
            ("gaya-ukm-malay.csl", "MATLAB", 2008, "software", "(MATLAB 2008)"),
        )
        for style_file, title, year, kind, expected in cases:
            with self.subTest(style=style_file, title=title):
                record: dict[str, object] = {
                    "id": "software",
                    "type": "software",
                    "issued": {"date-parts": [[year]]},
                    "title": title,
                }
                if kind == "manual":
                    record["author"] = [{"family": title}]
                actual = render_citation(
                    style_file,
                    "Citation: [@software]",
                    [record],
                )
                self.assertEqual(f"Citation: {expected}", actual)

    def test_official_single_author_and_institution_citations(self) -> None:
        cases: tuple[tuple[str, int, str, bool], ...] = (
            ("Mohd. Fuad", 2010, "(Mohd. Fuad 2010)", False),
            ("Noor Azlan Ghazali", 2012, "(Noor Azlan Ghazali 2012)", False),
            ("Chan Ngai Weng", 2011, "(Chan Ngai Weng 2011)", False),
            ("Reid", 2012, "(Reid 2012)", False),
            ("Romlah", 2009, "(Romlah 2009)", False),
            ("Shaharir", 2010, "(Shaharir 2010)", False),
            (
                "International Labour Office",
                2010,
                "(International Labour Office 2010)",
                True,
            ),
            (
                "Jabatan Standard Malaysia",
                2011,
                "(Jabatan Standard Malaysia 2011)",
                True,
            ),
            (
                "Institute of Quality Assurance",
                2012,
                "(Institute of Quality Assurance 2012)",
                True,
            ),
        )
        for author, year, expected, is_institution in cases:
            with self.subTest(author=author):
                author_name = {"literal": author} if is_institution else {"family": author}
                record = {
                    "id": "citation",
                    "type": "report" if is_institution else "article-journal",
                    "author": [author_name],
                    "issued": {"date-parts": [[year]]},
                    "title": "Citation fixture",
                    "container-title": "Fixture Journal",
                }
                actual = render_citation(
                    "gaya-ukm-english.csl",
                    "Citation: [@citation]",
                    [record],
                )
                self.assertEqual(f"Citation: {expected}", actual)


if __name__ == "__main__":
    unittest.main()
