<div align="center">
<a href="https://github.com/sinkaroid/tomoe/wiki"><img width="500" src="https://cdn.discordapp.com/attachments/952117487166705747/1013588505919762443/tomoe_.png" alt="tomoe"></a>

<h4 align="center">An exalted doujinshi downloader with ease.</h4>
<p align="center">
	<a href="https://github.com/sinkaroid/tomoe/actions/workflows/api.yml"><img src="https://github.com/sinkaroid/tomoe/workflows/modular%20bulk%20download/badge.svg"></a>
	<a href="https://codeclimate.com/github/sinkaroid/tomoe/maintainability"><img src="https://api.codeclimate.com/v1/badges/a729e38da1fe1ee520b1/maintainability" /></a>
</p>

Tomoe is a CLI tool for downloading doujinshi from various doujinboards. It's also has built-in modular bulk downloads, and has auto render into PDF (**Portable Document Format**) for it's utility, hopefully will be reusable.  

<a href="#options">🚀 Commands</a> •
<a href="https://github.com/sinkaroid/tomoe/wiki">Documentation</a> •
<a href="https://github.com/sinkaroid/tomoe/issues/new/choose">Report Issues</a>
</div>

- [Tomoe](#)
  - [Features](#features)
    - [Tomoe vs. the doujinboards](#tomoe-vs-the-doujinboards)
    - [Site support](#site-support)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
  - [Documentation](https://github.com/sinkaroid/tomoe/wiki)
    - [Command usage](#command-usage)
    - [Quick examples](#quick-example)
    - [Options](#options)
    - [Bulk download](#bulk-download)
    - [Bulk download using nested list](#bulk-download-using-nested-list)
  - [Pronounciation](#pronounciation)
  - [Acknowledgements](./CLOSING_REMARKS.md)
  - [Legal](#legal)
  - [EoF](#eof)
  
---

## Tomoe vs. the doujinboards
Tomoe consumes [Jandapress](https://github.com/sinkaroid/jandapress) and uses [janda](https://pypi.org/project/janda/) for the doujin Python library.  

**Features availability** Speed or perfomace may not accurate because internet connection or API response. Some tests has high resolve time and rendering a bit longer, because some source does not providing real extension of a images, tomoe should check and guessing it's format.

| Site            | Status                                                                                                                                                              | Bulk download | Average response  | Downloaded |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ | ------------- | ---------------------- |
| `nhentai`       | [![Nhentai download](https://github.com/sinkaroid/tomoe/workflows/nhentai/badge.svg)](https://github.com/sinkaroid/tomoe/actions/workflows/nhentai.yml)             | `Yes` | ~0.52 minutes | ~10.39 MB (26 images) |
| `pururin`       | [![Pururin download](https://github.com/sinkaroid/tomoe/workflows/pururin/badge.svg)](https://github.com/sinkaroid/tomoe/actions/workflows/pururin.yml)             | `Yes` |~0.63 minutes | ~15.55 MB (20 images) |
| `hentaifox`     | [![Hentaifox download](https://github.com/sinkaroid/tomoe/workflows/hentaifox/badge.svg)](https://github.com/sinkaroid/tomoe/actions/workflows/hentaifox.yml)       | `Yes` |~0.33 minutes | ~8.18 MB (26 images)  |
| `hentai2read`   | [![Hentai2read download](https://github.com/sinkaroid/tomoe/workflows/hentai2read/badge.svg)](https://github.com/sinkaroid/tomoe/actions/workflows/hentai2read.yml) | `Yes` |~0.10 minutes | ~7.78 MB (26 images)  |
| `simply-hentai` | [![Simply-hentai download](https://github.com/sinkaroid/tomoe/workflows/simplyh/badge.svg)](https://github.com/sinkaroid/tomoe/actions/workflows/simply.yml)        | `Yes` |~0.29 minutes | ~42.61 MB (19 images) |
| `asmhentai`     | [![Asmhentai download](https://github.com/sinkaroid/tomoe/workflows/asmhentai/badge.svg)](https://github.com/sinkaroid/tomoe/actions/workflows/asmhentai.yml)       | `Yes` |~0.23 minutes | ~4.96 MB (23 images)  |


## Features

- Plenty of sites coverage
- Built-in auto render into PDF
- Modular bulk downloads
- Minimalist dependencies
- Download with ease, doesn't require you a lot of arguments

<img src="https://cdn.discordapp.com/attachments/952117487166705747/955118232119955466/nh-tomoe.png" width="600" alt="tomoe">

## Site support

Currently tomoe support the following websites:

- [nhentai.net](https://nhentai.net/)
- [pururin.to](https://pururin.to/)
- [hentaifox.com](https://hentaifox.com/)
- [hentai2read.com](https://hentai2read.com/)
- [simply-hentai.com](https://simply-hentai.com/)
- [asmhentai.com](https://asmhentai.com/)


## Prerequisites

<table>
	<td><b>NOTE:</b> Python 3.7 or above</td>
</table>

## Installation

`pip install tomoe` / `pipenv install tomoe`  

- Or manual build by cloning the repository and running `python setup.py install`


## Command usage

`tomoe --args <id|path>`

## Quick example

`tomoe --nhentai 177013`

After that, you could see the download results or throw you an error if something went wrong.

## Options

It's fairly simple to use tomoe

| **Argument**                      | **Description**             | **Example**                                                                                                                                                         |
| --------------------------------- | --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| --nhentai, int                    | nhentai       | [`tomoe --nhentai 255369`](https://nhentai.net/g/255369/)                                                                                                           |
| --pururin, int                    | pururin       | [`tomoe --pururin 47226`](https://pururin.to/gallery/47226/crot-sampe-lumpuh)                                                                                       |
| --hentaifox, int                  | hentaifox     | [`tomoe --hentaifox 59026`](https://hentaifox.com/gallery/59026/)                                                                                                   |
| --hentai2read, str chapter:number | hentai2read   | [`tomoe --hentai2read chaldea_life:1`](https://hentai2read.com/chaldea_life/)                                                                                       |
| --simply, str                     | simply-hentai | [`tomoe --simply "fate-grand-order/fgo-no-ashibon-fgo-foot-book/all-pages"`](https://www.simply-hentai.com/fate-grand-order/fgo-no-ashibon-fgo-foot-book/all-pages) |
| --asmhentai, int                  | asmhentai     | [`tomoe --asmhentai 311851`](https://asmhentai.com/g/311851/)                                                                                                       |

## Bulk download
You can passing multiple id to requests bulk download

| **Sites**   | **Description**                 | **Example**                                                                                                                |
| ----------- | ------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| nhentai     | place multiple id               | `tomoe --nhentai 255369 417103 417119`                                                                                     |
| pururin     | place multiple id               | `tomoe --pururin 47226 64351 56175`                                                                                        |
| hentaifox   | place multiple id               | `tomoe --hentaifox 59026 61805`                                                                                            |
| hentai2read | place multiple `chapter:number` | `tomoe --hentai2read chaldea_life:1 watashitachi_producersan_ni_mechakucha:1`                                              |
| simply      | place multiple chapter          | `tomoe --simply "fate-grand-order/fgo-no-ashibon-fgo-foot-book/all-pages" "original-work/kanchou-manga-cffc37a/all-pages"` |
| asmhentai   | place multiple id               | `tomoe --asmhentai 311851 210135 309068`                                                                                   |

## Bulk download using nested list
`tomoe --bulk doujin.json`  

Since this tool covers plenty of website, If You need to download from each multiple different website You can make bulk download with arbitrary methods, Meant you can mix and wrap the whole book id into nested array in a JSON file. Read more about [Understanding Nested Arrays.](https://javascript.plainenglish.io/understanding-the-nested-arrays-fbf3ab13c2b4#:~:text=An%20array%20is%20an%20ordered,the%20element%20of%20an%20array)

Create `doujin.json` in the same directory You want to run tomoe and follow this structure:  
**Note** *You should not change the "book" property*
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
            "hentai2read": "chaldea_life:1"
        },
        {
            "simply": "fate-grand-order/fgo-no-ashibon-fgo-foot-book/all-pages"
        }
    ]
}
```

Then tells tomoe to resolve all the book id from the JSON file.
`tomoe --bulk doujin.json`

## Legal

This tool can be freely copied, modified, altered, distributed without any attribution whatsoever. However, if you feel
like this tool deserves an attribution, mention it. It won't hurt anybody.
> Licence: WTF.

## Pronounciation

[`ja_JP`](https://www.localeplanet.com/java/ja-JP/index.html) • **to-moe** — commonly translated as "comma", is a comma-like swirl symbol used in Japanese mon. It closely resembles the usual form of a magatama.

## EoF

All books from those third-party doujinboards are definitely ilegal from original authors. Support the authors by buying the original book.