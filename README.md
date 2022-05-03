[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![](https://data.jsdelivr.com/v1/package/npm/@jhintr/lxgw-wenkai-webfont/badge)](https://www.jsdelivr.com/package/npm/@jhintr/lxgw-wenkai-webfont)
[![](https://data.jsdelivr.com/v1/package/npm/@jhintr/lxgw-wenkai-webfont-latin/badge)](https://www.jsdelivr.com/package/npm/@jhintr/lxgw-wenkai-webfont-latin)

A webfont package for the [LXGW-WenKai](https://github.com/lxgw/LxgwWenKai) typeface.

The original `unicode.json` is from [noto sans sc](https://github.com/fontsource/fontsource/blob/main/packages/noto-sans-sc/unicode.json), and I will keep extending characters that not included in it.

Benefits a lot from the work of @chawyehsu https://github.com/chawyehsu/lxgw-wenkai-webfont.

## CDN via jsDelivr

```html
<!-- all chars -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@jhintr/lxgw-wenkai-webfont@1.0/style.css">
<!-- only latin and sanskrit chars -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@jhintr/lxgw-wenkai-webfont-latin@1.0/style.css">
<style>
    body {
        font-family: "LXGWWenKai", cursive;
    }
</style>
```
