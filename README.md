# Tomoe [![Testing](https://github.com/sinkaroid/tomoe/actions/workflows/api.yml/badge.svg)](https://github.com/sinkaroid/tomoe/actions/workflows/api.yml) [![Maintainability](https://api.codeclimate.com/v1/badges/a729e38da1fe1ee520b1/maintainability)](https://codeclimate.com/github/sinkaroid/tomoe/maintainability)

<a href="https://github.com/sinkaroid/tomoe/wiki"><img align="right" src="https://cdn.discordapp.com/attachments/952117487166705747/954724094379708436/s.png" width="180"></a>

**A doujinshi downloader with ease**

Tomoe is a CLI tool for downloading doujinshi from various doujinboards. It's also has built-in auto render into PDF for it's utility, hopefully will be reusable.

> 🚀 [Commands](#options) • [Documentation](https://github.com/sinkaroid/tomoe/wiki) • [Report Issues](https://github.com/sinkaroid/tomoe/issues/new/choose)

## Tomoe vs. the doujinboards

Some tests has high resolve time and rendering a bit longer,  
because some source does not providing real extension of a images, tomoe should check and guessing it's format

| Site            | Status                                                                                                                                                              | Average time  | Downloaded contents    |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- | ---------------------- |
| `nhentai`       | [![Nhentai download](https://github.com/sinkaroid/tomoe/workflows/nhentai/badge.svg)](https://github.com/sinkaroid/tomoe/actions/workflows/nhentai.yml)             | ~0.52 minutes | ~10.39 MB (26 content) |
| `pururin`       | [![Pururin download](https://github.com/sinkaroid/tomoe/workflows/pururin/badge.svg)](https://github.com/sinkaroid/tomoe/actions/workflows/pururin.yml)             | ~0.63 minutes | ~15.55 MB (20 content) |
| `hentaifox`     | [![Hentaifox download](https://github.com/sinkaroid/tomoe/workflows/hentaifox/badge.svg)](https://github.com/sinkaroid/tomoe/actions/workflows/hentaifox.yml)       | ~0.33 minutes | ~8.18 MB (26 content)  |
| `hentai2read`   | [![Hentai2read download](https://github.com/sinkaroid/tomoe/workflows/hentai2read/badge.svg)](https://github.com/sinkaroid/tomoe/actions/workflows/hentai2read.yml) | ~0.10 minutes | ~7.78 MB (26 content)  |
| `simply-hentai` | [![Simply-hentai download](https://github.com/sinkaroid/tomoe/workflows/simplyh/badge.svg)](https://github.com/sinkaroid/tomoe/actions/workflows/simply.yml)        | ~0.29 minutes | ~42.61 MB (19 content) |
| `asmhentai`     | [![Asmhentai download](https://github.com/sinkaroid/tomoe/workflows/asmhentai/badge.svg)](https://github.com/sinkaroid/tomoe/actions/workflows/asmhentai.yml)       | ~0.23 minutes | ~4.96 MB (23 content)  |

## Features

- Plenty of sites coverage
- Built-in auto render into PDF
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

## Dependencies

tomoe depends on [requests](https://requests.readthedocs.io/en/master/) + [asyncio](https://docs.python.org/3/library/asyncio.html),
and uses [janda](https://pypi.org/project/janda/) for it's doujin library client for Python.

## Prerequisites

<table>
	<td><b>NOTE:</b> Python 3.7 or above</td>
</table>

## Installation

It's fairly simple to install tomoe

### 🚀from PyPI

`pip install tomoe`

### 🚀from pipenv

`pipenv install tomoe`

### 🚀from this repository

Clone this repository, and do `python setup.py install`

## Command usage

`tomoe --args <id|path>`

## Quick example

    $ tomoe --nhentai 255369

After that, you could see the download results or throw you an error if something went wrong.

## Options

Here are all the options it supports.

| **Argument**                      | **Description**             | **Example**                                                                                                                                                         |
| --------------------------------- | --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| --nhentai, int                    | download from nhentai       | [`tomoe --nhentai 255369`](https://nhentai.net/g/255369/)                                                                                                           |
| --pururin, int                    | download from pururin       | [`tomoe --pururin 47226`](https://pururin.to/gallery/47226/crot-sampe-lumpuh)                                                                                       |
| --hentaifox, int                  | download from hentaifox     | [`tomoe --hentaifox 59026`](https://hentaifox.com/gallery/59026/)                                                                                                   |
| --hentai2read, str chapter:number | download from hentai2read   | [`tomoe --hentai2read chaldea_life:1`](https://hentai2read.com/chaldea_life/)                                                                                       |
| --simply, str                     | download from simply-hentai | [`tomoe --simply "fate-grand-order/fgo-no-ashibon-fgo-foot-book/all-pages"`](https://www.simply-hentai.com/fate-grand-order/fgo-no-ashibon-fgo-foot-book/all-pages) |
| --asmhentai, int                  | download from asmhentai     | [`tomoe --asmhentai 311851`](https://asmhentai.com/g/311851/)                                                                                                       |

### Bulk Download

| **Sites**   | **Description**                 | **Example**                                                                                                                |
| ----------- | ------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| nhentai     | place multiple id               | `tomoe --nhentai 255369 417103 417119`                                                                                     |
| pururin     | place multiple id               | `tomoe --pururin 47226 64351 56175`                                                                                        |
| hentaifox   | place multiple id               | `tomoe --hentaifox 59026 61805`                                                                                            |
| hentai2read | place multiple `chapter:number` | `tomoe --hentai2read chaldea_life:1 watashitachi_producersan_ni_mechakucha:1`                                              |
| simply      | place multiple chapter          | `tomoe --simply "fate-grand-order/fgo-no-ashibon-fgo-foot-book/all-pages" "original-work/kanchou-manga-cffc37a/all-pages"` |
| asmhentai   | place multiple id               | `tomoe --asmhentai 311851 210135 309068`                                                                                   |

## Todo

- [ ] Support for bulk download
- [x] Improve image viewer
- [x] Add render to another format support
- [ ] Add custom cookie requests

## Legal

This tool can be freely copied, modified, altered, distributed without any attribution whatsoever. However, if you feel
like this tool deserves an attribution, mention it. It won't hurt anybody

## Pronounciation

[`ja_JP`](https://www.localeplanet.com/java/ja-JP/index.html) • **to-moe** — that resembles a comma or the usual form of a [magatama](#tomoe).

## EoF

All books from those doujinboards are definitely ilegal from original authors.
