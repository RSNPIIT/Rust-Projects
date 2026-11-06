//! Project 012: File Metadata Inspector
//! Demonstrates filesystem inspection and human-readable byte calculations.

use std::path::Path;

pub fn format_bytes(bytes: u64) -> String {
    const KB: u64 = 1024;
    const MB: u64 = KB * 1024;
    const GB: u64 = MB * 1024;

    if bytes >= GB {
        format!("{:.2} GB", bytes as f64 / GB as f64)
    } else if bytes >= MB {
        format!("{:.2} MB", bytes as f64 / MB as f64)
    } else if bytes >= KB {
        format!("{:.2} KB", bytes as f64 / KB as f64)
    } else {
        format!("{} B", bytes)
    }
}

pub struct FileInfo {
    pub file_name: String,
    pub extension: String,
    pub simulated_size: u64,
}

impl FileInfo {
    pub fn inspect_path(p: &Path, simulated_size: u64) -> Self {
        Self {
            file_name: p.file_name().and_then(|n| n.to_str()).unwrap_or("unknown").to_string(),
            extension: p.extension().and_then(|e| e.to_str()).unwrap_or("none").to_string(),
            simulated_size,
        }
    }
}

fn main() {
    println!("=== 🦀 Project 012: File Metadata Inspector ===");
    let paths = [
        ("src/main.rs", 2450),
        ("assets/archive.tar.gz", 15482390),
        ("videos/presentation.mp4", 1854923847),
    ];

    for (p, size) in paths {
        let info = FileInfo::inspect_path(Path::new(p), size);
        println!("File: {:<25} Ext: {:<5} Size: {}", info.file_name, info.extension, format_bytes(info.simulated_size));
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_format_bytes() {
        assert_eq!(format_bytes(500), "500 B");
        assert_eq!(format_bytes(1024), "1.00 KB");
        assert_eq!(format_bytes(1048576), "1.00 MB");
    }
}
