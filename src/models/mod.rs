use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// Standardized Gallery struct used throughout Tomoe.
#[derive(Debug, Clone)]
pub struct Gallery {
    pub provider: String,
    pub id: String,
    pub title: String,
    pub images: Vec<String>,
    pub total: usize,
    pub tags: Vec<String>,
}

/// Raw payload returned by Jandapress API endpoints.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GalleryData {
    pub id: serde_json::Value,
    #[serde(default)]
    pub title: String,
    #[serde(default)]
    pub image: Vec<String>,
    #[serde(default)]
    pub total: usize,
    #[serde(default)]
    pub tags: Vec<String>,
}

/// API Response envelope from Jandapress.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct JandaResponse {
    pub status: Option<u16>,
    pub source: Option<String>,
    pub data: Option<GalleryData>,
    pub message: Option<String>,
}

/// Structure for bulk download JSON configurations (e.g. `bulk.json`).
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BulkConfig {
    pub book: Vec<HashMap<String, serde_json::Value>>,
}
