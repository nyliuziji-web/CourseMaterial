#!/usr/bin/env python3
import glob
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
BUILD_DIR = ROOT_DIR / "build"
EXAMPLE_DIR = ROOT_DIR / "example"

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
    input("Press Enter to exit")
    sys.exit(1)


def get_tex_files(directory):
    result = []
    for f in directory.glob("*.tex"):
        if f.stem.startswith("_") or f.stem.startswith("."):
            continue
        result.append(f.stem)
    result.sort()
    return result


def generate_tex(src_type, course_name, files, show_solutions):
    lines = [
        "% Auto-generated",
        "\\documentclass[11pt,a4paper]{ctexart}",
        "\\input{preamble.tex}",
    ]
    if show_solutions:
        lines.append("\\ShowSolutionstrue")
    lines.append("\\begin{document}")
    lines.append("\\coursesection{%s}" % course_name)
    for fn in files:
        lines.append("\\subimport{%s/%s/}{%s}" % (src_type, course_name, fn))
        lines.append("\\clearpage")
    lines.append("\\end{document}")
    return "\n".join(lines) + "\n"


def compile_pdf(tex_content, output_pdf):
    temp_tex = ROOT_DIR / "__compile_temp.tex"
    temp_tex.write_text(tex_content, encoding="utf-8")
    for p in list(BUILD_DIR.glob("__compile_temp.*")):
        p.unlink(missing_ok=True)
    for _ in range(2):
        subprocess.run(
            [XELATEX, "-interaction=nonstopmode",
             "-output-directory", str(BUILD_DIR), "__compile_temp.tex"],
            cwd=ROOT_DIR,
            capture_output=True,
        )
        if not (BUILD_DIR / "__compile_temp.pdf").exists():
            return False
    pdf = BUILD_DIR / "__compile_temp.pdf"
    pdf.replace(output_pdf)
    for p in list(BUILD_DIR.glob("__compile_temp.*")):
        p.unlink(missing_ok=True)
    return True


def main():
    global XELATEX
    XELATEX = find_xelatex()
    print("Using:", XELATEX)
    print()

    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    EXAMPLE_DIR.mkdir(parents=True, exist_ok=True)

    categories = {"exam": "往年题", "homework": "作业题"}
    total_ok = 0
    total_fail = 0

    for src_type in ("exam", "homework"):
        src_dir = ROOT_DIR / src_type
        if not src_dir.is_dir():
            continue
        category = categories[src_type]
        print(">>> Compiling %s..." % src_type)
        dirs = sorted([d for d in src_dir.iterdir() if d.is_dir()])
        for d in dirs:
            files = get_tex_files(d)
            if not files:
                continue

            tex_q = generate_tex(src_type, d.name, files, False)
            pdf_q = EXAMPLE_DIR / ("%s%s-题目.pdf" % (d.name, category))
            if compile_pdf(tex_q, pdf_q):
                print("  [%s] 题目 OK" % d.name)
                total_ok += 1
            else:
                print("  [%s] 题目 FAILED" % d.name)
                total_fail += 1

            tex_s = generate_tex(src_type, d.name, files, True)
            pdf_s = EXAMPLE_DIR / ("%s%s-解析.pdf" % (d.name, category))
            if compile_pdf(tex_s, pdf_s):
                print("  [%s] 解析 OK" % d.name)
                total_ok += 1
            else:
                print("  [%s] 解析 FAILED" % d.name)
                total_fail += 1
        print()

    print("=" * 50)
    print("  Done! Exam + Homework: %d OK, %d FAILED" % (total_ok, total_fail))
    print("=" * 50)

    temp_tex = ROOT_DIR / "__compile_temp.tex"
    if temp_tex.exists():
        temp_tex.unlink()
    input("Press Enter to exit")


if __name__ == "__main__":
    main()
