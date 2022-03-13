#!/usr/bin/env python
import json
import os
import sys
from multiprocessing import Pool

from fontTools.subset import main

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

TTF_FILE = os.path.join(ROOT_DIR, "LXGWWenKai-Light.ttf")

RELEASE_DIR = os.path.join(ROOT_DIR, "release")

FONT_DIR = os.path.join(RELEASE_DIR, "woff2")

FONT_FAMILY = "LXGW WenKai"

SUBSET_PREFIX = "lxgw-wenkai-light-subset"

CSS_FILENAME = "lxgw-wenkai-light.css"

BASE_UNICODE = "unicode.json"

EXTEND_UNICODE = "unicode_ex.json"


def get_unicode_range(all_subset):
    css_range = {}
    task_range = {}
    with open(BASE_UNICODE) as f1, open(EXTEND_UNICODE) as f2:
        r1 = json.load(f1)
        r2 = json.load(f2)
        css_range = {**r1, **r2}
        task_range = css_range if all_subset else r2
    return css_range, task_range


def get_font_face(part, unicode, subset_filename):
    return f"""/* {FONT_FAMILY} [{part}] */
@font-face {{
    font-family: '{FONT_FAMILY}';
    font-style: normal;
    font-weight: 300;
    font-display: swap;
    src: url('./woff2/{subset_filename}') format('woff2');
    unicode-range: {unicode}
}}
"""


def build_package(all_subset):
    css_range, task_range = get_unicode_range(all_subset)
    tasks = []
    css_list = []

    for part, unicode in css_range.items():
        subset_filename = f"{SUBSET_PREFIX}-{part}.woff2"
        output_filename = os.path.join(FONT_DIR, subset_filename)

        # subset css
        css_list.append(get_font_face(part, unicode, subset_filename))

        if part in task_range:
            args = [
                TTF_FILE,
                f"--output-file={output_filename}",
                "--flavor=woff2",
                f"--unicodes={unicode}",
                "--passthrough-tables",
            ]
            tasks.append((subset_filename, args))

    # save css file
    css_file = os.path.join(RELEASE_DIR, CSS_FILENAME)
    with open(css_file, "w", newline="\n") as f:
        f.write("".join(css_list))

    # subset fonts in parallel
    with Pool(4) as pool:
        pool.map(subset_worker, tasks)


def subset_worker(task):
    subset_filename, args = task
    print("Generating {}".format(subset_filename))
    main(args)


if __name__ == "__main__":
    arg = sys.argv[1] if sys.argv[1:] else None
    if arg in ["-a", "--all"]:
        build_package(all_subset=True)
    else:
        build_package(all_subset=False)
