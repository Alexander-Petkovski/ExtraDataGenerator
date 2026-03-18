# ExtraDataGenerator

> **Instantly generate messy, realistic test data so you can prove your data pipeline actually works.**

---

## The Problem

When you build anything that processes data a cleaning tool, an import pipeline, a report generator, a machine learning model, you need to test it against realistic data. Specifically, **you need data with real problems in it.**

The question is: where do you get that data?

- **Use real data?** It might be private, sensitive, or under an NDA. You can't share it with teammates or put it in a test suite.
- **Make it up manually?** You'd spend an hour building a spreadsheet with 20 rows. Then you need 500 rows. Then a colleague needs a slightly different version. Then someone needs an Excel version. Then you need to reproduce it six months later.
- **Use random data generators?** They give you clean, perfect data. Real data is never clean or perfect. A pipeline that only works on perfect data is not a production-ready pipeline. Maybe you just need the most broken data you can find.

**ExtraDataGenerator solves this.** In seconds, it produces a file with hundreds of rows, realistic-looking content, and exactly the kind of data quality problems you'd encounter in the real world, encoding issues, null variants, formatting inconsistencies, currency symbols, broken numbers, hidden rows, and more. And because it's seeded, you get the **exact same file every time** you run it with the same settings, which means you can use it in automated tests.

---

## What It Does

ExtraDataGenerator produces CSV and Excel files loaded with configurable data problems. Every problem it can inject corresponds directly to a real cleaning operation — specifically the ones handled by [ExtraDataCleaner](https://github.com/Alexander-Petkovski/ExtraDataCleaner), its companion tool.

| What gets injected | What it tests |
|---|---|
| UTF-8 BOM character at start of file | Encoding / BOM stripping |
| Junk title row above the real header | Header row auto-detection |
| Randomly scattered blank rows | Empty row removal |
| Fully empty columns | Empty column removal |
| `N/A`, `NULL`, `none`, `missing`, `--` mixed in | Null unification |
| EU decimal format: `1.234,56` | Decimal-comma normalisation |
| Currency symbols: `£1,234.56`, `$99.00` | Currency stripping |
| Accounting negatives: `(500.00)` | Paren-to-negative conversion |
| Percentage suffix: `75.0%` | Percentage-to-numeric conversion |
| Excel errors: `#VALUE!`, `#REF!`, `#DIV/0!` | Error string replacement |
| Mixed booleans: `yes` / `Y` / `1` / `on` | Boolean normalisation |
| Leading and trailing spaces in cells | Whitespace stripping |
| Mixed-case headers: `FIRST NAME`, `fIrSt NaMe` | snake_case conversion |
| Numbers stored as text strings | Numeric coercion |
| Duplicate column header | Header de-duplication |
| Merged cells *(Excel only)* | Merged cell forward-fill |
| Hidden rows and columns *(Excel only)* | Hidden row/col detection |

**You pick which problems to include.** Need to test just your null-handling? Untick everything else. Need a completely clean baseline to compare against? Hit **None**. Need everything at once? Hit **All**.

---

## Download

**→ [Download ExtraDataGenerator.exe](../../releases/latest)** — double-click to run, no installation needed.

Runs on Windows. No Python. No setup.

---

## How to Use

### The easy way (GUI)

1. Double-click `ExtraDataGenerator.exe`
2. Set **Rows** (how many data rows you want) and **Seed** (any number — same seed always produces the same file)
3. Choose an **Output folder** and **filename**
4. Pick **CSV**, **Excel**, or **Both**
5. Tick which **Column Types** to include (names, email, dates, numbers, booleans, etc.)
6. Tick which **Issues** to inject — or use a preset:
   - **All** — inject every problem
   - **None** — produce clean data (useful as a baseline for comparison)
   - **CSV Safe** — all issues except Excel-only ones
7. Click **Generate Data**

### The power way (command line)

```bash
# 100-row CSV, all issues, seed 42
ExtraDataGenerator.exe --rows 100 --seed 42 --out ./output --format csv

# 500-row Excel file with only name, email, and currency columns
ExtraDataGenerator.exe --rows 500 --seed 7 --format xlsx \
  --cols first_name,last_name,email,currency

# Generate both CSV and Excel at once
ExtraDataGenerator.exe --rows 200 --out ./output --format both

# Turn off specific issues
ExtraDataGenerator.exe --rows 100 --no-bom --no-merged-cells

# Preview what would be generated without writing any files
ExtraDataGenerator.exe --rows 50 --preview
```

### All command-line options

| Option | Default | Description |
|---|---|---|
| `--rows N` | `100` | How many data rows to generate |
| `--seed N` | `42` | Random seed — same seed = identical output every run |
| `--out DIR` | `.` | Output directory |
| `--filename NAME` | `test_data` | Output filename (without extension) |
| `--format` | `csv` | `csv` / `xlsx` / `both` |
| `--cols TYPES` | all | Comma-separated list of column types to include |
| `--no-<issue>` | — | Disable a specific issue (e.g. `--no-bom`, `--no-null-variants`) |

**Available column types:** `first_name` · `last_name` · `email` · `phone` · `date` · `integer` · `float` · `currency` · `percentage` · `boolean` · `category` · `status` · `text`

**Disableable issues:** `bom` · `title-row` · `blank-rows` · `blank-cols` · `null-variants` · `eu-decimal` · `currency-symbols` · `accounting-neg` · `percentages` · `excel-errors` · `mixed-booleans` · `extra-whitespace` · `mixed-case-headers` · `numbers-as-text` · `duplicate-col` · `merged-cells` · `hidden-rows-cols`

---

## Why Reproducibility Matters

The seed is what makes this tool useful for testing rather than just demos. Set a seed and it becomes a fixture — something you can rely on.

```python
from core_gen import DataGenerator
from pathlib import Path

# This produces the exact same file every single time
gen = DataGenerator(seed=42)
gen.generate(
    rows=100,
    col_types=["first_name", "last_name", "email", "currency", "boolean"],
    issues={"null_variants": True, "currency_symbols": True, "mixed_booleans": True},
    fmt="csv",
    out_path=Path("./test_fixtures"),
    filename="regression_test_001",
)
```

Run this in your CI pipeline. Run ExtraDataCleaner on the output. Assert the result matches a known-good snapshot. If someone breaks the cleaning logic, the test fails.

---

## Building from Source

Requires Python 3.10+ and Windows.

```
build_exe.bat
```

Finds Python automatically, installs all dependencies, generates the icon, and produces a standalone `ExtraDataGenerator.exe`.

**Dependencies:**

| Package | Why it's needed |
|---|---|
| `pandas` | DataFrame construction and CSV/Excel export |
| `numpy` | Fast vectorised random data generation |
| `openpyxl` | Excel output with merged cells and hidden rows |

---

## Project Structure

```
ExtraDataGenerator/
├── generator.py          # Entry point, GUI if no args, CLI otherwise
├── core_gen.py           # DataGenerator class, all generation and injection logic
├── gui_gen.py            # Desktop GUI (Windows classic theme, matches ExtraDataCleaner)
├── make_icon.py          # Generates the app icon at build time
├── build_exe.bat         # One-click .exe builder for Windows
├── ExtraDataGenerator.spec  # PyInstaller packaging config
└── requirements.txt      # Python dependencies
```

---

## Companion Tool

**ExtraDataCleaner** → [github.com/Alexander-Petkovski/ExtraDataCleaner](https://github.com/Alexander-Petkovski/ExtraDataCleaner)

The tool these test files are designed for. Generate with ExtraDataGenerator → clean with ExtraDataCleaner → compare before and after to verify every operation works correctly.

---

## License

MIT
