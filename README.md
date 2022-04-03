# Tomoe

<a href="https://github.com/sinkaroid/tomoe/wiki"><img align="right" src="https://cdn.discordapp.com/attachments/952117487166705747/954724094379708436/s.png" width="200"></a>

[![Testing](https://github.com/sinkaroid/tomoe/actions/workflows/api.yml/badge.svg)](https://github.com/sinkaroid/tomoe/actions/workflows/api.yml) [![Maintainability](https://api.codeclimate.com/v1/badges/a729e38da1fe1ee520b1/maintainability)](https://codeclimate.com/github/sinkaroid/tomoe/maintainability)

**A doujinshi downloader with ease**  

Tomoe is a CLI tool for downloading doujinshi from various doujinboards, apart from nHentai this stuff also has plenty sites coverage. It's also has built-in auto render into PDF for it's utility, hopefully will be reusable and one step closer to a full-fledged downloader.  

> 🚀 [Contributing](https://github.com/sinkaroid/tomoe/blob/master/CONTRIBUTING.md) • [Documentation](https://github.com/sinkaroid/tomoe/wiki) • [Releases](https://github.com/sinkaroid/tomoe/releases) • [Report Issues](https://github.com/sinkaroid/tomoe/issues/new/choose) • [Support this Project](https://paypal.me/sinkaroid)

## Features
- Plenty of sites coverage
- Built-in auto render into PDF
- Minimalist dependencies
- Download with ease, doesn't require you a lot of arguments

## Site support
<details>
<img src="https://cdn.discordapp.com/attachments/952117487166705747/955118232119955466/nh-tomoe.png" width="700" alt="tomoe">
</details> 

- [x] nhentai
- [x] pururin
- [x] hentaifox
- [x] hentai2read
- [x] simply-hentai
- [x] qhentai 
- [x] asmhentai

## Dependencies
Tomoe depends on [requests](https://requests.readthedocs.io/en/master/) + [asyncIO](https://docs.python.org/3/library/asyncio.html), 
and uses [Janda](https://pypi.org/project/janda/) for it's doujin library client for Python.

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

## Usage
`tomoe --args <bookID>`

## Quick example
	$ tomoe --nhentai 255369


After that, you could see the download results or throw you an error if something went wrong.

## Options

Here are all the options it supports.

| **Argument**               | **Description**             | **Example**                                                                                         |
|----------------------------|-----------------------------|-----------------------------------------------------------------------------------------------------|
| --nhentai, int             | download from nhentai       | [`tomoe --nhentai 255369`](https://nhentai.net/g/255369/)                                           |
| --pururin, int             | download from pururin       | [`tomoe --pururin 47226`](https://pururin.to/gallery/47226/crot-sampe-lumpuh)                       |
| --hentaifox, int           | download from hentaifox     | [`tomoe --hentaifox 59026`](https://hentaifox.com/gallery/59026/)                                   |
| --hentai2read, str chapter | download from hentai2read   | [`tomoe --hentai2read chaldea_life 1`](https://hentai2read.com/chaldea_life/)                       |
| --simply, str              | download from simply-hentai | [`tomoe --simply "fate-grand-order/perros"`](https://www.simply-hentai.com/fate-grand-order/perros) |
| --qhentai, str             | download from qhentai       | [`tomoe --qhentai "eight-star-sand"`](https://qhentai.net/eight-star-sand/)                         |
| --asmhentai, int           | download from asmhentai     | [`tomoe --asmhentai 311851`](https://asmhentai.com/g/311851/)                                       |

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