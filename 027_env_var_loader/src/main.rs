//! Project 027: Dotenv File Parser
//! Demonstrates file parsing, comment stripping, and environment map generation.

use std::collections::HashMap;

pub fn parse_dotenv_content(content: &str) -> HashMap<String, String> {
    let mut map = HashMap::new();
    for line in content.lines() {
        let line = line.trim();
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        if let Some((key, val)) = line.split_once('=') {
            let key = key.trim().to_string();
            let mut val = val.trim();
            if (val.starts_with('"') && val.ends_with('"')) || (val.starts_with('\'') && val.ends_with('\'')) {
                if val.len() >= 2 {
                    val = &val[1..val.len() - 1];
                }
            }
            map.insert(key, val.to_string());
        }
    }
    map
}

fn main() {
    println!("=== 🦀 Project 027: Dotenv File Parser ===");
    let sample_env = "
        # Database Settings
        DB_HOST=127.0.0.1
        DB_PORT=5432
        DB_USER=\"postgres_admin\"
        APP_DEBUG=true
    ";
    let vars = parse_dotenv_content(sample_env);
    for (k, v) in vars {
        println!("{:>12} = {}", k, v);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_env() {
        let content = "# Comment\nKEY=VALUE\nPORT=\"8080\"";
        let parsed = parse_dotenv_content(content);
        assert_eq!(parsed.get("KEY"), Some(&"VALUE".to_string()));
        assert_eq!(parsed.get("PORT"), Some(&"8080".to_string()));
    }
}
