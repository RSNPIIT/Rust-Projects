//! Project 021: Run-Length Encoding (RLE)
//! Demonstrates lossless stream compression and decompression.

pub fn encode_rle(input: &str) -> String {
    if input.is_empty() {
        return String::new();
    }
    let mut encoded = String::new();
    let mut chars = input.chars().peekable();

    while let Some(current) = chars.next() {
        let mut count = 1;
        while chars.peek() == Some(&current) {
            count += 1;
            chars.next();
        }
        encoded.push_str(&format!("{}{}", count, current));
    }
    encoded
}

pub fn decode_rle(encoded: &str) -> Result<String, &'static str> {
    let mut decoded = String::new();
    let mut count_str = String::new();

    for c in encoded.chars() {
        if c.is_digit(10) {
            count_str.push(c);
        } else {
            let count: usize = count_str.parse().map_err(|_| "Malformed RLE number")?;
            count_str.clear();
            for _ in 0..count {
                decoded.push(c);
            }
        }
    }
    Ok(decoded)
}

fn main() {
    println!("=== 🦀 Project 021: Run-Length Encoding ===");
    let original = "WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWB";
    let encoded = encode_rle(original);
    let decoded = decode_rle(&encoded).unwrap();

    println!("Original:  {} (len: {})", original, original.len());
    println!("Encoded:   {} (len: {})", encoded, encoded.len());
    println!("Decoded:   {}", decoded);
    assert_eq!(original, decoded);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_rle_roundtrip() {
        let s = "AAAAABBBCCDAA";
        let enc = encode_rle(s);
        assert_eq!(enc, "5A3B2C1D2A");
        assert_eq!(decode_rle(&enc).unwrap(), s);
    }
}
