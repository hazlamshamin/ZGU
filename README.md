# ZGU

ZGU provides two CSL citation styles for **Gaya UKM**, the thesis style used by
Universiti Kebangsaan Malaysia.

> **Disclaimer:** ZGU is an unofficial project. It is independently adapted from
> the official Gaya UKM guides, but it is not published, approved, or endorsed by
> Universiti Kebangsaan Malaysia. Always check your final document against the
> official guide and your faculty's current requirements.

Use these styles with Zotero or Mendeley to format citations and references
according to the supported rules in the official Gaya UKM guide.

## Which Style Do I Need?

- Use [gaya-ukm-malay.csl](styles/gaya-ukm-malay.csl) if your thesis is written
  in Bahasa Melayu.
- Use [gaya-ukm-english.csl](styles/gaya-ukm-english.csl) if your thesis is
  written in English.

You only need one style. Do not load both into the same document.

## Install in Zotero

1. Download the `.csl` file you need from the `styles` folder.
2. Open Zotero and go to **Settings** or **Preferences**.
3. Open **Cite**, then **Styles**.
4. Click the **+** or **Add** button.
5. Select the downloaded `.csl` file.
6. Open your document and choose **ZGU** from the citation style list in the
   Zotero toolbar.

The menu may be under **Zotero > Document Preferences** in Word, LibreOffice, or
a Zotero-enabled WPS installation. Menu names can differ slightly between plugin
versions.

This repository contains the citation styles, not the Zotero word-processor
plugin. In WPS, use the Zotero-WPS connector you already installed. If ZGU does
not appear there, first confirm that it appears in Zotero's style list.

## Zotero, Mendeley, and EndNote

ZGU files are standard CSL 1.0 styles.

| Software | Compatibility | How to use it |
|---|---|---|
| Zotero | Native | Add the `.csl` file under **Settings > Cite > Styles** |
| Mendeley Cite | Custom style | Choose **Add a custom style** and paste the raw CSL URL |
| EndNote | Not supported directly | EndNote requires a separate `.ens` output style |

ZGU is not registered in the public CSL style repository used by Zotero and
Mendeley, so neither product lists it in the built-in style search. Add the
downloaded file in Zotero, or use the custom-style URL option in Mendeley Cite:

```text
English:
https://raw.githubusercontent.com/hazlamshamin/ZGU/main/styles/gaya-ukm-english.csl

Bahasa Melayu:
https://raw.githubusercontent.com/hazlamshamin/ZGU/main/styles/gaya-ukm-malay.csl
```

EndNote cannot import a `.csl` file directly. It uses the proprietary `.ens`
format, so no EndNote style is included. Exporting references from Zotero or
Mendeley into EndNote does not convert the citation style.

## Basic Workflow

1. Put your cursor where the citation should appear.
2. In the Zotero toolbar, click **Add/Edit Citation**.
3. Search for the source and select it.
4. Put your cursor at the end of the document.
5. Click **Add/Edit Bibliography**.

Zotero will create the reference list from the sources you cite. Do not type the
bibliography by hand unless you are deliberately converting it to plain text.

## Common Citation Examples

### Citation inside parentheses

Use **Add/Edit Citation** normally:

```text
(Hawkings 2012)
(Abdul Rahman & Arsmah 2009)
(Jamaluddin 2007, 2009, 2012)
```

### Author name already in the sentence

When the author name is already part of your sentence, type the author names and
then insert the citation with **Suppress Author** enabled:

```text
Abdul Razak and Abu Osman (2009)
Abdul Rahman dan Arsmah (2009)
```

This step is necessary because Zotero cannot tell whether the author name is
already in your sentence. Without **Suppress Author**, the name may appear twice.

### Several sources in one citation

Add each source through **Add/Edit Citation** in the same citation box:

```text
(Abdul Samad 2011; Azahan 2011; Jamaluddin 2010; Kadir 2012)
```

ZGU will sort the sources and separate them with semicolons.

### Authors with the same surname

If the authors have the same surname, ZGU will use their given names or
initials when needed:

```text
(Khalid B.A.K. 2010; Khalid Yusoff 2010)
```

This works only when the author names are stored correctly in Zotero. Put the
surname in **Last Name** and the remaining name in **First Name**.

## Check Your Zotero Metadata

The style can only format the information that Zotero receives.

- Use full institutional names. ZGU does not automatically turn
  `Dewan Bahasa dan Pustaka` into `DBP`.
- Enter titles in the required title case. ZGU does not change title case.
- If a source has no named author and its title starts with **A**, **An**, or
  **The**, put the sortable form in Zotero's **Short Title** field. For example, use
  `Encyclopaedia of Islam` for `The Encyclopaedia of Islam`.
- Keep italics already present in a title, such as a species name. Zotero and
  ZGU preserve that imported italic text.
- If a field is missing, repair it in Zotero and click **Refresh** in the Zotero
  toolbar.

Missing publication information is shown as `s.l.: s.n.` in the English style
and `t.tp.: t.pt.` in the Malay style.

## Reference List Layout

ZGU creates one paragraph for each reference. It avoids manual line breaks and
requests single-spaced entries with no extra space between them.

For the guide's exact `12.5 mm` second-line indent, adjust the generated
**Bibliography** paragraph style in your word processor:

1. Right-click **Bibliography** in the **Styles** pane and choose **Modify**.
2. Open **Format > Paragraph**.
3. Set **Left indent** to `1.25 cm`.
4. Set **Special > Hanging** to `1.25 cm`.
5. Set **Line spacing** to **Single** and spacing before/after to `0 pt`.

The exact menu location may differ in WPS or LibreOffice, but the paragraph
settings are the same. Citation styles cannot store the exact indent width, so
this is a one-time document-formatting step.

## Supported Sources

The styles cover the main source types used in Gaya UKM Chapters IV and V:

- books, edited books, and chapters
- journal, magazine, and newspaper articles
- conference papers
- theses, reports, and manuscripts
- legislation
- webpages
- software manuals and software

This is a focused Gaya UKM style, not a complete implementation of every example
in the guide.

## What Is Not Included

- No repository-level license or `LICENSE` file.
- No Zotero add-on, Mendeley add-on, or EndNote style.
- No Word, WPS, LibreOffice, or LaTeX thesis template.
- No cover page, margin setup, font setup, or full thesis page layout.
- No footnotes, short-note forms, Al-Quran citations, Hadith citations, or Arabic/Jawi ordering.
- No automatic conversion of institution names to acronyms.
- No automatic title translation or automatic title-case correction.
- No automatic cultural-name parsing for Malay, Arabic, Chinese, Indonesian, or Sabah/Sarawak names.
- No dedicated support for legal cases, films, videos, datasets, interviews, personal communications, meeting papers, compilers, coordinators, monographs, or translations.
- No automatic enforcement of the guide's exact `12.5 mm` hanging-indent width inside every word processor.
- No bundled copies of the UKM PDF guides or the GayaUKM LaTeX template.

## Comparison With Other UKM Styles

The table compares the main-source behaviour tested against the official guides.

- **ZGU**: the styles in this repository.
- **Canonical**: [Universiti Kebangsaan Malaysia (Malay)](https://www.zotero.org/styles/universiti-kebangsaan-malaysia).
- **Mendeley Malay**: [GayaUKM-Melayu-MazlehaMaskin](http://csl.mendeley.com/styles/66537561/GayaUKM-MelayuMazleha).
- **Mendeley English**: [UKM (English) - Mazleha Maskin](https://csl.mendeley.com/styles/66537561/universiti-kebangsaan-malaysia-mazleha-Eng).

`✓` means the tested examples match the guide. `✗` means at least one tested
example fails. `—` means the style is not intended for that language.

| Tested behaviour | ZGU | Canonical | Mendeley Malay | Mendeley English |
|---|---|---|---|---|
| English three-author rule | ✓ | — | — | ✓ |
| Malay two/three-author rule | ✓ | ✓ | ✗ (uses `et al.`) | — |
| Same-surname authors expanded | ✓ | ✗ (not expanded) | ✗ (initial before surname) | ✗ (not expanded) |
| Anonymous sources use `Anon.` | ✓ | ✗ | ✗ | ✗ |
| Page locator uses a colon | ✓ | ✗ (`hlm.` form) | ✗ (no colon) | ✗ (`, p.` form) |
| Books, edited books, and chapters | ✓ | ✗ (place/publisher reversed) | ✗ (punctuation) | ✓ |
| Journal articles | ✓ | ✓ | ✓ | ✓ |
| Magazines and newspapers | ✓ | ✗ (dates/months missing) | ✗ | ✗ |
| Theses, reports, and manuscripts | ✓ | ✗ | ✗ | ✗ |
| Legislation and act number | ✓ | ✗ | ✗ | ✗ |
| Webpages and access dates | ✓ | ✓ | ✗ (punctuation) | ✓ |
| Software and software manuals | ✓ | ✗ (version missing) | ✗ (version missing) | ✗ (version missing) |
| Book and container-title italics | ✓ | ✗ (books upright) | ✓ | ✓ |
| Single-spaced reference list | ✓ | ✗ (double) | ✗ (double) | ✗ (double) |
| Exact `12.5 mm` hanging indent | ✗ (set `1.25 cm` in Word/WPS) | ✗ | ✗ | ✗ |
| Narrative `and`/`dan` conjunction | ✗ (type names; **Suppress Author**) | ✗ | ✗ | ✗ |
| Footnotes, Al-Quran, and Hadith | ✗ (not included) | ✗ | ✗ | ✗ |

On the current source-backed fixtures, ZGU matches **13/13 citation examples and
16/16 reference examples in both languages**. The other styles have material
gaps in the main source types shown above. ZGU is still not a full implementation
of every source type or formatting rule in the official guides.

## Common Problems

- **The wrong name appears.** Check the author's **Last Name** and **First Name**
  fields in Zotero, then refresh the citation.
- **A DBP or DOSH citation does not shorten automatically.** Enter the shorter
  institution name yourself. ZGU cannot infer an acronym from a full name.
- **The title is in the wrong position.** For an authorless A, An, or The title,
  fill in Zotero's **Short Title** field.
- **Italic text disappeared from a title.** Check whether the italics are present
  in Zotero's title field. ZGU preserves imported italics but cannot reconstruct
  formatting that was removed before import.
- **The indentation is wrong.** Change the **Bibliography** paragraph style using
  the steps above.

## For Developers

Pandoc with citeproc support is required. The test suite is currently verified
with Python 3.14, Pandoc 3.8.2, latexmk 4.67, pdftotext 26.03.0, and Java 23.

Run the main tests:

```sh
uv run python -m unittest discover -s tests -v
```

Check the checked-in examples against the official UKM PDFs:

```sh
uv run python tests/official/check_official_sources.py -v
```

Check against the maintained GayaUKM LaTeX styles:

```sh
uv run python tests/latex/check_latex.py -v
```

## Sources

- [UKM Gaya UKM postgraduate page](https://www.ukm.my/akademik/pelajar-pascasiswazah/)
- [GayaUKM LaTeX repository](https://github.com/mohdhairimohdzaman/GayaUKM)

## Issues

If you find a discrepancy with the official Gaya UKM guide, open an issue in this
repository. Include the guide page, the source type, and the output you expected.
