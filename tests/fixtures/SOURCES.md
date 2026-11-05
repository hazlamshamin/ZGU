# Fixture provenance

The fixtures are reduced, machine-readable versions of examples in the official UKM manuals.

## Two independent test layers

- `official-malay.*` and `official-english.*` contain source-backed bibliography examples only. They use `nocite` so the complete fixture set is rendered, and their snapshots do not contain synthetic records.
- `citations-malay.*` and `citations-english.*` contain the minimum records needed to exercise the guide's in-text citation patterns. Tests compare only the citation text before the bibliography heading. Their invented titles and journal names are deliberately outside the official reference snapshots.
- Additional inline probes in `tests/test_conformance.py` separate source-backed examples from synthetic edge probes. Tests named `test_official_*` use guide examples; synthetic probes exercise the missing publication-data fallback, Short Title sorting mechanics, and rich-text italic preservation.

## Common sources

- Malay: [Panduan Penulisan Tesis Gaya UKM, 2015](https://www.ukm.my/akademik/wp-content/uploads/2022/12/2015-GayaUKM-BM.pdf)
- English: [UKM Thesis Writing Style Guideline according to Gaya UKM, 2015](https://www.ukm.my/akademik/wp-content/uploads/2022/12/2015-GayaUKM-BI-Final.pdf)

## Source sections

| Fixture behaviour | Malay manual | English manual |
|---|---|---|
| One author in text | 4.2.1 | 4.2.1 |
| Two authors in text | 4.2.2(a) | 4.2.2(a) |
| Three authors in text | 4.2.2(a) | 4.2.2(b) |
| Four or more authors in text | 4.2.2(b) | 4.2.2(b) |
| Institutional author | 4.2.3 | 4.2.3 |
| Unknown author | 4.2.4 | 4.2.4 |
| Multiple citations and year suffixes | 4.2.6 | 4.2.6 |
| Narrative citation and page locator | 4.2.1 and Appendix R1 | 4.2.1 and Appendix R1 |
| Software citation | 4.2.9 | 4.2.9 |
| Book | 5.3(a) and 5.3(b) | 5.3(a) and 5.3(b) |
| Edited book | 5.3.5 | 5.3.5 |
| Journal article | 5.5 | 5.5 |
| Chapter in a book | 5.3.11 | 5.3.11 |
| Conference paper | 5.6 | 5.6 |
| Thesis | 5.12.1 | 5.12.1 |
| Legislation / public document | 5.4(a)(i) | 5.4(a)(i) |
| Magazine article | 5.7 | 5.7 |
| Technical report | 5.12.4 | 5.12.3 |
| Manuscript with no date | 5.12.2 | 5.12.2 |
| Webpage | 5.13 | 5.13 |
| Newspaper | 5.8 and 5.9 | 5.8 and 5.9 |
| General newspaper reference | 5.10 | 5.10 |
| Software manual | 5.12.7 | 5.12.6 |
| Software | 5.12.8 | 5.12.7 |
| Single-spaced references and hanging indent | 5.1 and 5.3 | 5.1 and 5.3 |

## Citation workflow constraints

- A single CSL citation layout cannot emit `and`/`dan` for narrative citations and `&` for parenthetical citations. Narrative authors are therefore typed in prose and the citation is inserted with its author suppressed.
- The style always emits the year. Omission after the first mention in a paragraph is a manual prose workflow.
- CSL cannot detect a leading A, An, or The when sorting authorless titles. Zotero's **Short Title** field provides the sortable form.
- CSL cannot set the guide's exact 12.5 mm hanging-indent width. The style requests a hanging indent; the word-processor bibliography style must set the exact width.

## Deliberate normalisations

- Page ranges are rendered with the CSL processor's typographic en dash rather than the manual's typed hyphen.
- Italics are asserted separately from the plain-text snapshots because a plain rendering intentionally drops font styling. Rich-text italics already present in imported metadata are preserved.
- The language-specific three-author rules are kept separate rather than normalised to one rule.
- Title capitalisation is taken from Zotero metadata. The styles do not change it automatically, which avoids incorrectly capitalising Malay prepositions such as `di` and `dan`.
- For non-book source examples whose titles are upright in the PDFs, the title stays upright even though the generic instruction in section 5.1.4 says titles should be italicized.
- Line breaks and spaces around page ranges are normalised. The official source check verifies each reference excerpt against the corresponding PDF after whitespace and dash normalisation.
- The English conference examples in the official guide use `hlm.` for proceedings pages, so the English style follows that guide-specific wording rather than replacing it with `pp.`.

The citation-only fixtures use a minimal article or book record so the exact author combination can be tested. Their invented titles and journal names are not asserted as official UKM reference examples.

The Hamzah Fansuri manuscript is also the no-date fixture: it exercises the `t.th.` and `n.d.` behavior while preserving the official manuscript identifier.

The GayaUKM LaTeX template maintained at `https://github.com/mohdhairimohdzaman/GayaUKM` is used as an independent cross-check for the shared author-date, no-comma, italic-title, and place-publisher behavior. It is not treated as overriding the 2015 guides where their wording differs.

The optional `tests/official/check_official_sources.py` integration check verifies that every line in `*-official-excerpts.txt` appears in the corresponding SHA-256-pinned UKM PDF.
