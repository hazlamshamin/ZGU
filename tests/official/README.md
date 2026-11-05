# Official guide provenance check

This optional integration check downloads the two official 2015 UKM PDFs, verifies their SHA-256 fingerprints, extracts their text with `pdftotext`, and verifies that every checked-in official reference excerpt occurs in the corresponding primary source.

Only whitespace, dash spacing, line-break hyphenation, spacing before punctuation, curly quotes, and a terminal period are normalised. The normalized source text must contain the complete expected reference line.

Run:

```sh
uv run python tests/official/check_official_sources.py -v
```

Pinned source hashes:

- Malay `4aa8652487c0b2eac9c08a2e496bcd4055302666086ca8aca2bdff7ca7c5b4ae`
- English `e39ed8564d99a6e40fec0e14be9adee4f1b5294a1d69b1585f94b5026ac583e1`
