#!/usr/bin/env python
import json
import os
from datetime import datetime
from multiprocessing import Pool
from pathlib import Path

from fontTools.subset import main


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

BASE_UNICODE = "unicode.json"

EXTEND_CJK = "unicode_ex.json"

EXTEND_LATIN = "unicode_latin.json"


def get_unicode_range(all_subset: bool):
    """Read unicode range from `.json` file.

    Parameters:
        all_subset: dealing with just `unicode_ex.json` or not

    Returns:
        tuple of css_range and task_range
    """

    css_range = {}
    task_range = {}
    with open(BASE_UNICODE) as f1, open(EXTEND_CJK) as f2, open(EXTEND_LATIN) as f3:
        r1 = json.load(f1)
        r2 = json.load(f2)
        r3 = json.load(f3)
        css_range = {**r1, **r2, **r3}
        task_range = css_range if all_subset else {**r2, **r3}
    return css_range, task_range


def get_font_face(font_name: str, part: str, unicode: str, subset_filename: str):
    """Format @font-face string.

    Parameters:
        font_name: Font name
        part: subset part
        unicode: unicode range of the part
        subset_filename: woff2 filename of the subset

    Returns:

        css string of @font-face.
    """

    return f"""/* {font_name} [{part}] */
@font-face {{
    font-family: '{font_name.split("-")[0]}';
    font-style: normal;
    font-weight: 300;
    font-display: swap;
    src: url('./woff2/{subset_filename}') format('woff2');
    unicode-range: {unicode}
}}
"""


def build_package(ttf: str, all_subset: bool = False):
    """Build woff2 package with its css file.

    Parameters:
        ttf: ttf filename
        all_subset: dealing with just `unicode_ex.json` or not
    """

    font_name = ttf.replace(".ttf", "")

    dist_dir = os.path.join(ROOT_DIR, "dist")
    woff2_dir = os.path.join(dist_dir, "woff2")
    Path(woff2_dir).mkdir(parents=True, exist_ok=True)

    css_filename = f"{font_name.lower()}.css"

    css_range, task_range = get_unicode_range(all_subset)
    tasks = []
    css_list = [f"/* Last update: {datetime.now()} */\n\n"]

    for part, unicode in css_range.items():
        subset_filename = f"{font_name.lower()}-subset-{part}.woff2"
        output_filename = os.path.join(woff2_dir, subset_filename)

        css_list.append(get_font_face(font_name, part, unicode, subset_filename))

        if part in task_range:
            args = [
                ttf,
                f"--output-file={output_filename}",
                "--flavor=woff2",
                f"--unicodes={unicode}",
                "--passthrough-tables",
            ]
            tasks.append((subset_filename, args))

    # save css file
    css_file = os.path.join(dist_dir, css_filename)
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
    import argparse

    parser = argparse.ArgumentParser(description="Build subsets of woff2 from ttf.")

    parser.add_argument(
        "ttf",
        type=str,
        help="specify ttf filename",
    )
    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="deal with all unicode_ranges",
    )
    args = parser.parse_args()

    build_package(args.ttf, args.all)
