//! Project 016: Minimal JSON Field Extractor
//! Demonstrates zero-dependency JSON string lexing and property extraction.

use std::collections::HashMap;

#[derive(Debug, PartialEq, Clone)]
pub enum JsonValue {
    String(String),
    Number(f64),
    Bool(bool),
    Null,
}

pub fn parse_flat_json(input: &str) -> Result<HashMap<String, JsonValue>, String> {
    let mut map = HashMap::new();
    let trimmed = input.trim();
    if !trimmed.starts_with('{') || !trimmed.ends_with('}') {
        return Err("Input must be enclosed in braces {}".to_string());
    }

    let inner = &trimmed[1..trimmed.len() - 1].trim();
    if inner.is_empty() {
        return Ok(map);
    }

    for pair in inner.split(',') {
        let parts: Vec<&str> = pair.splitn(2, ':').collect();
        if parts.len() != 2 {
            return Err(format!("Invalid key-value pair: {}", pair));
        }
        let key = parts[0].trim().trim_matches('"').to_string();
        let val_str = parts[1].trim();

        let val = if val_str.starts_with('"') && val_str.ends_with('"') {
            JsonValue::String(val_str[1..val_str.len() - 1].to_string())
        } else if val_str == "true" {
            JsonValue::Bool(true)
        } else if val_str == "false" {
            JsonValue::Bool(false)
        } else if val_str == "null" {
            JsonValue::Null
        } else if let Ok(num) = val_str.parse::<f64>() {
            JsonValue::Number(num)
        } else {
            return Err(format!("Unrecognized value format: {}", val_str));
        };

        map.insert(key, val);
    }

    Ok(map)
}

fn main() {
    println!("=== 🦀 Project 016: Minimal JSON Field Extractor ===");
    let raw = r#"{"name": "Rust", "version": 2021, "awesome": true, "legacy": null}"#;
    let parsed = parse_flat_json(raw).unwrap();
    for (k, v) in parsed {
        println!("{:<10} => {:?}", k, v);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_json_parse() {
        let json = r#"{"title": "Book", "pages": 320, "published": true}"#;
        let map = parse_flat_json(json).unwrap();
        assert_eq!(map.get("title"), Some(&JsonValue::String("Book".to_string())));
        assert_eq!(map.get("pages"), Some(&JsonValue::Number(320.0)));
        assert_eq!(map.get("published"), Some(&JsonValue::Bool(true)));
    }
}
