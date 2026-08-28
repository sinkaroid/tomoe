use crate::error::TomoeError;
use crate::models::{Gallery, JandaResponse};
use reqwest::Client;
use std::time::Duration;

/// Client for communicating with self-hosted or remote Jandapress API instances.
#[derive(Debug, Clone)]
pub struct JandaClient {
    client: Client,
    base_url: String,
}

impl JandaClient {
    /// Creates a new `JandaClient` with the given base URL.
    pub fn new(base_url: impl Into<String>) -> Result<Self, TomoeError> {
        let user_agent = format!("Tomoe/{} (Rust)", env!("CARGO_PKG_VERSION"));
        let client = Client::builder()
            .timeout(Duration::from_secs(30))
            .user_agent(user_agent)
            .build()?;

        let url = base_url.into().trim_end_matches('/').to_string();
        Ok(Self {
            client,
            base_url: url,
        })
    }

    /// Fetches gallery metadata for a specific provider and item ID/path.
    pub async fn get_gallery(&self, provider: &str, id: &str) -> Result<Gallery, TomoeError> {
        let clean_id = id.trim_start_matches('/');
        let endpoint = format!("{}/{}/get?book={}", self.base_url, provider, clean_id);
        let resp = self.client.get(&endpoint).send().await?;

        if !resp.status().is_success() {
            let status = resp.status();
            let body = resp.text().await.unwrap_or_default();
            return Err(TomoeError::ApiError {
                provider: provider.to_string(),
                id: id.to_string(),
                message: format!("HTTP {} - {}", status, body),
            });
        }

        let payload: JandaResponse = resp.json().await?;

        if let (Some(err_msg), None) = (payload.message, &payload.data) {
            return Err(TomoeError::ApiError {
                provider: provider.to_string(),
                id: id.to_string(),
                message: err_msg,
            });
        }

        let data = payload.data.ok_or_else(|| TomoeError::ApiError {
            provider: provider.to_string(),
            id: id.to_string(),
            message: "Missing 'data' field in Jandapress API response".to_string(),
        })?;

        let id_str = match data.id {
            serde_json::Value::Number(n) => n.to_string(),
            serde_json::Value::String(s) => s,
            other => other.to_string(),
        };

        let total = if data.total == 0 {
            data.image.len()
        } else {
            data.total
        };

        Ok(Gallery {
            provider: provider.to_string(),
            id: id_str,
            title: data.title,
            images: data.image,
            total,
            tags: data.tags,
        })
    }
}
