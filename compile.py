import glob
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

import argparse

ROOT_DIR = Path(__file__).resolve().parent
BUILD_DIR = ROOT_DIR / "build"

XELATEX = None


def find_xelatex():
    tex = os.environ.get("XELATEX")
    if tex:
        return tex
    tex = shutil.which("xelatex")
    if tex:
        return tex
    patterns = []
    if sys.platform == "win32":
        for root in ("D:\\texlive", "C:\\texlive", "C:\\Program Files\\MiKTeX"):
            patterns.append(root + "\\**\\xelatex.exe")
    elif sys.platform == "darwin":
        patterns.extend([
            "/Library/TeX/texbin/xelatex",
            "/usr/local/texlive/*/bin/*/xelatex",
            "/opt/homebrew/bin/xelatex",
        ])
    else:
        patterns.extend([
            "/usr/bin/xelatex",
            "/usr/local/bin/xelatex",
            "/usr/texbin/xelatex",
        ])
    for p in patterns:
        for m in sorted(glob.glob(p, recursive=True)):
            return m
    print("Error: xelatex not found.", file=sys.stderr)
    sys.exit(1)


def natural_key(s):
    return re.sub(r'(\d+)', lambda m: m.group(1).zfill(10), s)


def get_tex_files(directory):
    """Return list of (teacher, stem) for all .tex files under directory.

    Scans the directory's immediate subdirectories (teacher folders).
    If .tex files exist directly in `directory` (no teacher subfolder),
    they are listed with teacher="".
    """
    result = []
    # Level-1 .tex files (no teacher subfolder)
    for f in directory.glob("*.tex"):
        if f.stem.startswith("_") or f.stem.startswith("."):
            continue
        result.append(("", f.stem))
    # Level-2 .tex files (inside teacher subfolders)
    for sub in sorted(directory.iterdir(), key=lambda x: natural_key(x.name)):
        if not sub.is_dir():
            continue
        for f in sub.glob("*.tex"):
            if f.stem.startswith("_") or f.stem.startswith("."):
                continue
            result.append((sub.name, f.stem))
    result.sort(key=lambda x: natural_key(x[1]))
    return result


def get_courses(src_dir):
    courses = []
    for d in sorted(src_dir.iterdir(), key=lambda x: natural_key(x.name)):
        if not d.is_dir():
            continue
        files = get_tex_files(d)
        if files:
            courses.append((d.name, files))
    return courses


def generate_tex(courses, selected, src_type, show_solutions, toc):
    lines = [
        "% Auto-generated",
        "\\documentclass[11pt,a4paper]{ctexart}",
        "\\input{preamble.tex}",
    ]
    if show_solutions:
        lines.append("\\ShowSolutionstrue")
    lines.append("\\begin{document}")
    if toc:
        lines.append("\\tableofcontents")
        lines.append("\\clearpage")
    for ci, (cname, files) in enumerate(courses):
        if not any(c == ci for c, _ in selected):
            continue
        lines.append("\\coursesection{%s}" % cname)
        all_selected = any(c == ci and i is None for c, i in selected)
        for ji, (teacher, fn) in enumerate(files):
            if all_selected or any(c == ci and (i is None or i == ji) for c, i in selected):
                subdir = "%s/%s/%s/" % (src_type, cname, teacher) if teacher else "%s/%s/" % (src_type, cname)
                lines.append("\\subimport{%s}{%s}" % (subdir, fn))
                lines.append("\\clearpage")
    lines.append("\\end{document}")
    return "\n".join(lines) + "\n"


def compile_pdf(tex_content, output_pdf):
    temp_tex = ROOT_DIR / "__compile_temp.tex"
    temp_tex.write_text(tex_content, encoding="utf-8")
    for pattern in ("__compile_temp.*", "*.log", "*.aux", "*.out", "*.toc"):
        for p in list(BUILD_DIR.glob(pattern)):
            p.unlink(missing_ok=True)
    for _ in range(2):
        r = subprocess.run(
          [XELATEX, "-interaction=scrollmode",
            "-output-directory", str(BUILD_DIR), "__compile_temp.tex"],
            cwd=ROOT_DIR,
            capture_output=False,
        )
    pdf = BUILD_DIR / "__compile_temp.pdf"
    if not pdf.exists():
          return False
    # check log for errors even if PDF was produced
    log = BUILD_DIR / "__compile_temp.log"
    if log.exists():
        errors = [l for l in log.read_text(encoding="utf-8", errors="replace").splitlines()
                  if l.startswith("!")]
        if errors:
            print("\n*** LaTeX errors (PDF may be incomplete) ***", file=sys.stderr)
            for e in errors[:10]:
                print(e, file=sys.stderr)
            if len(errors) > 10:
                print("  ... and %d more" % (len(errors) - 10), file=sys.stderr)
    pdf.replace(output_pdf)
    for pattern in ("__compile_temp.*", "*.log", "*.aux", "*.out", "*.toc"):
        for p in list(BUILD_DIR.glob(pattern)):
            p.unlink(missing_ok=True)
    return True


def read_input(prompt, default=""):
    v = input(prompt).strip()
    return v if v else default


def open_file(path):
    try:
        if sys.platform == "win32":
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.run(["open", str(path)], check=False)
        else:
            subprocess.run(["xdg-open", str(path)], check=False)
    except Exception:
        pass


def wait_exit():
    print("Press Enter to exit...", end=" ", flush=True)
    if sys.platform == "win32":
        import msvcrt
        t0 = time.time()
        while time.time() - t0 < 5:
            if msvcrt.kbhit():
                msvcrt.getch()
                break
            time.sleep(0.1)
    else:
        import select
        try:
            select.select([sys.stdin], [], [], 5)
        except (InterruptedError, ValueError):
            pass

def _check_log(pdf_exists):
    """Print first 10 LaTeX errors from log file."""
    log = BUILD_DIR / "__compile_temp.log"
    if log.exists():
        errors = [l for l in log.read_text(encoding="utf-8", errors="replace").splitlines()
                  if l.startswith("!")]
        if errors:
            if pdf_exists:
                print("\n*** LaTeX errors (PDF may be incomplete) ***", file=sys.stderr)
            else:
                print("\n*** LaTeX errors ***", file=sys.stderr)
            for e in errors[:10]:
                print(e, file=sys.stderr)
            if len(errors) > 10:
                print("  ... and %d more" % (len(errors) - 10), file=sys.stderr)
            return False
    return True


def main():
    global XELATEX
    XELATEX = find_xelatex()
    print("Using:", XELATEX)
    print()

    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    # --- argparse ---
    parser = argparse.ArgumentParser(description="Compile course material TeX files to PDF")
    parser.add_argument("-m", "--mode", choices=["exam", "homework"], help="Source type")
    parser.add_argument("-c", "--course", type=int, nargs="*", help="Course number(s), e.g. -c 1 or -c 1 2 3")
    parser.add_argument("-f", "--file", type=str, nargs="*", help="File selector per course, e.g. -f 1.2 1.3")
    parser.add_argument("-a", "--answer", choices=["q", "s", "b"], default="b",
                        help="q=questions only, s=solutions only, b=both (default)")
    parser.add_argument("--toc", action="store_true", help="Include table of contents")
    parser.add_argument("-o", "--output", default="compiled", help="Output filename (without .pdf)")
    args = parser.parse_args()

    if args.mode:
        mode = args.mode
    else:
        mode = read_input("Mode [E/H, Enter=E]: ", "E").lower()
        mode = "homework" if mode == "h" else "exam"
    src_type = "homework" if mode == "h" else "exam"
    src_dir = ROOT_DIR / src_type

    if not src_dir.is_dir():
        print("Error: %s directory not found." % src_type, file=sys.stderr)
        if not args.mode:
            input("Press Enter to exit")
        sys.exit(1)

    courses = get_courses(src_dir)
    if not courses:
        print("Error: no tex files found.", file=sys.stderr)
        if not args.mode:
            input("Press Enter to exit")
        sys.exit(1)

    if args.answer:
        show_sol = args.answer in ("s", "b")
        both = args.answer == "b"
    else:
        ans = read_input("Answer mode [q/s/b, Enter=b]: ", "b").lower()
        show_sol = ans in ("s", "b")
        both = ans == "b"

    for i, (cname, files) in enumerate(courses, 1):
        print("  %d. %s" % (i, cname))
        for j, (teacher, fn) in enumerate(files, 1):
            label = ("%s/%s" % (teacher, fn)) if teacher else fn
            print("      %d.%d %s" % (i, j, label))

    if args.course or args.file:
        selected = []
        if args.course:
            for c in args.course:
                selected.append((c - 1, None))
        if args.file:
            for f in args.file:
                m = re.match(r"^(\d+)\.(\d+)$", f)
                if m:
                    selected.append((int(m.group(1)) - 1, int(m.group(2)) - 1))
        if not selected:
            print("Error: no valid selection.", file=sys.stderr)
            sys.exit(1)
    else:
        while True:
            sel_raw = input("Selection (e.g. 5 or 4,5.2): ").strip()
            if not sel_raw:
                print("Invalid input, try again.")
                continue
            parts = [p.strip() for p in sel_raw.split(",")]
            selected = []
            valid = True
            for p in parts:
                m = re.match(r"^(\d+)\.(\d+)$", p)
                if m:
                    ci = int(m.group(1)) - 1
                    fi = int(m.group(2)) - 1
                    if 0 <= ci < len(courses) and 0 <= fi < len(courses[ci][1]):
                        selected.append((ci, fi))
                    else:
                        valid = False
                        break
                elif re.match(r"^\d+$", p):
                    ci = int(p) - 1
                    if 0 <= ci < len(courses):
                        selected.append((ci, None))
                    else:
                        valid = False
                        break
                else:
                    valid = False
                    break
            if valid and selected:
                break
            print("Invalid input, try again.")

    if args.mode:
        toc = args.toc
        out_name = args.output
    else:
        if args.toc:
            toc = True
        else:
            toc = read_input("Table of contents [y/n, Enter=n]: ", "n").lower().startswith("y")
        out_name = read_input("Output filename [Enter=compiled]: ", "compiled")
    if out_name.endswith(".pdf"):
        out_name = out_name[:-4]

    if both:
        jobs = [(False, "questions", "-questions"), (True, "solutions", "-solutions")]
    else:
        jobs = [(show_sol, "solutions" if show_sol else "questions", "")]

    outputs = []
    main_tex = None

    for sol, label, suffix in jobs:
        print("Compiling %s..." % label, end=" ", flush=True)
        tex = generate_tex(courses, selected, src_type, sol, toc)
        pdf = BUILD_DIR / ("%s%s.pdf" % (out_name, suffix))
        if compile_pdf(tex, pdf):
            print("OK")
            outputs.append(pdf)
        else:
            print("FAILED")
        if main_tex is None:
            main_tex = tex

    if main_tex is not None:
        (ROOT_DIR / "main.tex").write_text(main_tex, encoding="utf-8")

    temp_tex = ROOT_DIR / "__compile_temp.tex"
    if temp_tex.exists():
        temp_tex.unlink()

    if outputs:
        print()
        print("Compilation successful!")
        for f in outputs:
            print("  %s" % f)
        open_file(outputs[0])
    else:
        print("Compilation failed.", file=sys.stderr)
        _check_log(False)

    wait_exit()


if __name__ == "__main__":
    main()
