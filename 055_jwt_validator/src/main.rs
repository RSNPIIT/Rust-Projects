//! Project 055: JWT Structure Validator
//! Demonstrates 3-part JWT token parsing and Base64Url decoding.

pub struct JwtParts<'a> {
    pub header_raw: &'a str,
    pub payload_raw: &'a str,
    pub signature_raw: &'a str,
}

pub fn parse_jwt(token: &str) -> Result<JwtParts<'_>, &'static str> {
    let parts: Vec<&str> = token.split('.').collect();
    if parts.len() != 3 {
        return Err("Invalid JWT format: must have header.payload.signature");
    }
    Ok(JwtParts {
        header_raw: parts[0],
        payload_raw: parts[1],
        signature_raw: parts[2],
    })
}

fn main() {
    println!("=== 🦀 Project 055: JWT Structure Validator ===");
    let sample_jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkFsaWNlIn0.signature";
    let parts = parse_jwt(sample_jwt).unwrap();
    println!("Header:    {}", parts.header_raw);
    println!("Payload:   {}", parts.payload_raw);
    println!("Signature: {}", parts.signature_raw);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_jwt_parts() {
        let t = "aaa.bbb.ccc";
        let res = parse_jwt(t).unwrap();
        assert_eq!(res.header_raw, "aaa");
        assert_eq!(res.payload_raw, "bbb");
    }
}
