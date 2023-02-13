<div align="center">
<a href="https://github.com/sinkaroid/tomoe/wiki"><img width="500" src="https://cdn.discordapp.com/attachments/952117487166705747/1013588505919762443/tomoe_.png" alt="tomoe"></a>

<h3 align="center">An exalted doujinshi downloader with ease.</h3>
<p align="center">
	<a href="https://github.com/sinkaroid/tomoe/actions/workflows/bulk_download.yml"><img src="https://github.com/sinkaroid/tomoe/workflows/modular%20bulk%20download/badge.svg"></a>
	<a href="https://codeclimate.com/github/sinkaroid/tomoe/maintainability"><img src="https://api.codeclimate.com/v1/badges/a729e38da1fe1ee520b1/maintainability" /></a>
</p>

Tomoe is a CLI tool for downloading doujinshi from various doujinboards. It's also has built-in modular bulk download and auto render into PDF (**Portable Document Format**) for it's utility, hopefully will be reusable.

<a href="#options">🚀 Commands</a> •
<a href="https://github.com/sinkaroid/tomoe/wiki">Documentation</a> •
<a href="https://github.com/sinkaroid/tomoe/issues/new/choose">Report Issues</a>

</div>

- [Tomoe](#)
  - [Features](#features)
    - [Tomoe availability](#tomoe-vs-the-doujinboards)
    - [Site support](#site-support)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
  - [Documentation](https://github.com/sinkaroid/tomoe/wiki)
    - [Command usage](#command-usage)
    - [Quick examples](#quick-example)
    - [Options](#options)
    - [Bulk download](#bulk-download)
    - [Bulk download using nested list](#bulk-download-using-nested-list)
  - [Pronunciation](#pronunciation)
  - [Acknowledgements](./CLOSING_REMARKS.md)
  - [Legal](#legal)

---

## Tomoe vs. the doujinboards

Tomoe consumes [Jandapress](https://github.com/sinkaroid/jandapress) and uses [janda](https://pypi.org/project/janda/) for the doujin Python library.

**Features availability** Speed or performance may not be accurate because internet connection or API response. Some tests have high resolve time and render a bit longer, because some sources do not provide real extension of an images, tomoe should check and guess it's format.

| Site            | Status                                                                                                                                                              | Bulk download | Average response | 
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- | ---------------- | 
| `nhentai`       | [![Nhentai download](https://github.com/sinkaroid/tomoe/workflows/Nhentai%20test/badge.svg)](https://github.com/sinkaroid/tomoe/actions/workflows/nhentai.yml)             | `Yes`         | ~0.52 minutes    | 
| `pururin`       | [![Pururin download](https://github.com/sinkaroid/tomoe/workflows/Pururin%20test/badge.svg)](https://github.com/sinkaroid/tomoe/actions/workflows/pururin.yml)             | `Yes`         | ~0.63 minutes    |
| `hentaifox`     | [![Hentaifox download](https://github.com/sinkaroid/tomoe/workflows/Hentaifox%20test/badge.svg)](https://github.com/sinkaroid/tomoe/actions/workflows/hentaifox.yml)       | `Yes`         | ~0.33 minutes    |
| `hentai2read`   | [![Hentai2read download](https://github.com/sinkaroid/tomoe/workflows/Hentai2read%20test/badge.svg)](https://github.com/sinkaroid/tomoe/actions/workflows/hentai2read.yml) | `Yes`         | ~0.10 minutes    | 
| `simply-hentai` | [![Simply-hentai download](https://github.com/sinkaroid/tomoe/workflows/Simplyhentai%20test/badge.svg)](https://github.com/sinkaroid/tomoe/actions/workflows/simply.yml)        | `Yes`         | ~0.29 minutes    |
| `asmhentai`     | [![Asmhentai download](https://github.com/sinkaroid/tomoe/workflows/Asmhentai%20test/badge.svg)](https://github.com/sinkaroid/tomoe/actions/workflows/asmhentai.yml)       | `Yes`         | ~0.23 minutes    |
| `3hentai`     | [![3hentai download](https://github.com/sinkaroid/tomoe/workflows/3hentai%20test/badge.svg)](https://github.com/sinkaroid/tomoe/actions/workflows/3hentai.yml)       | `Yes`         | ~0.20 minutes    |

## Features

- Plenty of sites coverage
- Built-in auto render into PDF
- Modular bulk download
- Minimalist dependencies
- Download with ease, doesn't require you a lot of arguments

<img src="https://cdn.discordapp.com/attachments/997107089921028136/1014351915578040380/tomoe_.png" width="600" alt="tomoe">

## Site support

Currently tomoe supports the following websites:

- [nhentai.net](https://nhentai.net/)
- [pururin.to](https://pururin.to/)
- [hentaifox.com](https://hentaifox.com/)
- [hentai2read.com](https://hentai2read.com/)
- [simply-hentai.com](https://simply-hentai.com/)
- [asmhentai.com](https://asmhentai.com/)
- [3hentai.net](https://3hentai.net/)

## Prerequisites

<table>
	<td><b>NOTE:</b> Python 3.7 or above</td>
</table>

## Installation

`pip install tomoe`

- Or manual build by cloning the repository and run `python setup.py install`

## Command usage

`tomoe --args <id|path>`

## Quick example

`tomoe --nhentai 177013`

After that, you could see the download results or throw you an error if something went wrong.

## Options

It's fairly simple to use tomoe

| **Argument**                      | **Description**           | **Example**                                                                                                                                                         |
| --------------------------------- | ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| --nhentai, int                    | nhentai                   | [`tomoe --nhentai 255369`](https://nhentai.net/g/255369/)                                                                                                           |
| --pururin, int                    | pururin                   | [`tomoe --pururin 47226`](https://pururin.to/gallery/47226/crot-sampe-lumpuh)                                                                                       |
| --hentaifox, int                  | hentaifox                 | [`tomoe --hentaifox 59026`](https://hentaifox.com/gallery/59026/)                                                                                                   |
| --hentai2read, str chapter:number | hentai2read               | [`tomoe --hentai2read chaldea_life/1`](https://hentai2read.com/chaldea_life/)                                                                                       |
| --simply, str                     | simply-hentai             | [`tomoe --simply "fate-grand-order/fgo-no-ashibon-fgo-foot-book/all-pages"`](https://www.simply-hentai.com/fate-grand-order/fgo-no-ashibon-fgo-foot-book/all-pages) |
| --asmhentai, int                  | asmhentai                 | [`tomoe --asmhentai 311851`](https://asmhentai.com/g/311851/)     
| --three, int                  | 3hentai                 | [`tomoe --three 608979`](https://asmhentai.com/g/311851/)                                                                                                   |
| --bulk, str                       | custom bulk download      | [`tomoe --bulk doujin.json`](/doujin.json)                                                                                                                          |
| --pdf, str                        | render pdf for each title | [`tomoe --nhentai 255369 --pdf`](https://3hentai.net/d/608979)                                                                                                     |

## Bulk download

You can pass multiple id to request bulk download

| **Sites**   | **Description**                 | **Example**                                                                                                                |
| ----------- | ------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| nhentai     | place multiple id               | `tomoe --nhentai 255369 417103 417119`                                                                                     |
| pururin     | place multiple id               | `tomoe --pururin 47226 64351 56175`                                                                                        |
| hentaifox   | place multiple id               | `tomoe --hentaifox 59026 61805`                                                                                            |
| hentai2read | place multiple `chapter:number` | `tomoe --hentai2read chaldea_life/1 watashitachi_producersan_ni_mechakucha/1`                                              |
| simply      | place multiple chapter          | `tomoe --simply "fate-grand-order/fgo-no-ashibon-fgo-foot-book/all-pages" "original-work/kanchou-manga-cffc37a/all-pages"` |
| asmhentai   | place multiple id               | `tomoe --asmhentai 311851 210135 309068`                                                                                   |

## Bulk download using nested list

`tomoe --bulk doujin.json`

If you need to download multiple doujins from each different website, you can do a bulk download using an arbitrary method. Meaning that you can mix and wrap the whole book ids into nested array in a JSON file. Read more about [Understanding Nested Arrays.](https://javascript.plainenglish.io/understanding-the-nested-arrays-fbf3ab13c2b4#:~:text=An%20array%20is%20an%20ordered,the%20element%20of%20an%20array)

Create `doujin.json` in the same directory where you want to run tomoe and follow this structure:  
**Note** _You should not change the "book" property_

```js
{
    "book": [
        {
            "nhentai": 177013
        },
        {
            "nhentai": 255369
        },
        {
            "pururin": 47226
        },
        {
            "pururin": 64351
        },
        {
            "hentaifox": 59026
        },
        {
            "hentaifox": 61805
        },
        {
            "asmhentai": 311851
        },
        {
            "asmhentai": 210135
        },
        {
            "hentai2read": "chaldea_life/1"
        },
        {
            "simply": "fate-grand-order/fgo-no-ashibon-fgo-foot-book/all-pages"
        }
    ]
}
```

Then tell tomoe to resolve all the book ids from the JSON file.
`tomoe --bulk doujin.json`

## Pronunciation

[`ja_JP`](https://www.localeplanet.com/java/ja-JP/index.html) • **to-moe** — commonly translated as "comma", is a comma-like swirl symbol used in Japanese mon. It closely resembles the usual form of a magatama.

## Legal

This tool can be freely copied, modified, altered, distributed without any attribution whatsoever. However, if you feel
like this tool deserves an attribution, mention it. It won't hurt anybody.

> Licence: WTF.