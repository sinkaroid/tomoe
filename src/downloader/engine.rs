use crate::error::TomoeError;
use crate::models::Gallery;
use crate::warn;
use reqwest::Client;
use std::fs::{self, File};
use std::io::Write;
use std::path::{Path, PathBuf};
use std::sync::Arc;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::time::{Duration, Instant};
use tokio::sync::Semaphore;

/// Image downloader engine for concurrent gallery fetching.
#[derive(Debug, Clone)]
pub struct DownloaderEngine {
    client: Client,
    concurrency: usize,
}

impl DownloaderEngine {
    /// Creates a new `DownloaderEngine` with default concurrency of 5 worker tasks.
    pub fn new() -> Result<Self, TomoeError> {
        let user_agent = format!("Tomoe/{} (Rust)", env!("CARGO_PKG_VERSION"));
        let client = Client::builder()
            .timeout(Duration::from_secs(30))
            .user_agent(user_agent)
            .build()?;
        Ok(Self {
            client,
            concurrency: 5,
        })
    }

    /// Sets custom concurrency level for downloading images.
    #[allow(dead_code)]
    pub fn with_concurrency(mut self, concurrency: usize) -> Self {
        self.concurrency = concurrency.max(1);
        self
    }

    /// Downloads all images for a given `Gallery` into a local directory.
    pub async fn download_gallery(&self, gallery: &Gallery) -> Result<PathBuf, TomoeError> {
        let start_time = Instant::now();
        let sanitized_title = sanitize_filename(&gallery.title);
        let mut raw_id = gallery.id.clone();
        if raw_id.starts_with("http://") || raw_id.starts_with("https://") {
            let pos = raw_id.find(&gallery.provider).unwrap();
            let sub = &raw_id[pos..];
            if let Some(slash_pos) = sub.find('/') {
                raw_id = sub[slash_pos + 1..].to_string();
            }
        }
        let clean_id = sanitize_filename(&raw_id.replace(['/', '\\'], "_"));
        let dir_name = format!("{}-{}-{}", gallery.provider, clean_id, sanitized_title);
        let output_dir = PathBuf::from(&dir_name);

        if !output_dir.exists() {
            fs::create_dir_all(&output_dir)?;
        }

        println!("----------------------------------------");
        println!("TITLE  : {}", gallery.title);
        println!("TAGS   : {}", gallery.tags.join(", "));
        println!("ID     : {}", gallery.id);
        println!("SOURCE : {}", gallery.provider);
        println!("TOTAL  : {} pages", gallery.total);
        println!("----------------------------------------");

        let image_urls = &gallery.images;
        if image_urls.is_empty() {
            warn!("No images found in gallery {}.", gallery.id);
            return Ok(output_dir);
        }

        // Check if gallery is already fully downloaded
        let existing_files_count = count_downloaded_images(&output_dir)?;
        if existing_files_count >= image_urls.len() {
            println!(
                "All {} images are already downloaded in: {}",
                image_urls.len(),
                output_dir
                    .canonicalize()
                    .unwrap_or_else(|_| output_dir.clone())
                    .display()
            );
            self.generate_tomoe_html(&output_dir, &dir_name, gallery)?;
            return Ok(output_dir);
        }

        let total_count = image_urls.len();
        let completed_counter = Arc::new(AtomicUsize::new(0));

        let semaphore = Arc::new(Semaphore::new(self.concurrency));
        let client = self.client.clone();
        let output_dir_arc = Arc::new(output_dir.clone());

        let mut handles = Vec::with_capacity(image_urls.len());
        for (idx, url) in image_urls.iter().enumerate() {
            let sem = semaphore.clone();
            let client = client.clone();
            let dir = output_dir_arc.clone();
            let counter = completed_counter.clone();
            let url = url.clone();

            let handle = tokio::spawn(async move {
                let _permit = sem.acquire().await.unwrap();
                let filename = extract_filename(&url, idx);
                let file_path = dir.join(&filename);

                if file_path.exists() && file_path.metadata().map(|m| m.len()).unwrap_or(0) > 0 {
                    let current = counter.fetch_add(1, Ordering::SeqCst) + 1;
                    print!("\r[Downloading] Page {}/{}", current, total_count);
                    let _ = std::io::stdout().flush();
                    return Ok::<(), TomoeError>(());
                }

                let mut retries = 3;
                let mut current_url = url.clone();
                let mut bytes_data = None;

                while retries > 0 {
                    match client.get(&current_url).send().await {
                        Ok(resp) if resp.status().is_success() => match resp.bytes().await {
                            Ok(b) => {
                                bytes_data = Some(b);
                                break;
                            }
                            Err(_) => retries -= 1,
                        },
                        Ok(resp) => {
                            if resp.status().as_u16() == 404 && current_url.ends_with(".jpg") {
                                current_url = current_url.replace(".jpg", ".png");
                            }
                            retries -= 1;
                        }
                        Err(_) => retries -= 1,
                    }
                    tokio::time::sleep(Duration::from_millis(500)).await;
                }

                let bytes = bytes_data.ok_or_else(|| TomoeError::DownloadError {
                    url: url.clone(),
                    reason: "Failed after multiple retries".to_string(),
                })?;

                let mut file = File::create(&file_path)?;
                file.write_all(&bytes)?;

                let current = counter.fetch_add(1, Ordering::SeqCst) + 1;
                print!("\r[Downloading] Page {}/{}", current, total_count);
                let _ = std::io::stdout().flush();
                Ok(())
            });
            handles.push(handle);
        }

        for handle in handles {
            if let Ok(Err(e)) = handle.await {
                warn!("Warning: {}", e);
            }
        }

        println!("\nDownload complete!");

        let elapsed = start_time.elapsed();
        let total_size_mb = calculate_dir_size_mb(&output_dir)?;
        println!(
            "Successfully downloaded gallery in {:.2?} (Total size: {:.2} MB)",
            elapsed, total_size_mb
        );

        self.generate_tomoe_html(&output_dir, &dir_name, gallery)?;

        Ok(output_dir)
    }

    /// Generates `tomoe.html` summary document inside the gallery directory.
    fn generate_tomoe_html(
        &self,
        dir: &Path,
        dir_name: &str,
        gallery: &Gallery,
    ) -> Result<(), TomoeError> {
        let html_path = dir.join("tomoe.html");
        let mut file = File::create(&html_path)?;

        writeln!(file, "<html><center><body>")?;
        writeln!(file, "<h1>{}</h1>", gallery.id)?;

        for (idx, url) in gallery.images.iter().enumerate() {
            let filename = extract_filename(url, idx);
            writeln!(file, "<img src=\"{}/{}\"><p></p>", dir_name, filename)?;
        }

        writeln!(
            file,
            "<p><b><h1><a href=\"https://crates.io/crates/tomoe\">crates.io/crates/tomoe</a></b><h1>"
        )?;
        writeln!(file, "</body></center></html>")?;

        Ok(())
    }
}

/// Helper function to sanitize titles for filesystem directory creation.
fn sanitize_filename(name: &str) -> String {
    let cleaned = name
        .chars()
        .map(|c| {
            if c.is_alphanumeric() || c == '-' {
                c
            } else {
                ' '
            }
        })
        .collect::<String>();
    cleaned.split_whitespace().collect::<Vec<_>>().join("_")
}

/// Extracts a clean file name from an image URL or generates one based on index.
fn extract_filename(url: &str, idx: usize) -> String {
    if let Some(part) = url
        .rsplit('/')
        .next()
        .filter(|p| !p.is_empty() && p.contains('.'))
    {
        return part.to_string();
    }
    format!("{:03}.jpg", idx + 1)
}

/// Counts downloaded image files in directory.
fn count_downloaded_images(dir: &Path) -> Result<usize, TomoeError> {
    let mut count = 0;
    if dir.exists() {
        for entry in fs::read_dir(dir)? {
            let entry = entry?;
            let path = entry.path();
            let is_image = path.is_file()
                && path
                    .extension()
                    .map(|e| e.to_string_lossy().to_lowercase())
                    .map(|ext| ext == "jpg" || ext == "jpeg" || ext == "png" || ext == "webp")
                    .unwrap_or(false);
            if is_image {
                count += 1;
            }
        }
    }
    Ok(count)
}

/// Calculates total size of a directory in Megabytes.
fn calculate_dir_size_mb(dir: &Path) -> Result<f64, TomoeError> {
    let mut total_bytes: u64 = 0;
    if dir.exists() {
        for entry in fs::read_dir(dir)? {
            let entry = entry?;
            if entry.path().is_file() {
                total_bytes += entry.metadata()?.len();
            }
        }
    }
    Ok(total_bytes as f64 / 1024.0 / 1024.0)
}
