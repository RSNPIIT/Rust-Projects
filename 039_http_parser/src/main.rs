//! Project 039: RFC 7230 HTTP/1.1 Parser
//! Demonstrates zero-copy header parsing and HTTP request decoding.

use std::collections::HashMap;

#[derive(Debug, PartialEq)]
pub struct HttpRequest<'a> {
    pub method: &'a str,
    pub path: &'a str,
    pub version: &'a str,
    pub headers: HashMap<&'a str, &'a str>,
    pub body: &'a str,
}

pub fn parse_http_request(raw: &str) -> Result<HttpRequest<'_>, &'static str> {
    let (header_part, body) = raw.split_once("\r\n\r\n").or_else(|| raw.split_once("\n\n")).ok_or("Malformed HTTP request: missing separator")?;
    let mut lines = header_part.lines();
    let request_line = lines.next().ok_or("Empty request")?;

    let parts: Vec<&str> = request_line.split_whitespace().collect();
    if parts.len() != 3 {
        return Err("Invalid HTTP request line");
    }

    let mut headers = HashMap::new();
    for line in lines {
        if let Some((k, v)) = line.split_once(':') {
            headers.insert(k.trim(), v.trim());
        }
    }

    Ok(HttpRequest {
        method: parts[0],
        path: parts[1],
        version: parts[2],
        headers,
        body,
    })
}

fn main() {
    println!("=== 🦀 Project 039: RFC 7230 HTTP/1.1 Parser ===");
    let raw = "GET /api/v1/users?page=2 HTTP/1.1\r\n\
               Host: localhost:8080\r\n\
               User-Agent: RustClient/1.0\r\n\
               Content-Type: application/json\r\n\
               \r\n\
               {\"query\": \"rust\"}";

    let req = parse_http_request(raw).unwrap();
    println!("Method:  {}", req.method);
    println!("Path:    {}", req.path);
    println!("Version: {}", req.version);
    println!("Headers: {:?}", req.headers);
    println!("Body:    {}", req.body);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_http_request() {
        let raw = "POST /submit HTTP/1.1\r\nContent-Length: 4\r\n\r\nping";
        let req = parse_http_request(raw).unwrap();
        assert_eq!(req.method, "POST");
        assert_eq!(req.path, "/submit");
        assert_eq!(req.body, "ping");
    }
}
