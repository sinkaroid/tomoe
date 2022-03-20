
<div align="center">
<a href="https://github.com/sinkaroid/tomoe/wiki"><img width="220" src="https://cdn.discordapp.com/attachments/952117487166705747/954724094379708436/s.png" alt="logo"></a>

**A doujinshi downloader with ease for mankind** 


 
tomoe is a CLI tool for downloading doujinshi from various doujinboards,  
It's also has built-in auto render into PDF for it's utility.

<a href="https://github.com/sinkaroid/tomoe/blob/master/CONTRIBUTING.md">Contributing</a> •
<a href="https://github.com/sinkaroid/tomoe/wiki">Wiki</a> •
<a href="https://github.com/sinkaroid/tomoe/issues/new/choose">Report Issues</a>

[![Testing](https://github.com/sinkaroid/tomoe/actions/workflows/api.yml/badge.svg)](https://github.com/sinkaroid/tomoe/actions/workflows/test.yml) [![Maintainability](https://api.codeclimate.com/v1/badges/a729e38da1fe1ee520b1/maintainability)](https://codeclimate.com/github/sinkaroid/tomoe/maintainability) [![Deps](https://img.shields.io/pypi/v/tomoe?label=PyPI&logo=PyPI&logoColor=white&color=blue)](https://codeclimate.com/github/sinkaroid/tomoe/maintainability)

<img src="https://cdn.discordapp.com/attachments/952117487166705747/955042310788354148/TOMOCROT.png" width="700" alt="tomoe">
<br>


tomoe depends on [requests](https://requests.readthedocs.io/en/master/) + [asyncIO](https://docs.python.org/3/library/asyncio.html), and uses [Janda](https://pypi.org/project/janda/) for it's doujin library client for Python.


</div>



## Site support

- [x] nhentai
- [x] pururin
- [x] hentaifox
- [x] hentai2read
- [x] simply-hentai
- [x] qhentai 

### Prerequisites

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

## Or if you clone manual this repo
	$ python setup.py install
	$ tomoe --nhentai 255369

After that, you could see the download results or throw you an error if something went wrong, this module also generating a static image viewer.


## Options

Here are all the options it supports.

| **Argument**               | **Description**             | **Example**                                                                                         |
| -------------------------- | --------------------------- | --------------------------------------------------------------------------------------------------- |
| --nhentai, int             | download from nhentai       | [`tomoe --nhentai 255369`](https://nhentai.net/g/255369/)                                           |
| --pururin, int             | download from pururin       | [`tomoe --pururin 47226`](https://pururin.to/gallery/47226/crot-sampe-lumpuh)                       |
| --hentaifox, int           | download from hentaifox     | [`tomoe --hentaifox 59026`](https://hentaifox.com/gallery/59026/)                                   |
| --hentai2read, str chapter | download from hentai2read   | [`tomoe --hentai2read chaldea_life 1`](https://hentai2read.com/chaldea_life/)                       |
| --simply, str              | download from simply-hentai | [`tomoe --simply "fate-grand-order/perros"`](https://www.simply-hentai.com/fate-grand-order/perros) |
| --qhentai, str             | download from qhentai       | [`tomoe --simply "eight-star-sand"`](https://qhentai.net/eight-star-sand/)                          |

## Todo

- [ ] Support for bulk download
- [x] Improve image viewer
- [x] Add render to another format support
- [ ] Add custom cookie requests

## Legal

This tool can be freely copied, modified, altered, distributed without any attribution whatsoever. However, if you feel
like this tool deserves an attribution, mention it. It won't hurt anybody

## Pronounciation
[`ja_JP`](https://www.localeplanet.com/java/ja-JP/index.html) • **to-moe** — that resembles a comma or the usual form of a magatama.

## EoF
All books from those doujinboards are definitely ilegal from original authors.