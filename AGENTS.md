# AGENTS.md

### 1. Architecture & Concurrency

- Utilize `tokio` multi-threaded runtime with `tokio::spawn` and `Semaphore` for concurrent image fetching.
- Use `reqwest::Client` connection pooling for HTTP requests.
- Automate Podman container (`ghcr.io/sinkaroid/jandapress:latest`) lifecycle checks at `http://localhost:2002`.

### 2. Error Handling & Logging

- Avoid `panic!`, `unwrap()`, or `expect()` in production code paths.
- Use native Rust error handling (`std::error::Error`, `std::fmt::Display`) in `src/error.rs`.
- Use the native ISO 8601 logger macros in `src/logger.rs`.

### 3. Dependency Policy

- Maintain a minimal dependency footprint (`tokio`, `clap`, `reqwest`, `serde`, `serde_json`, `printpdf`).

### 4. Verification Workflow

- **Check**: `cargo check`
- **Lint**: `cargo clippy -- -D warnings`
- **Format**: `cargo fmt`
- **Test**: `cargo test`
