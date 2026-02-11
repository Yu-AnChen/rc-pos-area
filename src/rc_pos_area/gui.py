"""
Tkinter GUI for the Positive Area Calculator.
"""

import matplotlib
matplotlib.use("Agg")

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import threading
import queue
from pathlib import Path
from datetime import datetime
from typing import List

from rc_pos_area.processor import validate_excel_file, process_single_excel
from rc_pos_area.report import generate_summary_report


def _find_excel_files(directory: Path) -> List[Path]:
    """Find unprocessed Excel files in a directory."""
    excel_files = list(directory.glob("*.xlsx"))
    excel_files = [
        f for f in excel_files
        if not f.name.startswith("~$") and not f.name.endswith("_processed.xlsx")
    ]
    return sorted(excel_files)


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.msg_queue: queue.Queue = queue.Queue()
        self.action_buttons: list = []

        self._build_ui()
        self._poll_queue()

    # ------------------------------------------------------------------ UI
    def _build_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=(10, 5))

        self._build_single_tab()
        self._build_batch_tab()
        self._build_report_tab()
        self._build_log_area()

    def _build_single_tab(self):
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="Single")

        self.single_input = tk.StringVar()
        self.single_output = tk.StringVar(value="results")

        ttk.Label(tab, text="Input Excel:").grid(row=0, column=0, sticky="w", pady=4)
        ttk.Entry(tab, textvariable=self.single_input, width=50).grid(row=0, column=1, padx=4)
        ttk.Button(tab, text="Browse...", command=lambda: self._browse_file(self.single_input)).grid(
            row=0, column=2
        )

        ttk.Label(tab, text="Output Dir:").grid(row=1, column=0, sticky="w", pady=4)
        ttk.Entry(tab, textvariable=self.single_output, width=50).grid(row=1, column=1, padx=4)
        ttk.Button(
            tab, text="Browse...", command=lambda: self._browse_directory(self.single_output)
        ).grid(row=1, column=2)

        btn_frame = ttk.Frame(tab)
        btn_frame.grid(row=2, column=0, columnspan=3, pady=12)

        btn_validate = ttk.Button(btn_frame, text="Validate", command=self._on_validate_single)
        btn_validate.pack(side="left", padx=4)
        self.action_buttons.append(btn_validate)

        btn_process = ttk.Button(btn_frame, text="Process", command=self._on_process_single)
        btn_process.pack(side="left", padx=4)
        self.action_buttons.append(btn_process)

        tab.columnconfigure(1, weight=1)

    def _build_batch_tab(self):
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="Batch")

        self.batch_input = tk.StringVar()
        self.batch_output = tk.StringVar(value="results")
        self.batch_dry_run = tk.BooleanVar(value=False)

        ttk.Label(tab, text="Input Dir:").grid(row=0, column=0, sticky="w", pady=4)
        ttk.Entry(tab, textvariable=self.batch_input, width=50).grid(row=0, column=1, padx=4)
        ttk.Button(
            tab, text="Browse...", command=lambda: self._browse_directory(self.batch_input)
        ).grid(row=0, column=2)

        ttk.Label(tab, text="Output Dir:").grid(row=1, column=0, sticky="w", pady=4)
        ttk.Entry(tab, textvariable=self.batch_output, width=50).grid(row=1, column=1, padx=4)
        ttk.Button(
            tab, text="Browse...", command=lambda: self._browse_directory(self.batch_output)
        ).grid(row=1, column=2)

        ttk.Checkbutton(tab, text="Dry run (validate only)", variable=self.batch_dry_run).grid(
            row=2, column=0, columnspan=3, sticky="w", pady=4
        )

        btn_batch = ttk.Button(tab, text="Run Batch", command=self._on_run_batch)
        btn_batch.grid(row=3, column=0, columnspan=3, pady=12)
        self.action_buttons.append(btn_batch)

        tab.columnconfigure(1, weight=1)

    def _build_report_tab(self):
        tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(tab, text="Report")

        self.report_input = tk.StringVar()
        self.report_output = tk.StringVar()

        ttk.Label(tab, text="Processed Dir:").grid(row=0, column=0, sticky="w", pady=4)
        ttk.Entry(tab, textvariable=self.report_input, width=50).grid(row=0, column=1, padx=4)
        ttk.Button(
            tab, text="Browse...", command=lambda: self._browse_directory(self.report_input)
        ).grid(row=0, column=2)

        ttk.Label(tab, text="Output File:").grid(row=1, column=0, sticky="w", pady=4)
        ttk.Entry(tab, textvariable=self.report_output, width=50).grid(row=1, column=1, padx=4)
        ttk.Button(
            tab, text="Browse...", command=lambda: self._browse_save_file(self.report_output)
        ).grid(row=1, column=2)

        btn_report = ttk.Button(tab, text="Generate Report", command=self._on_generate_report)
        btn_report.grid(row=2, column=0, columnspan=3, pady=12)
        self.action_buttons.append(btn_report)

        tab.columnconfigure(1, weight=1)

    def _build_log_area(self):
        frame = ttk.Frame(self.root)
        frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        ttk.Label(frame, text="Status Log:").pack(anchor="w")

        self.log_text = scrolledtext.ScrolledText(frame, height=10, state="disabled", wrap="word")
        self.log_text.pack(fill="both", expand=True, pady=(2, 4))

        bottom = ttk.Frame(frame)
        bottom.pack(fill="x")

        ttk.Button(bottom, text="Clear Log", command=self._clear_log).pack(side="left")

        self.progress = ttk.Progressbar(bottom, length=200, mode="determinate")
        self.progress.pack(side="right")

    # --------------------------------------------------------- queue polling
    def _poll_queue(self):
        while True:
            try:
                msg_type, msg_data = self.msg_queue.get_nowait()
            except queue.Empty:
                break
            if msg_type == "log":
                self._append_log(msg_data)
            elif msg_type == "progress":
                current, total = msg_data
                self.progress.configure(maximum=total, value=current)
            elif msg_type == "done":
                self._append_log(msg_data)
                self.progress.stop()
                self.progress.configure(mode="determinate", value=0)
                self._set_buttons_enabled(True)
            elif msg_type == "error":
                self._append_log(f"ERROR: {msg_data}")
                self.progress.stop()
                self.progress.configure(mode="determinate", value=0)
                self._set_buttons_enabled(True)
        self.root.after(100, self._poll_queue)

    def _append_log(self, message: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"[{timestamp}] {message}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    def _clear_log(self):
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")

    def _set_buttons_enabled(self, enabled: bool):
        state = "normal" if enabled else "disabled"
        for btn in self.action_buttons:
            btn.configure(state=state)

    def _run_in_thread(self, target, *args):
        self._set_buttons_enabled(False)
        self.progress.configure(mode="indeterminate")
        self.progress.start(10)
        thread = threading.Thread(target=target, args=args, daemon=True)
        thread.start()

    # --------------------------------------------------------- file dialogs
    def _browse_file(self, var: tk.StringVar):
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if path:
            var.set(path)

    def _browse_directory(self, var: tk.StringVar):
        path = filedialog.askdirectory()
        if path:
            var.set(path)

    def _browse_save_file(self, var: tk.StringVar):
        path = filedialog.asksaveasfilename(
            defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")]
        )
        if path:
            var.set(path)

    # ---------------------------------------------------- action dispatchers
    def _on_validate_single(self):
        input_path = self.single_input.get().strip()
        if not input_path:
            self._append_log("ERROR: No input file selected.")
            return
        self._run_in_thread(self._worker_single_validate, Path(input_path))

    def _on_process_single(self):
        input_path = self.single_input.get().strip()
        output_dir = self.single_output.get().strip()
        if not input_path:
            self._append_log("ERROR: No input file selected.")
            return
        if not output_dir:
            self._append_log("ERROR: No output directory specified.")
            return
        self._run_in_thread(self._worker_single_process, Path(input_path), Path(output_dir))

    def _on_run_batch(self):
        input_dir = self.batch_input.get().strip()
        output_dir = self.batch_output.get().strip()
        if not input_dir:
            self._append_log("ERROR: No input directory selected.")
            return
        if not output_dir:
            self._append_log("ERROR: No output directory specified.")
            return
        self._run_in_thread(
            self._worker_batch, Path(input_dir), Path(output_dir), self.batch_dry_run.get()
        )

    def _on_generate_report(self):
        processed_dir = self.report_input.get().strip()
        output_file = self.report_output.get().strip()
        if not processed_dir:
            self._append_log("ERROR: No processed directory selected.")
            return
        if not output_file:
            output_file = f"Summary-{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        self._run_in_thread(self._worker_report, Path(processed_dir), Path(output_file))

    # -------------------------------------------------------- worker threads
    def _worker_single_validate(self, input_path: Path):
        try:
            self.msg_queue.put(("log", f"Validating {input_path.name}..."))
            errors = validate_excel_file(input_path)
            if errors:
                detail = "\n".join(f"  - {e}" for e in errors)
                self.msg_queue.put(("error", f"Validation failed:\n{detail}"))
            else:
                self.msg_queue.put(("done", "Validation passed."))
        except Exception as e:
            self.msg_queue.put(("error", f"Validation error: {e}"))

    def _worker_single_process(self, input_path: Path, output_dir: Path):
        try:
            self.msg_queue.put(("log", f"Validating {input_path.name}..."))
            errors = validate_excel_file(input_path)
            if errors:
                detail = "\n".join(f"  - {e}" for e in errors)
                self.msg_queue.put(("error", f"Validation failed:\n{detail}"))
                return

            self.msg_queue.put(("log", f"Processing {input_path.name}..."))
            output_file = process_single_excel(input_path, output_dir, verbose=False, quiet=True)
            self.msg_queue.put(("done", f"Successfully processed: {output_file}"))
        except Exception as e:
            self.msg_queue.put(("error", f"Processing failed: {e}"))

    def _worker_batch(self, input_dir: Path, output_dir: Path, dry_run: bool):
        try:
            if not input_dir.is_dir():
                self.msg_queue.put(("error", f"Directory not found: {input_dir}"))
                return

            excel_files = _find_excel_files(input_dir)
            if not excel_files:
                self.msg_queue.put(("error", f"No Excel files found in {input_dir}"))
                return

            total = len(excel_files)
            self.msg_queue.put(("log", f"Found {total} Excel file(s). Validating..."))

            all_valid = True
            for f in excel_files:
                errors = validate_excel_file(f)
                if errors:
                    all_valid = False
                    detail = "\n".join(f"  - {e}" for e in errors)
                    self.msg_queue.put(("log", f"FAILED: {f.name}\n{detail}"))
                else:
                    self.msg_queue.put(("log", f"OK: {f.name}"))

            if not all_valid:
                self.msg_queue.put(("error", "Validation failed. Fix errors before processing."))
                return

            self.msg_queue.put(("log", "All files passed validation."))

            if dry_run:
                self.msg_queue.put(("done", "Dry run complete. No files were processed."))
                return

            successful, failed = 0, 0
            for i, f in enumerate(excel_files, 1):
                self.msg_queue.put(("log", f"[{i}/{total}] Processing {f.name}..."))
                self.msg_queue.put(("progress", (i, total)))
                try:
                    output_file = process_single_excel(f, output_dir, verbose=False, quiet=True)
                    successful += 1
                    self.msg_queue.put(("log", f"  Created: {output_file.name}"))
                except Exception as e:
                    failed += 1
                    self.msg_queue.put(("log", f"  Failed: {e}"))

            self.msg_queue.put(("done", f"Batch complete. {successful} succeeded, {failed} failed."))
        except Exception as e:
            self.msg_queue.put(("error", str(e)))

    def _worker_report(self, processed_dir: Path, output_path: Path):
        try:
            if not processed_dir.is_dir():
                self.msg_queue.put(("error", f"Directory not found: {processed_dir}"))
                return

            processed_files = sorted(processed_dir.glob("*_processed.xlsx"))
            if not processed_files:
                self.msg_queue.put(("error", f"No processed files found in {processed_dir}"))
                return

            self.msg_queue.put(
                ("log", f"Found {len(processed_files)} processed file(s). Generating report...")
            )
            generate_summary_report(processed_files, output_path, verbose=False, quiet=True)
            self.msg_queue.put(("done", f"Report created: {output_path}"))
        except Exception as e:
            self.msg_queue.put(("error", f"Report generation failed: {e}"))


def main():
    root = tk.Tk()
    root.title("Positive Area Calculator")
    root.geometry("700x550")
    root.minsize(600, 450)
    App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
