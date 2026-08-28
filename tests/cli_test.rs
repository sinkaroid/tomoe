use clap::Parser;
use tomoe::cli::Cli;

#[test]
fn test_cli_parsing_nhentai() {
    let args = vec!["tomoe", "--nhentai", "255369", "--pdf"];
    let cli = Cli::try_parse_from(args).expect("Should parse nhentai args");

    assert_eq!(cli.nhentai, Some(vec!["255369".to_string()]));
    assert!(cli.pdf);
}

#[test]
fn test_cli_parsing_pururin() {
    let args = vec!["tomoe", "--pururin", "47226"];
    let cli = Cli::try_parse_from(args).expect("Should parse pururin args");

    assert_eq!(cli.pururin, Some(vec!["47226".to_string()]));
}

#[test]
fn test_cli_parsing_hentaifox() {
    let args = vec!["tomoe", "--hentaifox", "59026"];
    let cli = Cli::try_parse_from(args).expect("Should parse hentaifox args");

    assert_eq!(cli.hentaifox, Some(vec!["59026".to_string()]));
}

#[test]
fn test_cli_parsing_asmhentai() {
    let args = vec!["tomoe", "--asmhentai", "311851"];
    let cli = Cli::try_parse_from(args).expect("Should parse asmhentai args");

    assert_eq!(cli.asmhentai, Some(vec!["311851".to_string()]));
}

#[test]
fn test_cli_parsing_hentai2read() {
    let args = vec!["tomoe", "--hentai2read", "chaldea_life/1"];
    let cli = Cli::try_parse_from(args).expect("Should parse hentai2read args");

    assert_eq!(cli.hentai2read, Some(vec!["chaldea_life/1".to_string()]));
}

#[test]
fn test_cli_parsing_simply() {
    let args = vec![
        "tomoe",
        "--simply",
        "fate-grand-order/fgo-no-ashibon-fgo-foot-book/all-pages",
    ];
    let cli = Cli::try_parse_from(args).expect("Should parse simply args");

    assert_eq!(
        cli.simply,
        Some(vec![
            "fate-grand-order/fgo-no-ashibon-fgo-foot-book/all-pages".to_string()
        ])
    );
}

#[test]
fn test_cli_parsing_3hentai() {
    let args = vec!["tomoe", "--3hentai", "608979"];
    let cli = Cli::try_parse_from(args).expect("Should parse 3hentai args");

    assert_eq!(cli.three, Some(vec!["608979".to_string()]));

    // Test alias --three
    let alias_args = vec!["tomoe", "--three", "608979"];
    let alias_cli = Cli::try_parse_from(alias_args).expect("Should parse three alias args");

    assert_eq!(alias_cli.three, Some(vec!["608979".to_string()]));
}

#[test]
fn test_cli_parsing_bulk() {
    let args = vec!["tomoe", "--bulk", "a.json"];
    let cli = Cli::try_parse_from(args).expect("Should parse bulk arg");

    assert_eq!(cli.bulk, Some("a.json".to_string()));
}

#[test]
fn test_cli_parsing_admin_flags() {
    let args = vec![
        "tomoe",
        "--kill_janda",
        "--start_janda",
        "--no_selfhost",
        "--jandapress_url",
        "http://localhost:2002",
        "--nhentai_api_key",
        "secret_key",
    ];
    let cli = Cli::try_parse_from(args).expect("Should parse admin flags");

    assert!(cli.kill_janda);
    assert!(cli.start_janda);
    assert!(cli.no_selfhost);
    assert_eq!(
        cli.jandapress_url,
        Some("http://localhost:2002".to_string())
    );
    assert_eq!(cli.nhentai_api_key, Some("secret_key".to_string()));
}
