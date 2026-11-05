# LaTeX cross-check

This optional integration check pins GayaUKM to commit `bbf601f30389e550ed4f69e2c2d7522ba748c116` (v1.4, `GayaUKM.cls` dated 2019-05-18).

Prerequisites:

- TeX Live with `latexmk` and `pdflatex`
- BibTeX
- Poppler `pdftotext`
- Network access to fetch the pinned `.bst` files from GitHub

Run:

```sh
uv run python tests/latex/check_latex.py -v
```

The script downloads the pinned `GayaUKM.bst` or `GayaUKM-ms.bst` into a temporary directory, compiles the checked-in minimal TeX document, compares the generated `.bbl` with the checked-in expected output, and checks that the compiled PDF uses author-date citations without a comma.

The bibliography inputs use the guide's official book, journal, chapter, thesis, webpage, three-author journal, and four-author conference examples. This keeps the LaTeX oracle independent of the synthetic citation-only fixtures.
