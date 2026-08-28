use crate::error::TomoeError;
use crate::{info, warn};
use std::process::Command;
use std::time::Duration;

pub const DEFAULT_JANDAPRESS_URL: &str = "http://localhost:2002";
pub const CONTAINER_NAME: &str = "tomoe-jandapress";
pub const CONTAINER_IMAGE: &str = "ghcr.io/sinkaroid/jandapress:latest";

/// Checks if the `podman` command-line executable exists on the host system.
pub fn is_podman_available() -> bool {
    let output = if cfg!(target_os = "windows") {
        Command::new("cmd")
            .args(["/C", "podman --version"])
            .output()
    } else {
        Command::new("podman").arg("--version").output()
    };

    match output {
        Ok(out) => out.status.success(),
        Err(_) => false,
    }
}

/// Ensures that the Jandapress API service is available.
/// If `url_override` is provided, skips container orchestration and uses the custom URL.
/// Otherwise, uses Podman to pull/start the `ghcr.io/sinkaroid/jandapress` container.
pub async fn ensure_jandapress(
    url_override: Option<&str>,
    no_selfhost: bool,
    nhentai_api_key: Option<&str>,
) -> Result<String, TomoeError> {
    if let Some(url) = url_override {
        let trimmed = url.trim_end_matches('/');
        info!("Using custom Jandapress URL: {}", trimmed);
        return Ok(trimmed.to_string());
    }

    if no_selfhost {
        info!(
            "Podman auto-selfhosting disabled by flag. Using default endpoint {}",
            DEFAULT_JANDAPRESS_URL
        );
        return Ok(DEFAULT_JANDAPRESS_URL.to_string());
    }

    if !is_podman_available() {
        return Err(TomoeError::PodmanNotFound);
    }

    info!("Podman CLI detected. Checking Jandapress container status...");

    let mut ps_running = run_cmd("podman", &["ps", "--format", "{{.Names}}"]);

    if let Err(ref e) = ps_running {
        let err_str = e.to_string();
        if err_str.contains("Cannot connect to Podman")
            || err_str.contains("unable to connect")
            || err_str.contains("dead network")
            || err_str.contains("podman.sock")
        {
            info!("Podman machine connection failure detected. Orchestrating auto-start...");
            let start_res = run_cmd("podman", &["machine", "start"]);

            if let Err(ref start_err) = start_res {
                let start_err_str = start_err.to_string();
                if start_err_str.contains("does not exist")
                    || start_err_str.contains("no machine")
                    || start_err_str.contains("initialize")
                    || start_err_str.contains("not found")
                {
                    info!("No Podman machine found. Initializing a new Podman machine VM...");
                    if let Err(init_err) = run_cmd("podman", &["machine", "init"]) {
                        warn!("Failed to initialize podman machine: {}", init_err);
                        return Err(TomoeError::PodmanExecFailed(format!(
                            "Failed to auto-initialize Podman machine: {}",
                            init_err
                        )));
                    }
                    info!("Podman machine VM initialized successfully. Starting machine...");
                    if let Err(second_start) = run_cmd("podman", &["machine", "start"]) {
                        warn!(
                            "Failed to start podman machine after initialization: {}",
                            second_start
                        );
                    }
                } else {
                    warn!("Failed to start podman machine: {}", start_err);
                }
            }

            info!("Waiting 10 seconds for Podman VM machine to boot up...");
            tokio::time::sleep(Duration::from_secs(10)).await;
            ps_running = run_cmd("podman", &["ps", "--format", "{{.Names}}"]);
        }
    }

    let ps_running = ps_running?;
    let mut is_running = ps_running.lines().any(|line| line.trim() == CONTAINER_NAME);

    if let (true, Some(host_key)) = (is_running, nhentai_api_key) {
        let container_key = get_container_nhentai_api_key();
        if container_key.as_deref() != Some(host_key) {
            info!("NHENTAI_API_KEY mismatch. Re-creating Jandapress container...");
            let _ = run_cmd("podman", &["rm", "-f", CONTAINER_NAME])?;
            is_running = false;
        }
    }

    if !is_running {
        let ps_all = run_cmd("podman", &["ps", "-a", "--format", "{{.Names}}"])?;
        let exists = ps_all.lines().any(|line| line.trim() == CONTAINER_NAME);

        if exists {
            if nhentai_api_key.is_some() {
                info!(
                    "Container '{}' exists but has outdated config. Re-creating to apply key...",
                    CONTAINER_NAME
                );
                let _ = run_cmd("podman", &["rm", "-f", CONTAINER_NAME])?;
                launch_new_container(nhentai_api_key)?;
            } else {
                info!(
                    "Container '{}' exists but is stopped. Starting container...",
                    CONTAINER_NAME
                );
                let _ = run_cmd("podman", &["start", CONTAINER_NAME])?;
            }
        } else {
            launch_new_container(nhentai_api_key)?;
        }
    } else {
        info!("Container '{}' is already running.", CONTAINER_NAME);
    }

    wait_for_health(DEFAULT_JANDAPRESS_URL, Duration::from_secs(15)).await?;

    Ok(DEFAULT_JANDAPRESS_URL.to_string())
}

/// Helper function to launch a new Jandapress container with optional NHENTAI_API_KEY
fn launch_new_container(nhentai_api_key: Option<&str>) -> Result<(), TomoeError> {
    info!(
        "Pulling and launching Jandapress container '{}' from {}...",
        CONTAINER_NAME, CONTAINER_IMAGE
    );
    let mut run_args = vec![
        "run".to_string(),
        "-d".to_string(),
        "-p".to_string(),
        "2002:3000".to_string(),
    ];
    if let Some(key) = nhentai_api_key {
        run_args.push("-e".to_string());
        run_args.push(format!("NHENTAI_API_KEY={}", key));
    }
    run_args.push("--name".to_string());
    run_args.push(CONTAINER_NAME.to_string());
    run_args.push(CONTAINER_IMAGE.to_string());

    let run_args_refs: Vec<&str> = run_args.iter().map(|s| s.as_str()).collect();
    run_cmd("podman", &run_args_refs)?;
    Ok(())
}

/// Helper function to inspect the container env variables and extract NHENTAI_API_KEY
fn get_container_nhentai_api_key() -> Option<String> {
    if let Ok(inspect) = run_cmd("podman", &["inspect", CONTAINER_NAME]) {
        for line in inspect.lines() {
            let trimmed = line.trim();
            if trimmed.starts_with("\"NHENTAI_API_KEY=") {
                let cleaned = trimmed
                    .trim_start_matches('"')
                    .trim_end_matches(',')
                    .trim_end_matches('"');
                if let Some(val) = cleaned.strip_prefix("NHENTAI_API_KEY=") {
                    return Some(val.to_string());
                }
            }
        }
    }
    None
}

/// Helper function to execute shell/podman commands safely.
fn run_cmd(cmd: &str, args: &[&str]) -> Result<String, TomoeError> {
    let output = if cfg!(target_os = "windows") {
        let mut full_cmd = vec![cmd];
        full_cmd.extend(args);
        Command::new("cmd")
            .args(["/C", &full_cmd.join(" ")])
            .output()
    } else {
        Command::new(cmd).args(args).output()
    };

    match output {
        Ok(out) => {
            if out.status.success() {
                Ok(String::from_utf8_lossy(&out.stdout).to_string())
            } else {
                let stderr = String::from_utf8_lossy(&out.stderr);
                Err(TomoeError::PodmanExecFailed(stderr.trim().to_string()))
            }
        }
        Err(e) => Err(TomoeError::PodmanExecFailed(e.to_string())),
    }
}

/// Polls the Jandapress API endpoint until it responds or timeouts.
async fn wait_for_health(url: &str, timeout: Duration) -> Result<(), TomoeError> {
    let client = reqwest::Client::builder()
        .timeout(Duration::from_secs(3))
        .build()?;

    let start = std::time::Instant::now();
    info!(
        "Waiting for Jandapress container health check at {}...",
        url
    );

    while start.elapsed() < timeout {
        if let Ok(res) = client.get(url).send().await {
            let status = res.status().as_u16();
            if res.status().is_success() || status == 404 || status == 200 {
                info!("Jandapress container is online and healthy!");
                return Ok(());
            }
        }
        tokio::time::sleep(Duration::from_millis(800)).await;
    }

    warn!("Jandapress health check polling reached timeout, but proceeding with queries.");
    Ok(())
}

/// Stops and removes the Jandapress container if it exists.
pub fn kill_jandapress() -> Result<(), TomoeError> {
    info!("Checking if Jandapress container is running...");
    if !is_podman_available() {
        return Err(TomoeError::PodmanNotFound);
    }
    let ps_all = run_cmd("podman", &["ps", "-a", "--format", "{{.Names}}"])?;
    let exists = ps_all.lines().any(|line| line.trim() == CONTAINER_NAME);
    if exists {
        info!(
            "Stopping and removing Jandapress container '{}'...",
            CONTAINER_NAME
        );
        let _ = run_cmd("podman", &["rm", "-f", CONTAINER_NAME])?;
        info!("Jandapress container killed successfully.");
    } else {
        info!("Jandapress container is already dead/not found.");
    }
    Ok(())
}
