use std::fmt;

/// Custom error types for Tomoe operations.
#[derive(Debug)]
pub enum TomoeError {
    PodmanNotFound,
    PodmanExecFailed(String),
    #[allow(dead_code)]
    ContainerStartFailed(String),
    ApiError {
        provider: String,
        id: String,
        message: String,
    },
    DownloadError {
        url: String,
        reason: String,
    },
    PdfError(String),
    InvalidBulkFile(String),
    Io(std::io::Error),
    Reqwest(reqwest::Error),
    Json(serde_json::Error),
}

impl fmt::Display for TomoeError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            TomoeError::PodmanNotFound => write!(
                f,
                "Podman CLI binary not found on host system. Please install podman or pass --jandapress_url"
            ),
            TomoeError::PodmanExecFailed(msg) => {
                write!(f, "Failed to execute podman command: {}", msg)
            }
            TomoeError::ContainerStartFailed(msg) => {
                write!(f, "Jandapress container failed to start: {}", msg)
            }
            TomoeError::ApiError {
                provider,
                id,
                message,
            } => write!(f, "Jandapress API error ({}/{}): {}", provider, id, message),
            TomoeError::DownloadError { url, reason } => {
                write!(f, "Failed to download image from {}: {}", url, reason)
            }
            TomoeError::PdfError(msg) => write!(f, "PDF generation failed: {}", msg),
            TomoeError::InvalidBulkFile(msg) => {
                write!(f, "Invalid bulk file configuration: {}", msg)
            }
            TomoeError::Io(err) => write!(f, "IO error: {}", err),
            TomoeError::Reqwest(err) => write!(f, "HTTP error: {}", err),
            TomoeError::Json(err) => write!(f, "JSON serialization/deserialization error: {}", err),
        }
    }
}

impl std::error::Error for TomoeError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            TomoeError::Io(err) => Some(err),
            TomoeError::Reqwest(err) => Some(err),
            TomoeError::Json(err) => Some(err),
            _ => None,
        }
    }
}

impl From<std::io::Error> for TomoeError {
    fn from(err: std::io::Error) -> Self {
        TomoeError::Io(err)
    }
}

impl From<reqwest::Error> for TomoeError {
    fn from(err: reqwest::Error) -> Self {
        TomoeError::Reqwest(err)
    }
}

impl From<serde_json::Error> for TomoeError {
    fn from(err: serde_json::Error) -> Self {
        TomoeError::Json(err)
    }
}
