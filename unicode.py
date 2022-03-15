#!/usr/bin/env python

# The result of `supplement_range()` shows that
# every subset of `unicode.json` has about 138 ~ 189 chars.
# So I group every 200 chars of missing cjk into a new subset,
# which prefixed with `ex`.

import json


def supplement_range(unicode_range: str):
    """Returns supplemented range.

    Parameters:
        unicode_range (str): string looks like `U+1f1f7-1f1ff, U+1f21a`,
        some items use `-` to omit middle characters

    Returns:
        List of supplemented characters
    """

    range_list = unicode_range.split(",")
    range_list = [r.strip()[2:] for r in range_list]

    result = ["U+" + i for i in range_list if "-" not in i]

    for u in [i for i in range_list if "-" in i]:
        chars = u.split("-")
        c0 = int(chars[0], base=16)
        if len(chars[0]) > len(chars[1]):
            diff = len(chars[0]) - len(chars[1])
            chars[1] = chars[0][:diff] + chars[1]
        c1 = int(chars[1], base=16)
        t_list = ["U+" + hex(j)[2:] for j in range(c0, c1 + 1)]
        result += t_list

    return result


def get_missing_cjk():
    """Get missing characters in `U+4e00 ~ U+9fff`.

    Returns:
        sorted list of cjk characters.
    """

    cjk_dict = {hex(i).replace("0x", "U+"): 0 for i in range(0x4E00, 0x9FFF + 1)}

    with open("unicode.json") as f:
        range_dict = json.load(f)
        for subset, unicode_range in range_dict.items():
            sr = supplement_range(unicode_range)
            for i in sr:
                if i in cjk_dict:
                    cjk_dict[i] = 1
    missing = sorted([k for k, v in cjk_dict.items() if v == 0])
    return missing


def make_ex_json():
    """Make extended json from `missing_cjk`

    Returns:
        json file for missing cjk characters
    """

    missing_cjk = get_missing_cjk()
    missing_dict = {}
    range_num = 200
    count = 0
    while count * range_num < len(missing_cjk):
        _cjk = missing_cjk[count * range_num : (count + 1) * range_num]
        missing_dict[f"ex{count}"] = ", ".join(_cjk)
        count += 1

    with open("unicode_ex.json", "w") as outfile:
        json.dump(missing_dict, outfile, indent=2)


if __name__ == "__main__":
    make_ex_json()
