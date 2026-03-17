"""
ExtraDataGenerator — gui_gen.py
================================
Windows 7 / XP classic themed GUI — identical palette to ExtraDataCleaner.
"""

from __future__ import annotations

import random
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

_HERE = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).parent
sys.path.insert(0, str(_HERE))

from core_gen import DataGenerator, COLUMN_TYPES, ISSUE_LABELS   # noqa: E402


# ── Windows 7 / XP Classic colour palette (identical to ExtraDataCleaner) ─────
BG       = "#F0F0F0"
PANEL    = "#FFFFFF"
HDR_TOP  = "#1B5EA6"
HDR_BOT  = "#2878CE"
BORDER   = "#ABABAB"
BTN      = "#E1E1E1"
BTN_H    = "#E8F4FF"
BTN_P    = "#2B6CB0"
BTN_PH   = "#1A4F8A"
FG       = "#000000"
FG_DIM   = "#6D6D6D"
FG_HEAD  = "#FFFFFF"
SUCCESS  = "#1A7524"
WARNING  = "#8B5E00"
ERROR    = "#C0392B"
LOG_BG   = "#FFFFFF"
LOG_FG   = "#000000"
FONT     = ("Tahoma", 9)
FONT_B   = ("Tahoma", 9, "bold")
FONT_H   = ("Tahoma", 11, "bold")
MONO     = ("Courier New", 8)


# ── widget helpers (identical to ExtraDataCleaner) ────────────────────────────

class _Btn(tk.Button):
    def __init__(self, parent, text, cmd, primary=False, small=False, **kw):
        self._bg_up   = BTN_P if primary else BTN
        self._bg_down = BTN_PH if primary else BTN_H
        self._fg      = FG_HEAD if primary else FG
        super().__init__(
            parent, text=text, command=cmd,
            bg=self._bg_up, fg=self._fg,
            activebackground=self._bg_down, activeforeground=self._fg,
            relief="raised", bd=1, cursor="hand2",
            font=(FONT[0], 8 if small else 9),
            padx=4 if small else 10, pady=2 if small else 4,
            **kw,
        )
        self.bind("<Enter>", lambda e: self.config(bg=self._bg_down))
        self.bind("<Leave>", lambda e: self.config(bg=self._bg_up))


def _sep(parent):
    return tk.Frame(parent, bg=BORDER, height=1)


def _cb(parent, text, default=True):
    var = tk.BooleanVar(value=default)
    tk.Checkbutton(
        parent, text=text, variable=var,
        bg=BG, fg=FG, activebackground=BG, activeforeground=FG,
        selectcolor=BG, font=FONT,
    ).pack(anchor="w", pady=1)
    return var


def _entry(parent, var, width=12):
    return tk.Entry(
        parent, textvariable=var, bg=PANEL, fg=FG,
        font=FONT, relief="sunken", bd=1, width=width,
        insertbackground=FG,
    )


# ── main window ───────────────────────────────────────────────────────────────

class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("ExtraDataGenerator")
        self.configure(bg=BG)
        self.resizable(True, True)
        self.minsize(720, 700)
        self._build_ui()
        self._center()
        self._load_icon()

    def _load_icon(self):
        ico = _HERE / "icon.ico"
        try:
            if ico.exists():
                self.iconbitmap(str(ico))
        except Exception:
            pass

    # ── UI builder ────────────────────────────────────────────────────────────

    def _build_ui(self):

        # ── blue title bar ────────────────────────────────────────────────────
        hbar = tk.Frame(self, bg=HDR_TOP, height=44)
        hbar.pack(fill="x")
        hbar.pack_propagate(False)
        tk.Frame(hbar, bg=HDR_BOT, height=2).pack(fill="x", side="bottom")
        inner = tk.Frame(hbar, bg=HDR_TOP)
        inner.pack(fill="both", expand=True, padx=12)
        tk.Label(inner, text="ExtraDataGenerator",
                 bg=HDR_TOP, fg=FG_HEAD, font=FONT_H).pack(side="left", pady=10)
        tk.Label(inner, text="   Test data generator",
                 bg=HDR_TOP, fg="#9FC8EF", font=FONT).pack(side="left", pady=10)

        _sep(self).pack(fill="x")

        # ── top two-column row: data size (left) + output settings (right) ────
        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", padx=10, pady=(8, 4))
        top.columnconfigure(0, weight=1)
        top.columnconfigure(1, weight=1)

        # left — data size & seed
        lf = tk.LabelFrame(top, text=" Data Size ",
                           bg=BG, fg=FG, font=FONT_B, bd=1, relief="groove",
                           padx=8, pady=6)
        lf.grid(row=0, column=0, sticky="nsew", padx=(0, 4))
        lf.columnconfigure(1, weight=1)

        def _lbl_row(parent, r, label, widget_fn):
            tk.Label(parent, text=label, bg=BG, fg=FG, font=FONT,
                     anchor="w", width=8).grid(row=r, column=0, sticky="w", pady=4)
            widget_fn(parent).grid(row=r, column=1, sticky="w", padx=(6, 0), pady=4)

        self._rows_var = tk.StringVar(value="100")
        _lbl_row(lf, 0, "Rows:", lambda p: _entry(p, self._rows_var, 8))

        # seed row with Randomise button
        seed_frame_outer = tk.Frame(lf, bg=BG)
        tk.Label(lf, text="Seed:", bg=BG, fg=FG, font=FONT,
                 anchor="w", width=8).grid(row=1, column=0, sticky="w", pady=4)
        seed_frame = tk.Frame(lf, bg=BG)
        seed_frame.grid(row=1, column=1, sticky="w", padx=(6, 0), pady=4)
        self._seed_var = tk.StringVar(value="42")
        _entry(seed_frame, self._seed_var, 6).pack(side="left")
        _Btn(seed_frame, "Randomise", self._randomise_seed, small=True).pack(
            side="left", padx=(6, 0))

        tk.Label(lf, text="Same seed + config = identical output every time.",
                 bg=BG, fg=FG_DIM, font=(FONT[0], 8)).grid(
            row=2, column=0, columnspan=3, sticky="w", pady=(2, 0))

        # right — output settings
        rf = tk.LabelFrame(top, text=" Output Settings ",
                           bg=BG, fg=FG, font=FONT_B, bd=1, relief="groove",
                           padx=8, pady=6)
        rf.grid(row=0, column=1, sticky="nsew", padx=(4, 0))
        rf.columnconfigure(1, weight=1)

        def _out_row(r, lbl, wfn, extra=None):
            tk.Label(rf, text=lbl, bg=BG, fg=FG, font=FONT,
                     anchor="w", width=14).grid(row=r, column=0, sticky="w", pady=3)
            wfn(rf).grid(row=r, column=1, sticky="ew", padx=(4, 0), pady=3)
            if extra:
                extra(rf).grid(row=r, column=2, padx=(3, 0), pady=3)

        self._outdir_var = tk.StringVar(value="")
        _out_row(0, "Output folder:", lambda p: _entry(p, self._outdir_var, 16),
                 extra=lambda p: _Btn(p, "...", self._browse_outdir, small=True))

        self._fname_var = tk.StringVar(value="test_data")
        _out_row(1, "Filename:", lambda p: _entry(p, self._fname_var, 14))

        self._fmt_var = tk.StringVar(value="csv")
        def fmt_widget(p):
            f = tk.Frame(p, bg=BG)
            for v, l in [("csv", "CSV"), ("xlsx", "Excel"), ("both", "Both")]:
                tk.Radiobutton(f, text=l, variable=self._fmt_var, value=v,
                               bg=BG, fg=FG, activebackground=BG,
                               activeforeground=FG, selectcolor=BG,
                               font=FONT).pack(side="left", padx=(0, 6))
            return f
        _out_row(2, "Format:", fmt_widget)

        # ── column types ──────────────────────────────────────────────────────
        cf = tk.LabelFrame(self, text=" Column Types  (select which columns to include) ",
                           bg=BG, fg=FG, font=FONT_B, bd=1, relief="groove",
                           padx=8, pady=6)
        cf.pack(fill="x", padx=10, pady=(0, 4))

        self._col_vars: dict[str, tk.BooleanVar] = {}
        col_labels = {
            "first_name": "First Name",
            "last_name":  "Last Name",
            "email":      "Email",
            "phone":      "Phone",
            "date":       "Date",
            "integer":    "Integer",
            "float":      "Float",
            "currency":   "Currency",
            "percentage": "Percentage",
            "boolean":    "Boolean",
            "category":   "Category",
            "status":     "Status",
            "text":       "Notes / Text",
        }
        col_keys = list(col_labels.keys())
        cols_per_row = 5
        for i, key in enumerate(col_keys):
            r, c = divmod(i, cols_per_row)
            var = tk.BooleanVar(value=True)
            tk.Checkbutton(
                cf, text=col_labels[key], variable=var,
                bg=BG, fg=FG, activebackground=BG, activeforeground=FG,
                selectcolor=BG, font=FONT,
            ).grid(row=r, column=c, sticky="w", padx=(0, 12), pady=1)
            self._col_vars[key] = var

        # select all / none buttons
        btn_row_cf = tk.Frame(cf, bg=BG)
        btn_row_cf.grid(row=(len(col_keys) // cols_per_row) + 1, column=0,
                        columnspan=cols_per_row, sticky="w", pady=(4, 0))
        _Btn(btn_row_cf, "All",  lambda: self._col_set(True),  small=True).pack(side="left", padx=(0,4))
        _Btn(btn_row_cf, "None", lambda: self._col_set(False), small=True).pack(side="left")

        # ── issues to introduce ───────────────────────────────────────────────
        isf = tk.LabelFrame(self,
                            text=" Issues to Introduce  (each maps to an ExtraDataCleaner operation) ",
                            bg=BG, fg=FG, font=FONT_B, bd=1, relief="groove",
                            padx=8, pady=6)
        isf.pack(fill="x", padx=10, pady=(0, 4))

        self._issue_vars: dict[str, tk.BooleanVar] = {}
        issue_keys  = list(ISSUE_LABELS.keys())
        iss_per_row = 2
        for i, key in enumerate(issue_keys):
            r, c = divmod(i, iss_per_row)
            var = tk.BooleanVar(value=True)
            tk.Checkbutton(
                isf, text=ISSUE_LABELS[key], variable=var,
                bg=BG, fg=FG, activebackground=BG, activeforeground=FG,
                selectcolor=BG, font=FONT,
            ).grid(row=r, column=c, sticky="w", padx=(0, 20), pady=1)
            self._issue_vars[key] = var

        # all / none / csv-safe buttons
        btn_row_isf = tk.Frame(isf, bg=BG)
        btn_row_isf.grid(row=(len(issue_keys) // iss_per_row) + 1, column=0,
                         columnspan=iss_per_row, sticky="w", pady=(6, 0))
        _Btn(btn_row_isf, "All",      lambda: self._issue_set(True),      small=True).pack(side="left", padx=(0,4))
        _Btn(btn_row_isf, "None",     lambda: self._issue_set(False),     small=True).pack(side="left", padx=(0,4))
        _Btn(btn_row_isf, "CSV Safe", lambda: self._issue_set_csv_safe(), small=True).pack(side="left", padx=(0,4))
        tk.Label(btn_row_isf,
                 text="  ← CSV Safe disables Excel-only options",
                 bg=BG, fg=FG_DIM, font=(FONT[0], 8)).pack(side="left")

        # ── action bar ────────────────────────────────────────────────────────
        _sep(self).pack(fill="x", pady=(4, 0))
        act = tk.Frame(self, bg=BG, pady=6)
        act.pack(fill="x", padx=10)
        self._gen_btn = _Btn(act, "  Generate Data  ", self._run, primary=True)
        self._gen_btn.pack(side="left")
        self._preview_var = tk.BooleanVar(value=False)
        tk.Checkbutton(act, text="Preview only  (no files written)",
                       variable=self._preview_var,
                       bg=BG, fg=FG_DIM, selectcolor=BG,
                       activebackground=BG, activeforeground=FG,
                       font=FONT).pack(side="left", padx=14)

        # ── log area ──────────────────────────────────────────────────────────
        _sep(self).pack(fill="x")
        log_outer = tk.Frame(self, bg=BG)
        log_outer.pack(fill="both", expand=True, padx=10, pady=(4, 0))

        lh = tk.Frame(log_outer, bg=BG)
        lh.pack(fill="x")
        tk.Label(lh, text="Generation Report",
                 bg=BG, fg=FG, font=FONT_B).pack(side="left")
        _Btn(lh, "Clear", self._clear_log, small=True).pack(side="right")

        log_wrap = tk.Frame(log_outer, bg=BORDER, bd=1, relief="sunken")
        log_wrap.pack(fill="both", expand=True, pady=(4, 0))
        self._log = tk.Text(
            log_wrap, bg=LOG_BG, fg=LOG_FG, font=MONO,
            relief="flat", bd=3, wrap="word",
            insertbackground=FG,
            selectbackground=BTN_P, selectforeground=FG_HEAD,
        )
        sb = ttk.Scrollbar(log_wrap, command=self._log.yview)
        self._log.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self._log.pack(fill="both", expand=True)

        self._log.tag_config("ok",   foreground=SUCCESS, font=(MONO[0], MONO[1], "bold"))
        self._log.tag_config("warn", foreground=WARNING)
        self._log.tag_config("err",  foreground=ERROR,   font=(MONO[0], MONO[1], "bold"))
        self._log.tag_config("head", foreground=HDR_TOP, font=(MONO[0], MONO[1], "bold"))
        self._log.tag_config("dim",  foreground=FG_DIM)

        # ── status bar ────────────────────────────────────────────────────────
        _sep(self).pack(fill="x")
        self._status = tk.Label(
            self, text="  Ready",
            bg=BG, fg=FG_DIM, font=(FONT[0], 8),
            anchor="w", relief="sunken", bd=1,
        )
        self._status.pack(fill="x", side="bottom")

        self._log_line(
            "Ready.  Configure options and click Generate Data.", "dim"
        )

    # ── helpers ───────────────────────────────────────────────────────────────

    def _col_set(self, value: bool):
        for v in self._col_vars.values():
            v.set(value)

    def _issue_set(self, value: bool):
        for v in self._issue_vars.values():
            v.set(value)

    def _issue_set_csv_safe(self):
        """Enable all issues except Excel-only ones."""
        excel_only = {"merged_cells", "hidden_rows_cols"}
        for k, v in self._issue_vars.items():
            v.set(k not in excel_only)

    def _randomise_seed(self):
        self._seed_var.set(str(random.randint(1, 999_999)))

    def _browse_outdir(self):
        d = filedialog.askdirectory(title="Select output folder")
        if d:
            self._outdir_var.set(d)

    def _clear_log(self):
        self._log.delete("1.0", "end")

    # ── run ───────────────────────────────────────────────────────────────────

    def _run(self):
        # Validate rows
        rows_str = self._rows_var.get().strip()
        if not rows_str.isdigit() or int(rows_str) < 1:
            messagebox.showwarning("Invalid rows",
                                   "Rows must be a positive integer.")
            return

        outdir = self._outdir_var.get().strip()
        if not outdir and not self._preview_var.get():
            messagebox.showwarning("No output folder",
                                   "Please choose an output folder.")
            return

        col_types = [k for k, v in self._col_vars.items() if v.get()]
        if not col_types:
            messagebox.showwarning("No columns",
                                   "Select at least one column type.")
            return

        self._gen_btn.config(state="disabled", text="  Generating…  ")
        self._set_status("Generating data…")
        threading.Thread(target=self._worker, daemon=True).start()

    def _worker(self):
        try:
            rows      = int(self._rows_var.get().strip())
            seed_str  = self._seed_var.get().strip()
            seed      = int(seed_str) if seed_str.isdigit() else 42
            col_types = [k for k, v in self._col_vars.items() if v.get()]
            issues    = {k: v.get() for k, v in self._issue_vars.items()}
            fmt       = self._fmt_var.get()
            outdir    = self._outdir_var.get().strip()
            fname     = self._fname_var.get().strip() or "test_data"
            preview   = self._preview_var.get()

            self._log_line(f"\n{'─'*52}", "dim")
            self._log_line(
                f"Generating  {rows} rows  ·  {len(col_types)} column types"
                f"  ·  seed={seed}",
                "head",
            )

            gen = DataGenerator(seed=seed)

            if preview:
                # Build df only — no write
                from core_gen import DataGenerator as _DG
                g = _DG(seed=seed)
                import numpy as np, pandas as pd
                df = g._build_clean(rows, col_types)
                df = g._inject_issues(df, issues, col_types)
                self._log_line(
                    f"\n[Preview]  {len(df)} rows × {len(df.columns)} cols"
                    f"  (no files written)", "warn"
                )
                self._log_line(
                    "Columns: " + ", ".join(df.columns.tolist()), "dim"
                )
                for ln in g.get_report().splitlines():
                    self._log_line(ln, "ok" if "✓" in ln else "warn" if "✗" in ln else "")
            else:
                result = gen.generate(
                    rows=rows,
                    col_types=col_types,
                    issues=issues,
                    fmt=fmt,
                    out_path=Path(outdir),
                    filename=fname,
                )
                for ln in gen.get_report().splitlines():
                    tag = "ok" if "✓" in ln else ("warn" if "✗" in ln else "")
                    self._log_line(ln, tag)

            self._log_line(f"{'─'*52}", "dim")
            self._log_line("Done.", "ok")
            self._set_status("Ready")

        except Exception as exc:
            import traceback
            self._log_line(f"ERROR: {exc}", "err")
            self._log_line(traceback.format_exc(), "err")
            self._set_status("Error — see report")
        finally:
            self.after(0, lambda: self._gen_btn.config(
                state="normal", text="  Generate Data  "))

    # ── thread-safe log / status ──────────────────────────────────────────────

    def _log_line(self, msg: str, tag: str = ""):
        def _do():
            if tag:
                self._log.insert("end", msg + "\n", tag)
            else:
                self._log.insert("end", msg + "\n")
            self._log.see("end")
        self.after(0, _do)

    def _set_status(self, msg: str):
        self.after(0, lambda: self._status.config(text=f"  {msg}"))

    def _center(self):
        self.update_idletasks()
        w, h = 760, 720
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")


# ── entry point ───────────────────────────────────────────────────────────────

def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
