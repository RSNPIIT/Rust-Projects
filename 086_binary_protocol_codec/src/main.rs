//! Project 086: High-Performance TLV Binary Codec
//! Demonstrates TLV framing, packet encoding, and decoding.

#[derive(Debug, PartialEq, Clone)]
pub struct TlvPacket {
    pub tag: u16,
    pub value: Vec<u8>,
}

impl TlvPacket {
    pub fn encode(&self) -> Vec<u8> {
        let mut buf = Vec::new();
        buf.extend_from_slice(&self.tag.to_be_bytes());
        buf.extend_from_slice(&(self.value.len() as u32).to_be_bytes());
        buf.extend_from_slice(&self.value);
        buf
    }

    pub fn decode(bytes: &[u8]) -> Result<Self, &'static str> {
        if bytes.len() < 6 { return Err("Buffer too short for TLV header"); }
        let tag = u16::from_be_bytes([bytes[0], bytes[1]]);
        let len = u32::from_be_bytes([bytes[2], bytes[3], bytes[4], bytes[5]]) as usize;
        if bytes.len() < 6 + len { return Err("Payload truncated"); }
        let value = bytes[6..6 + len].to_vec();
        Ok(Self { tag, value })
    }
}

fn main() {
    println!("=== 🦀 Project 086: TLV Binary Codec ===");
    let pkt = TlvPacket { tag: 0x0101, value: b"AUTH_REQUEST".to_vec() };
    let wire = pkt.encode();
    println!("Wire bytes: {:?}", wire);
    let decoded = TlvPacket::decode(&wire).unwrap();
    println!("Decoded Tag: 0x{:04X}, Value: {}", decoded.tag, String::from_utf8_lossy(&decoded.value));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tlv_codec() {
        let p = TlvPacket { tag: 10, value: vec![1, 2, 3] };
        let enc = p.encode();
        let dec = TlvPacket::decode(&enc).unwrap();
        assert_eq!(p, dec);
    }
}
