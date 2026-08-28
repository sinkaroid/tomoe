use clap::Parser;

/// Tomoe - A robust doujinshi downloader, uncompromising in efficiency.
#[derive(Parser, Debug, Clone)]
#[command(
    name = "tomoe",
    author = "sinkaroid",
    version = env!("CARGO_PKG_VERSION"),
    about = "A robust doujinshi downloader, uncompromising in efficiency",
    long_about = None
)]
pub struct Cli {
    /// Download galleries from nhentai by ID
    #[arg(long, num_args = 1..)]
    pub nhentai: Option<Vec<String>>,

    /// Download galleries from pururin by ID
    #[arg(long, num_args = 1..)]
    pub pururin: Option<Vec<String>>,

    /// Download galleries from hentaifox by ID
    #[arg(long, num_args = 1..)]
    pub hentaifox: Option<Vec<String>>,

    /// Download galleries from hentai2read by path (e.g., "chaldea_life/1")
    #[arg(long, num_args = 1..)]
    pub hentai2read: Option<Vec<String>>,

    /// Download galleries from simply-hentai by chapter path
    #[arg(long, num_args = 1..)]
    pub simply: Option<Vec<String>>,

    /// Download galleries from asmhentai by ID
    #[arg(long, num_args = 1..)]
    pub asmhentai: Option<Vec<String>>,

    /// Download galleries from 3hentai by ID
    #[arg(long = "3hentai", alias = "three", num_args = 1..)]
    pub three: Option<Vec<String>>,

    /// Bulk download using nested JSON file (e.g., "bulk.json")
    #[arg(long, value_name = "FILE")]
    pub bulk: Option<String>,

    /// Render downloaded images into PDF format automatically
    #[arg(long)]
    pub pdf: bool,

    /// Custom Jandapress server URL (bypasses local Podman self-hosting)
    #[arg(long = "jandapress_url", env = "JANDAPRESS_URL")]
    pub jandapress_url: Option<String>,

    /// Disable Podman auto-selfhosting check/launch
    #[arg(long = "no_selfhost")]
    pub no_selfhost: bool,

    /// Optional API key for nhentai official API
    #[arg(long = "nhentai_api_key", env = "NHENTAI_API_KEY")]
    pub nhentai_api_key: Option<String>,

    /// Stop and kill the local Jandapress Podman container (skip if already dead)
    #[arg(long = "kill_janda")]
    pub kill_janda: bool,

    /// Start the local Jandapress Podman container (skip if already alive)
    #[arg(long = "start_janda")]
    pub start_janda: bool,
}
