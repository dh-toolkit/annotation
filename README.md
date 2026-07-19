# Cultural annotation of *Possession* (TEI + BaseX)

TEI passages are the classification units. Keyword search finds candidate cultural markers; annotated notes turn the closed category matrix (**time / values / customs / beliefs / postcolonialism**) into countable distributions by chapter—the quantitative step before LLM evaluation.

## Workflow overview

```
plain text
  → convert_text_to_tei.py          → *.tei.xml
  → export_passages_for_annotation  → passages CSV
  → (annotate / merge suggested)    → filled CSV
  → apply_tei_annotations.py        → *.annotated.tei.xml
  → run_annotation_reports.py       → HTML + CSV reports
  → run_basex_queries.py            → BaseX XQuery reports
  → r/frequency_cultural_concepts.R → category × chapter counts
```

Plain TEI (`Possession_A_Romance.tei.xml`) only has structure. Category values live in cultural notes:

```xml
<note type="cultural">primary=values; secondary=beliefs; markers=…; notes=…</note>
```

BaseX alone is not enough for category distributions—you need cultural `<note>`s in the TEI, then query those notes (or use the annotation reports / R script).

---

## 1. Convert text → TEI

```powershell
py convert_text_to_tei.py ".\Possession_A_Romance.txt" -o ".\Possession_A_Romance.tei.xml"
```

For the smaller excerpt used in the annotation loop:

```powershell
py convert_text_to_tei.py ".\Possession_1000.txt" -o ".\Possession_1000.tei.xml"
```

Each annotatable unit is a `<p xml:id="p…">` inside a chapter `<div>`.

---

## 2. BaseX on plain TEI

### Q1. How many passages?

XPath:

```xpath
count(//tei:body/tei:div/tei:p[@xml:id])
```

```powershell
basex -i Possession_A_Romance.tei.xml -q "declare namespace tei='http://www.tei-c.org/ns/1.0'; count(//tei:body/tei:div/tei:p[@xml:id])"
```

**Answer:** 9888

### Q2. Which passages hit cultural keywords?

Candidate markers (myth / archive / period), e.g.:

```powershell
basex -i Possession_A_Romance.tei.xml -q "declare namespace tei='http://www.tei-c.org/ns/1.0'; for `$p in //tei:body/tei:div/tei:p[@xml:id] let `$t := string-join(`$p//text(), ' ') where matches(`$t, 'myth|Proserpina|Melusina|folklore|library|archive|manuscript|letter|Vico|Victorian|1986|century|era', 'i') return concat(string(`$p/@xml:id), ' | ', string(`$p/ancestor::tei:div[1]/@type), ' ', string(`$p/ancestor::tei:div[1]/@n), ' | ', substring(normalize-space(`$t), 1, 100))"
```

This finds **candidates** only. Closed-matrix categories require annotated TEI (below).

---

## 3. Annotation pipeline (excerpt)

Target file shape: `Possession_1000.annotated.tei.xml`  
(path: convert → annotate CSV → `apply_tei_annotations.py`)

```powershell
py export_passages_for_annotation.py --tei Possession_1000.tei.xml -o possession_passages.csv --preview-chars 500

py merge_suggested_annotations.py --filled possession_annotations_filled.csv --suggested possession_annotations_suggested.csv

py apply_tei_annotations.py --tei Possession_1000.tei.xml --csv possession_annotations_filled.csv -o Possession_1000.annotated.tei.xml

py run_annotation_reports.py --tei Possession_1000.annotated.tei.xml --html-report cultural-annotations-report.html --summary category-summary.html --csv possession_annotations_from_tei.csv

py run_basex_queries.py --java-home "%LOCALAPPDATA%\Java\..." --basex-bin "%LOCALAPPDATA%\BaseX\basex\bin"
```

One-shot alternative (convert → export → apply if filled CSV exists → reports):

```powershell
py run_tei_annotation_pipeline.py
```

---

## 4. Scripts

| Script | What it does |
|--------|----------------|
| `convert_text_to_tei.py` | text → TEI |
| `export_passages_for_annotation.py` | TEI → CSV |
| `merge_suggested_annotations.py` | merge suggested labels into filled CSV |
| `apply_tei_annotations.py` | filled CSV → annotated TEI |
| `run_annotation_reports.py` | annotated TEI → HTML/CSV reports |
| `run_basex_queries.py` | run BaseX XQuery reports |
| `install_java_for_basex.py` | install Temurin JRE 21 |
| `install_basex.py` | install BaseX |
| `run_tei_annotation_pipeline.py` | full pipeline in one go |

Supporting package: `cultural_tei/` (conversion, CSV I/O, notes, reports, BaseX helpers).

Quantitative follow-up in R (category × chapter):

```powershell
Rscript r/frequency_cultural_concepts.R
```

---

## Category matrix

Closed set used in cultural notes and reports:

| Category |
|----------|
| time |
| values |
| customs |
| beliefs |
| postcolonialism |

Each annotated passage may have a **primary** and optional **secondary** category, plus free-text markers and notes.
