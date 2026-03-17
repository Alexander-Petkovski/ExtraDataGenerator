# ExtraDataGenerator

**Intentionally messy test data factory — built to pair 1:1 with [ExtraDataCleaner](https://github.com/Alexander-Petkovski/ExtraDataCleaner)**

Generate reproducible CSV and Excel files loaded with real-world data quality problems: BOM prefixes, null variants, accounting negatives, EU decimals, mixed booleans, Excel errors, merged cells, hidden rows, and more. Every issue injected maps directly to a cleaning operation in ExtraDataCleaner, so you can test your pipeline end-to-end.

---

## Download

Grab the latest **ExtraDataGenerator.exe** from the [Releases](../../releases) page — no Python required.

---

## Features

| Issue Injected | Maps to ExtraDataCleaner Operation |
|---|---|
| UTF-8 BOM prefix | BOM stripping |
| Title / junk row before header | Header row auto-detection |
| Blank rows interspersed | Drop fully-empty rows |
| Fully-empty columns | Drop fully-empty columns |
| Null variants (`N/A`, `NULL`, `none`, `--`, `#N/A`…) | Null unification (30+ variants) |
| EU decimal format (`1.234,56`) | Decimal-comma normalisation |
| Currency symbols (`£1,234.56`, `$99.00`) | Currency symbol stripping |
| Accounting negatives (`(500.00)`) | Accounting paren conversion |
| Percentage suffix (`75.0%`) | Percentage → numeric |
| Excel error strings (`#VALUE!`, `#REF!`…) | Excel error replacement |
| Mixed boolean formats (`yes`/`Y`/`1`/`on`) | Boolean normalisation |
| Extra whitespace in cells | Cell whitespace stripping |
| Mixed-case column headers | snake_case conversion |
| Numbers stored as text strings | Numeric coercion |
| Duplicate column header | Header de-duplication |
| Merged cells *(Excel only)* | Merged cell forward-fill |
| Hidden rows / columns *(Excel only)* | Hidden row/col skipping |

---

## Column Types

Pick any combination of 13 column types:

`First Name` · `Last Name` · `Email` · `Phone` · `Date` · `Integer` · `Float` · `Currency` · `Percentage` · `Boolean` · `Category` · `Status` · `Notes`

---

## Usage

### GUI (double-click)

1. Set **Rows** and **Seed** (same seed + config = identical output every time)
2. Choose **Output folder** and **filename**
3. Pick **CSV**, **Excel**, or **Both**
4. Tick the column types to include
5. Tick the issues to inject — or use the presets:
   - **All** — every issue enabled
   - **None** — clean output (useful as a baseline)
   - **CSV Safe** — all issues except Excel-only ones
6. Click **Generate Data**

### CLI

```bash
# 100-row CSV with all issues, seed 42
python generator.py --rows 100 --seed 42 --out ./output --format csv

# 500-row Excel file, specific columns only
python generator.py --rows 500 --seed 7 --format xlsx \
  --cols first_name,last_name,email,integer,currency

# Both formats, no null variants injected
python generator.py --rows 200 --out ./output --format both --no-null-variants

# Preview only — print report without writing files
python generator.py --rows 50 --preview
```

### CLI flags

| Flag | Default | Description |
|---|---|---|
| `--rows N` | `100` | Number of data rows |
| `--seed N` | `42` | Random seed — same seed = identical output |
| `--out DIR` | `.` | Output directory |
| `--filename NAME` | `test_data` | Output filename (no extension) |
| `--format` | `csv` | `csv` / `xlsx` / `both` |
| `--cols TYPES` | all | Comma-separated column types to include |
| `--no-<issue>` | — | Disable a specific issue (e.g. `--no-bom`) |

**Disableable issues:** `bom` · `title-row` · `blank-rows` · `blank-cols` · `null-variants` · `eu-decimal` · `currency-symbols` · `accounting-neg` · `percentages` · `excel-errors` · `mixed-booleans` · `extra-whitespace` · `mixed-case-headers` · `numbers-as-text` · `duplicate-col` · `merged-cells` · `hidden-rows-cols`

---

## Building the .exe

Requires Python 3.10+ and Windows.

```
build_exe.bat
```

The script finds Python automatically, installs all dependencies, generates the icon, and produces `ExtraDataGenerator.exe` in the project folder. No Python needed to run the resulting exe.

**Dependencies installed by the build script:**

| Package | Purpose |
|---|---|
| `pandas` | DataFrame generation and CSV/Excel write |
| `numpy` | Vectorised random data generation |
| `openpyxl` | Excel write with merged cells, hidden rows/cols |
| `pillow` | Multi-resolution ICO generation |
| `pyinstaller` | Bundles everything into a single .exe |

---

## Project Structure

```
ExtraDataGenerator/
├── generator.py          # Entry point — GUI if no args, CLI otherwise
├── core_gen.py           # DataGenerator class — all generation + injection logic
├── gui_gen.py            # tkinter GUI (Windows 7/XP classic theme)
├── make_icon.py          # Generates icon.ico at build time
├── build_exe.bat         # One-click Windows .exe builder
├── ExtraDataGenerator.spec  # PyInstaller spec
└── requirements.txt      # Runtime dependencies
```

---

## Reproducibility

Every run with the same **seed** and **config** produces byte-for-byte identical output. This means you can:

- Commit a seed to your test suite and assert exact output
- Share a seed with a colleague and get the same file
- Regression-test ExtraDataCleaner by fixing both the seed and the issue set

```python
from core_gen import DataGenerator

gen = DataGenerator(seed=42)
result = gen.generate(
    rows=100,
    col_types=["first_name", "last_name", "email", "currency", "boolean"],
    issues={"null_variants": True, "currency_symbols": True, "mixed_booleans": True},
    fmt="csv",
    out_path=Path("./output"),
    filename="my_test",
)
print(gen.get_report())
```

---

## Companion Tool

**ExtraDataCleaner** → [github.com/Alexander-Petkovski/ExtraDataCleaner](https://github.com/Alexander-Petkovski/ExtraDataCleaner)

Generate with ExtraDataGenerator → clean with ExtraDataCleaner → compare input vs output to verify every operation.

---

## License

MIT
