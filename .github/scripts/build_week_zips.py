#!/usr/bin/env python3
"""Build one ZIP per weeks/ folder for students who do not use git.

    week07-Silver-Layer-Cleaning-and-Conforming.zip
    └── <repo>-week07-Silver-Layer-Cleaning-and-Conforming/
        └── weeks/
            ├── week07-Silver-Layer-Cleaning-and-Conforming/      ← the week folder (with labs/ once released)
            └── week06-Bronze-and-Silver-Cleaning/pizza_sales_medallion/data/
                                                                  ← other-week data this week's notebooks/labs read

Each ZIP keeps the repository's own layout, so every relative path (../../week06-…/…) works unchanged.
The other-week paths are found by scanning the week's .py and .sql files for ../weekNN-… / ../bonus-… /
../PROJECT references (repeated for the files they pull in). Markdown links are not scanned, so a
"next week" link never pulls in a whole week.

Only git-tracked files are zipped (git ls-files), on GitHub Actions and on your own machine, so gitignored
files (answer keys, CLAUDE.md, *.duckdb) never go into a ZIP.

Usage (from the repo root):  python3 .github/scripts/build_week_zips.py [output_dir] [--prefix NAME]
  output_dir  default: dist
  --prefix    top-folder prefix; default: the course code for the repository (COURSE_CODE below), else the repository name
"""
import argparse
import os
import posixpath
import re
import subprocess
import sys
import zipfile

SKIP = re.compile(r"(^|/)(\.DS_Store|__pycache__|__marimo__)(/|$)")
COURSE_CODE = {"data-warehousing": "MSIS-2419"}   # repository name -> course code (OMIS-113's repo is already named OMIS-113)
REF = re.compile(r"((?:\.\./)+)((?:week\d\d|bonus)-[A-Za-z0-9_.-]+|PROJECT)((?:/[^\s'\"()\[\]`<>|,;*?{}]+)*)")


def tracked_files():
    try:
        out = subprocess.run(["git", "ls-files", "-z"], check=True, capture_output=True).stdout.decode()
        return sorted(f for f in out.split("\0") if f and os.path.isfile(f))
    except (subprocess.CalledProcessError, FileNotFoundError):     # not a git checkout: every file on disk
        return sorted(os.path.relpath(os.path.join(b, f)).replace(os.sep, "/")
                      for b, _, fs in os.walk(".") if "/.git" not in b + "/" for f in fs)


def repo_name():
    if os.environ.get("GITHUB_REPOSITORY"):
        return os.environ["GITHUB_REPOSITORY"].split("/")[-1]
    try:
        url = subprocess.run(["git", "remote", "get-url", "origin"], check=True, capture_output=True, text=True).stdout.strip()
        return re.sub(r"\.git$", "", url.rstrip("/").split("/")[-1])
    except (subprocess.CalledProcessError, FileNotFoundError):
        return os.path.basename(os.getcwd())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out", nargs="?", default="dist")
    ap.add_argument("--prefix", default=None)
    args = ap.parse_args()
    prefix = args.prefix or COURSE_CODE.get(repo_name(), repo_name())
    os.makedirs(args.out, exist_ok=True)

    files = [f for f in tracked_files() if not SKIP.search(f)]
    fileset = set(files)
    dirs = {posixpath.dirname(f) for f in files}
    while "" in dirs:
        dirs.discard("")
    for f in list(dirs):                                  # every ancestor folder counts as existing
        while f:
            dirs.add(f)
            f = posixpath.dirname(f)
    folders = sorted({f.split("/")[1] for f in files if f.startswith("weeks/") and f.count("/") >= 2})

    def under(path):
        return [f for f in files if f == path or f.startswith(path + "/")]

    for folder in folders:
        top = f"weeks/{folder}"
        chosen = set(under(top))
        extra, todo, seen = set(), list(chosen), set()
        while todo:
            f = todo.pop()
            if f in seen or not f.endswith((".py", ".sql")):
                continue
            seen.add(f)
            try:
                text = open(f, encoding="utf-8", errors="ignore").read()
            except OSError:
                continue
            for m in REF.finditer(text):
                p = posixpath.normpath(posixpath.join(posixpath.dirname(f), m.group(1) + m.group(2) + (m.group(3) or "")))
                while p and p not in fileset and p not in dirs:     # glob tails like orders_201*.csv: back up to an existing folder
                    p = posixpath.dirname(p)
                parts = p.split("/")
                if len(parts) < 3 or parts[0] != "weeks" or parts[1] == folder:
                    continue                                        # not another week's sub-path (a whole week is never pulled in)
                if p not in extra:
                    extra.add(p)
                    new = set(under(p)) - chosen
                    chosen |= new
                    todo.extend(new)
        zpath = os.path.join(args.out, f"{folder}.zip")
        if os.path.exists(zpath):
            os.remove(zpath)
        root = f"{prefix}-{folder}"
        with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(chosen):
                z.write(f, f"{root}/{f}")
        size = os.path.getsize(zpath) / 1e6
        note = ("  + " + ", ".join(sorted(e[len('weeks/'):] for e in extra))) if extra else ""
        print(f"built {folder}.zip  ({len(chosen)} files, {size:.1f} MB){note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
