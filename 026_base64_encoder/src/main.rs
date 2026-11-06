//! Project 026: Base64 Encoder & Decoder
//! Demonstrates bit manipulation, chunking, and RFC 4648 Base64 logic.

const BASE64_CHARS: &[u8; 64] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

pub fn encode_base64(data: &[u8]) -> String {
    let mut result = String::new();
    for chunk in data.chunks(3) {
        let b0 = chunk[0];
        let b1 = if chunk.len() > 1 { chunk[1] } else { 0 };
        let b2 = if chunk.len() > 2 { chunk[2] } else { 0 };

        let idx0 = (b0 >> 2) as usize;
        let idx1 = (((b0 & 0x03) << 4) | (b1 >> 4)) as usize;
        let idx2 = (((b1 & 0x0F) << 2) | (b2 >> 6)) as usize;
        let idx3 = (b2 & 0x3F) as usize;

        result.push(BASE64_CHARS[idx0] as char);
        result.push(BASE64_CHARS[idx1] as char);

        if chunk.len() == 1 {
            result.push_str("==");
        } else if chunk.len() == 2 {
            result.push(BASE64_CHARS[idx2] as char);
            result.push('=');
        } else {
            result.push(BASE64_CHARS[idx2] as char);
            result.push(BASE64_CHARS[idx3] as char);
        }
    }
    result
}

fn decode_char(c: u8) -> Option<u8> {
    match c {
        b'A'..=b'Z' => Some(c - b'A'),
        b'a'..=b'z' => Some(c - b'a' + 26),
        b'0'..=b'9' => Some(c - b'0' + 52),
        b'+' => Some(62),
        b'/' => Some(63),
        _ => None,
    }
}

pub fn decode_base64(encoded: &str) -> Result<Vec<u8>, &'static str> {
    let clean: Vec<u8> = encoded.bytes().filter(|&b| b != b'=' && !b.is_ascii_whitespace()).collect();
    let mut out = Vec::new();

    for chunk in clean.chunks(4) {
        let mut buf = [0u8; 4];
        for (i, &b) in chunk.iter().enumerate() {
            buf[i] = decode_char(b).ok_or("Invalid base64 character")?;
        }

        let b0 = (buf[0] << 2) | (buf[1] >> 4);
        out.push(b0);

        if chunk.len() > 2 {
            let b1 = ((buf[1] & 0x0F) << 4) | (buf[2] >> 2);
            out.push(b1);
        }
        if chunk.len() > 3 {
            let b2 = ((buf[2] & 0x03) << 6) | buf[3];
            out.push(b2);
        }
    }
    Ok(out)
}

fn main() {
    println!("=== 🦀 Project 026: Base64 Encoder & Decoder ===");
    let msg = "Rustaceans are awesome!";
    let encoded = encode_base64(msg.as_bytes());
    let decoded = decode_base64(&encoded).unwrap();
    let recovered = String::from_utf8(decoded).unwrap();

    println!("Original:  {}", msg);
    println!("Encoded:   {}", encoded);
    println!("Recovered: {}", recovered);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_base64() {
        assert_eq!(encode_base64(b"Man"), "TWFu");
        assert_eq!(decode_base64("TWFu").unwrap(), b"Man");
    }
}
