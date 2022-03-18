
<div align="center">
<a href="https://github.com/sinkaroid/tomoe/wiki"><img width="250" src="https://cdn.discordapp.com/attachments/952117487166705747/954297510841679892/tomoe-crot.png" alt="logo"></a>

**A doujinshi downloader with ease for mankind** 

[![Testing](https://github.com/sinkaroid/tomoe/actions/workflows/api.yml/badge.svg)](https://github.com/sinkaroid/tomoe/actions/workflows/test.yml) [![Maintainability](https://api.codeclimate.com/v1/badges/a729e38da1fe1ee520b1/maintainability)](https://codeclimate.com/github/sinkaroid/tomoe/maintainability)
 
It's a CLI tool for downloading doujinshi from various doujinshi websites

<a href="https://github.com/sinkaroid/tomoe/blob/master/CONTRIBUTING.md">Contributing</a> •
<a href="https://github.com/sinkaroid/tomoe/wiki">Wiki</a> •
<a href="https://github.com/sinkaroid/tomoe/issues/new/choose">Report Issues</a>

</div>

## Site support

- ✅nhentai
- ✅pururin
- ✅hentaifox
- ✅hentai2read
- ✅simply-hentai

## Prerequisites

- Python 3.7 or above

## Installation
It's fairly simple to install tomoe.

### from PyPI
`pip install tomoe`

### from pipenv
`pipenv install tomoe`

### from this repository
You can clone this repository, and do `python setup.py install`


## Dependencies
Tomoe just depends on [requests](https://requests.readthedocs.io/en/master/) + [AsyncIO](https://docs.python.org/3/library/asyncio.html), and uses [Janda](https://pypi.org/project/janda/) for it's doujin library client for Python, simple.

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

| **Argument**       | **Description**             | **Example**                                                                                       |
| ------------------ | --------------------------- | ------------------------------------------------------------------------------------------------- |
| --nhentai, int     | download from nhentai       | [`tomoe --nhentai 255369`](https://nhentai.net/g/255369/)                                         |
| --pururin, int     | download from pururin       | [`tomoe --pururin 47226`](https://pururin.to/gallery/47226/crot-sampe-lumpuh)                     |
| --hentaifox, int   | download from hentaifox     | [`tomoe --hentaifox 59026`](https://hentaifox.com/gallery/59026/)                                 |
| --hentai2read, str | download from hentai2read   | [`tomoe --hentai2read chaldea_life`](https://hentai2read.com/chaldea_life/)                       |
| --simply, str      | download from simply-hentai | [`tomoe --simply fate-grand-order/perros`](https://www.simply-hentai.com/fate-grand-order/perros) |

## Todo

- [ ] Support for bulk / mass download
- [ ] Improve image viewer
- [ ] Add convert to another format support
- [ ] Add custom cookie requests

## Legal

This tool can be freely copied, modified, altered, distributed without any attribution whatsoever. However, if you feel
like this tool deserves an attribution, mention it. It won't hurt anybody

Please, read the [license terms](LICENSE). Don't worry, it can be read in less than 30 seconds, unless you have some
sort of reading disability - in that case, I'm wondering why you're still reading this text. Really. Stop. Please. I
mean, seriously. Why are you still reading?

## Pronounciation
[`ja_JP`](https://www.localeplanet.com/java/ja-JP/index.html) • **to-moe** — that resembles a comma or the usual form of a magatama.

## EoF
All books from those doujinboards are definitely ilegal from original authors.