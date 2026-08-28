<div align="center">
<a href="https://github.com/sinkaroid/tomoe/wiki"><img width="500" src="https://raw.githubusercontent.com/sinkaroid/tomoe/refs/heads/master/resources/project/images/tomoe_.png" alt="tomoe"></a>

<h3 align="center">An exalted doujinshi downloader with ease.</h3>
<p align="center">
	<a href="https://crates.io/crates/tomoe"><img src="https://img.shields.io/crates/v/tomoe.svg" alt="Crates.io"></a>
	<a href="https://github.com/sinkaroid/tomoe/actions"><img src="https://github.com/sinkaroid/tomoe/workflows/modular%20bulk%20download/badge.svg"></a>
</p>

Tomoe is a CLI tool rewritten in high-performance **Rust (Edition 2024)** for downloading doujinshi from various doujinboards. It features automated self-hosting of [Jandapress](https://github.com/sinkaroid/jandapress) via **Podman**, multi-threaded concurrent image downloading, modular bulk downloads, and native PDF rendering.

<a href="#options">🚀 Commands</a> •
<a href="https://github.com/sinkaroid/tomoe/wiki">Documentation</a> •
<a href="https://github.com/sinkaroid/tomoe/issues/new/choose">Report Issues</a>

</div>

---

## Features

- **Podman Auto-Selfhosting**: Automatically pulls & launches `ghcr.io/sinkaroid/jandapress:latest` locally on-demand.
- **Pure Rust Speed**: Concurrent multi-threaded downloading built on `tokio` and `reqwest`.
- **Native PDF Engine**: Zero-dependency image-to-PDF compiler using `printpdf`.
- **Modular Bulk Downloads**: Seamlessly resolves mixed provider entries from nested JSON files.
- **Cross-Platform**: Support for Windows, Linux, and macOS.

## Site Support

- [nhentai.net](https://nhentai.net/) (`--nhentai`)
- [pururin.to](https://pururin.to/) (`--pururin`)
- [hentaifox.com](https://hentaifox.com/) (`--hentaifox`)
- [hentai2read.com](https://hentai2read.com/) (`--hentai2read`)
- [simply-hentai.com](https://simply-hentai.com/) (`--simply`)
- [asmhentai.com](https://asmhentai.com/) (`--asmhentai`)
- [3hentai.net](https://3hentai.net/) (`--3hentai`)

## Prerequisites

- **Rust 1.75+** (Edition 2024 support)
- **Podman CLI** (Recommended for local container auto-selfhosting)

## Quick Start & Running Locally

### Option 1: Install Locally to PATH

```bash
git clone https://github.com/sinkaroid/tomoe.git
cd tomoe
cargo install --path .

# Then run anywhere:
tomoe --nhentai 255369
```

### Option 2: Run directly with Cargo

```bash
cargo run -- --nhentai 255369
cargo run -- --nhentai 255369 --pdf
cargo run -- --bulk legacy/doujin.json
```

### Option 3: Build Release Executable

```bash
cargo build --release
# Output binary location: ./target/release/tomoe
```

## Options

| Argument                  | Description                                                                | Example                                                                    |
| ------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `--nhentai <ID...>`       | Download from nhentai                                                      | `tomoe --nhentai 255369`                                                   |
| `--pururin <ID...>`       | Download from pururin                                                      | `tomoe --pururin 47226`                                                    |
| `--hentaifox <ID...>`     | Download from hentaifox                                                    | `tomoe --hentaifox 59026`                                                  |
| `--hentai2read <PATH...>` | Download from hentai2read                                                  | `tomoe --hentai2read chaldea_life/1`                                       |
| `--simply <CHAPTER...>`   | Download from simply-hentai                                                | `tomoe --simply "fate-grand-order/fgo-no-ashibon-fgo-foot-book/all-pages"` |
| `--asmhentai <ID...>`     | Download from asmhentai                                                    | `tomoe --asmhentai 311851`                                                 |
| `--3hentai <ID...>`       | Download from 3hentai                                                      | `tomoe --3hentai 608979`                                                   |
| `--bulk <FILE>`           | Bulk download from JSON file                                               | `tomoe --bulk legacy/doujin.json`                                          |
| `--pdf`                   | Render gallery into PDF                                                    | `tomoe --nhentai 255369 --pdf`                                             |
| `--jandapress_url <URL>`  | Specify remote Jandapress server                                           | `tomoe --nhentai 255369 --jandapress_url http://localhost:2002`            |
| `--no_selfhost`           | Skip local Podman container checks                                         | `tomoe --no_selfhost`                                                      |
| `--nhentai_api_key <KEY>` | Optional API key for nhentai official API                                  | `tomoe --nhentai_api_key mykey`                                            |
| `--kill_janda`            | Stop and kill the local Jandapress Podman container (skip if already dead) | `tomoe --kill_janda`                                                       |
| `--start_janda`           | Start the local Jandapress Podman container (skip if already alive)        | `tomoe --start_janda`                                                      |

## Legal

This tool can be freely copied, modified, altered, and distributed without any attribution whatsoever.
