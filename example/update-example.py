import glob
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
BUILD_DIR = ROOT_DIR / "build"
EXAMPLE_DIR = ROOT_DIR / "example"

XELATEX = None


def natural_key(s):
    return re.sub(r'(\d+)', lambda m: m.group(1).zfill(10), s)


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
    """Return list of (teacher, stem) for all .tex files under directory."""
    result = []
    for f in directory.glob("*.tex"):
        if f.stem.startswith("_") or f.stem.startswith("."):
            continue
        result.append(("", f.stem))
    for sub in sorted(directory.iterdir(), key=lambda x: natural_key(x.name)):
        if not sub.is_dir():
            continue
        for f in sub.glob("*.tex"):
            if f.stem.startswith("_") or f.stem.startswith("."):
                continue
            result.append((sub.name, f.stem))
    result.sort(key=lambda x: natural_key(x[1]))
    return result


def git_changed_files():
    """Changed file paths (vs HEAD, incl. untracked) or None if git unavailable."""
    if shutil.which("git") is None:
        return None
    files = set()
    for cmd in (
        ["git", "-c", "core.quotepath=false", "diff", "--name-only", "HEAD"],
        ["git", "-c", "core.quotepath=false", "ls-files", "--others", "--exclude-standard"],
    ):
        try:
            out = subprocess.run(cmd, cwd=ROOT_DIR, capture_output=True, text=True)
            if out.returncode != 0:
                return None
        except (OSError, subprocess.SubprocessError):
            return None
        files.update(out.stdout.splitlines())
    return files


def affected_courses(files):
    """Set of (src_type, course) changed, or None for full rebuild."""
    if files is None or "preamble.tex" in files:
        return None
    affected = set()
    for f in files:
        parts = Path(f).parts
        if len(parts) >= 2 and parts[0] in ("exam", "homework"):
            affected.add((parts[0], parts[1]))
    return affected


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
    for teacher, fn in files:
        subdir = "%s/%s/%s/" % (src_type, course_name, teacher) if teacher else "%s/%s/" % (src_type, course_name)
        lines.append("\\subimport{%s}{%s}" % (subdir, fn))
        lines.append("\\clearpage")
    lines.append("\\end{document}")
    return "\n".join(lines) + "\n"


def compile_pdf(tex_content, output_pdf):
    temp_tex = ROOT_DIR / "__compile_temp.tex"
    temp_tex.write_text(tex_content, encoding="utf-8")
    for p in list(BUILD_DIR.glob("__compile_temp.*")):
        try:
            p.unlink(missing_ok=True)
        except OSError:
            pass
    for _ in range(2):
        subprocess.run(
            [XELATEX, "-interaction=scrollmode",
             "-output-directory", str(BUILD_DIR), "__compile_temp.tex"],
            cwd=ROOT_DIR,
            capture_output=True,
        )
    pdf = BUILD_DIR / "__compile_temp.pdf"
    log = BUILD_DIR / "__compile_temp.log"
    if not pdf.exists():
        errors = []
        if log.exists():
            errors = [l for l in log.read_text(encoding="utf-8", errors="replace").splitlines()
                      if l.startswith("!")]
        print("\n*** LaTeX errors ***", file=sys.stderr)
        for e in errors[:20]:
            print(e, file=sys.stderr)
        if len(errors) > 20:
            print("  ... and %d more" % (len(errors) - 20), file=sys.stderr)
        print("PDF not generated.", file=sys.stderr)
        sys.exit(1)
    pdf.replace(output_pdf)
    for p in list(BUILD_DIR.glob("__compile_temp.*")):
        try:
            p.unlink(missing_ok=True)
        except OSError:
            pass
    return True


def main():
    global XELATEX
    XELATEX = find_xelatex()

    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    EXAMPLE_DIR.mkdir(parents=True, exist_ok=True)

    affected = affected_courses(git_changed_files())
    if affected is not None:
        if not affected:
            print("No changed courses, nothing to do.")
            return
        for src, course in sorted(affected, key=lambda x: (x[0], natural_key(x[1]))):
            print("changed: %s/%s" % (src, course))

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
            if affected is not None and (src_type, d.name) not in affected:
                continue
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


if __name__ == "__main__":
    main()
