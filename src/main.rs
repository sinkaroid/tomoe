mod cli;
mod client;
mod container;
mod downloader;
mod error;
mod logger;
mod models;
mod pdf;

use clap::Parser;
use cli::Cli;
use client::JandaClient;
use container::ensure_jandapress;
use downloader::DownloaderEngine;
use error::TomoeError;
use models::BulkConfig;
use std::fs;
use std::path::Path;

#[tokio::main]
async fn main() -> Result<(), TomoeError> {
    let cli = Cli::parse();
    let mut base_url = String::new();
    let mut janda_started = false;

    if cli.kill_janda {
        container::kill_jandapress()?;
    }

    if cli.start_janda {
        base_url = ensure_jandapress(
            cli.jandapress_url.as_deref(),
            cli.no_selfhost,
            cli.nhentai_api_key.as_deref(),
        )
        .await?;
        janda_started = true;
    }

    let targets = collect_targets(&cli)?;

    if targets.is_empty() {
        if cli.kill_janda || cli.start_janda {
            return Ok(());
        }
        println!("No arguments was given");
        return Ok(());
    }

    if !janda_started {
        base_url = ensure_jandapress(
            cli.jandapress_url.as_deref(),
            cli.no_selfhost,
            cli.nhentai_api_key.as_deref(),
        )
        .await?;
    }

    let client = JandaClient::new(base_url)?;
    let downloader = DownloaderEngine::new()?;

    let total_targets = targets.len();
    println!("Requesting {} doujinshi target(s)...", total_targets);

    for (provider, id) in targets {
        println!("\nProcessing {} target: {}", provider, id);

        match client.get_gallery(&provider, &id).await {
            Ok(gallery) => match downloader.download_gallery(&gallery).await {
                Ok(dir) => {
                    if cli.pdf {
                        let _ = pdf::compile_pdf(&dir, &gallery.id, &gallery.title).map_err(|e| {
                            warn!("Failed to compile PDF for {}: {}", gallery.title, e);
                        });
                    }
                    let html_path = dir.join("tomoe.html");
                    if html_path.exists() {
                        let _ = fs::remove_file(html_path);
                    }
                    println!("Complete process {}", id);
                }
                Err(e) => {
                    warn!("Failed to download gallery {}: {}", id, e);
                }
            },
            Err(e) => {
                warn!("Failed to fetch gallery metadata for {}: {}", id, e);
            }
        }
    }

    println!("\nAll tasks finished!");
    Ok(())
}

/// Collects list of (provider, id) tuples from CLI flags and bulk files.
fn collect_targets(cli: &Cli) -> Result<Vec<(String, String)>, TomoeError> {
    let mut targets = Vec::new();

    if let Some(ref ids) = cli.nhentai {
        for id in ids {
            targets.push(("nhentai".to_string(), id.clone()));
        }
    }

    if let Some(ref ids) = cli.pururin {
        for id in ids {
            targets.push(("pururin".to_string(), id.clone()));
        }
    }

    if let Some(ref ids) = cli.hentaifox {
        for id in ids {
            targets.push(("hentaifox".to_string(), id.clone()));
        }
    }

    if let Some(ref ids) = cli.hentai2read {
        for id in ids {
            targets.push(("hentai2read".to_string(), id.clone()));
        }
    }

    if let Some(ref ids) = cli.simply {
        for id in ids {
            targets.push(("simply-hentai".to_string(), id.clone()));
        }
    }

    if let Some(ref ids) = cli.asmhentai {
        for id in ids {
            targets.push(("asmhentai".to_string(), id.clone()));
        }
    }

    if let Some(ref ids) = cli.three {
        for id in ids {
            targets.push(("3hentai".to_string(), id.clone()));
        }
    }

    if let Some(ref bulk_file) = cli.bulk {
        let path = Path::new(bulk_file);
        if !path.exists() {
            return Err(TomoeError::InvalidBulkFile(format!(
                "Bulk JSON file not found: {}",
                bulk_file
            )));
        }

        let content = fs::read_to_string(path)?;
        let bulk_config: BulkConfig = serde_json::from_str(&content).map_err(|e| {
            TomoeError::InvalidBulkFile(format!("Invalid JSON structure in {}: {}", bulk_file, e))
        })?;

        for item in bulk_config.book {
            for (key, val) in item {
                let provider = match key.as_str() {
                    k if k.starts_with("pur") => "pururin",
                    k if k.starts_with("nh") => "nhentai",
                    k if k.starts_with("hentaif") => "hentaifox",
                    k if k.starts_with("asm") => "asmhentai",
                    k if k.starts_with("simply") => "simply-hentai",
                    k if k.starts_with("hentai2") => "hentai2read",
                    k if k.starts_with("three") || k.starts_with("3") => "3hentai",
                    other => other,
                };

                let val_str = match val {
                    serde_json::Value::Number(n) => n.to_string(),
                    serde_json::Value::String(s) => s,
                    other => other.to_string(),
                };

                targets.push((provider.to_string(), val_str));
            }
        }
    }

    Ok(targets)
}
