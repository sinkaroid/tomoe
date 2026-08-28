use tomoe::models::BulkConfig;

#[test]
fn test_bulk_json_deserialization() {
    let json_data = r#"{
        "book": [
            { "nhentai": 255369 },
            { "pururin": 47226 },
            { "hentai2read": "chaldea_life/1" }
        ]
    }"#;

    let config: BulkConfig = serde_json::from_str(json_data).expect("Should deserialize bulk json");
    assert_eq!(config.book.len(), 3);
    assert!(config.book[0].contains_key("nhentai"));
    assert!(config.book[1].contains_key("pururin"));
    assert!(config.book[2].contains_key("hentai2read"));
}
