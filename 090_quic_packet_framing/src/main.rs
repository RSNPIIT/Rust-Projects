//! Project 090: QUIC Variable-Length Integer & Framing
//! Demonstrates RFC 9000 variable-length integers and long packet header parsing.

pub fn encode_quic_varint(val: u64) -> Result<Vec<u8>, &'static str> {
    if val < (1 << 6) {
        Ok(vec![val as u8])
    } else if val < (1 << 14) {
        let v = (val as u16) | 0x4000;
        Ok(v.to_be_bytes().to_vec())
    } else if val < (1 << 30) {
        let v = (val as u32) | 0x80000000;
        Ok(v.to_be_bytes().to_vec())
    } else if val < (1 << 62) {
        let v = val | 0xC000000000000000;
        Ok(v.to_be_bytes().to_vec())
    } else {
        Err("Value exceeds 62 bits")
    }
}

pub fn decode_quic_varint(bytes: &[u8]) -> Result<(u64, usize), &'static str> {
    if bytes.is_empty() { return Err("Empty buffer"); }
    let prefix = bytes[0] >> 6;
    match prefix {
        0 => Ok((bytes[0] as u64, 1)),
        1 => {
            if bytes.len() < 2 { return Err("Truncated"); }
            let v = u16::from_be_bytes([bytes[0] & 0x3F, bytes[1]]) as u64;
            Ok((v, 2))
        }
        2 => {
            if bytes.len() < 4 { return Err("Truncated"); }
            let v = u32::from_be_bytes([bytes[0] & 0x3F, bytes[1], bytes[2], bytes[3]]) as u64;
            Ok((v, 4))
        }
        3 => {
            if bytes.len() < 8 { return Err("Truncated"); }
            let mut arr = [0u8; 8];
            arr.copy_from_slice(&bytes[0..8]);
            arr[0] &= 0x3F;
            Ok((u64::from_be_bytes(arr), 8))
        }
        _ => unreachable!(),
    }
}

fn main() {
    println!("=== 🦀 Project 090: QUIC Varint & Packet Framing ===");
    let numbers = [25u64, 15293, 494878333];
    for &n in &numbers {
        let encoded = encode_quic_varint(n).unwrap();
        let (decoded, len) = decode_quic_varint(&encoded).unwrap();
        println!("Value: {:<10} Encoded bytes: {:?} (len {}) => Decoded: {}", n, encoded, len, decoded);
        assert_eq!(n, decoded);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_quic_varint() {
        let enc = encode_quic_varint(494878333).unwrap();
        let (val, len) = decode_quic_varint(&enc).unwrap();
        assert_eq!(val, 494878333);
        assert_eq!(len, 4);
    }
}
