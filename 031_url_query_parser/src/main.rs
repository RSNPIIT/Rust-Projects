//! Project 031: URL Query String Parser & Encoder
//! Demonstrates URL decoding, percent-encoding, and query string parsing.

use std::collections::HashMap;

pub fn url_decode(s: &str) -> String {
    let mut out = Vec::new();
    let bytes = s.as_bytes();
    let mut i = 0;
    while i < bytes.len() {
        if bytes[i] == b'%' && i + 2 < bytes.len() {
            if let Ok(h) = u8::from_str_radix(std::str::from_utf8(&bytes[i + 1..i + 3]).unwrap_or(""), 16) {
                out.push(h);
                i += 3;
                continue;
            }
        } else if bytes[i] == b'+' {
            out.push(b' ');
            i += 1;
            continue;
        }
        out.push(bytes[i]);
        i += 1;
    }
    String::from_utf8_lossy(&out).to_string()
}

pub fn parse_query(query: &str) -> HashMap<String, String> {
    let mut params = HashMap::new();
    let raw_query = query.split_once('?').map_or(query, |(_, q)| q);
    for pair in raw_query.split('&') {
        if pair.is_empty() { continue; }
        if let Some((k, v)) = pair.split_once('=') {
            params.insert(url_decode(k), url_decode(v));
        } else {
            params.insert(url_decode(pair), String::new());
        }
    }
    params
}

fn main() {
    println!("=== 🦀 Project 031: URL Query String Parser ===");
    let url = "https://example.com/search?query=rust+programming&category=dev%26code&page=1";
    let params = parse_query(url);
    for (k, v) in params {
        println!("{:>10} : {}", k, v);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_query_parsing() {
        let q = "name=John+Doe&city=New%20York";
        let parsed = parse_query(q);
        assert_eq!(parsed.get("name"), Some(&"John Doe".to_string()));
        assert_eq!(parsed.get("city"), Some(&"New York".to_string()));
    }
}
