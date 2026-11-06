//! Project 096: TLS 1.3 ClientHello Record Parser
//! Demonstrates parsing TLS record headers and ClientHello handshake frames.

#[derive(Debug)]
pub struct TlsRecordHeader {
    pub content_type: u8,
    pub legacy_version: u16,
    pub length: u16,
}

pub fn parse_tls_record_header(buf: &[u8]) -> Result<TlsRecordHeader, &'static str> {
    if buf.len() < 5 { return Err("Buffer too short for TLS header"); }
    let content_type = buf[0];
    let legacy_version = u16::from_be_bytes([buf[1], buf[2]]);
    let length = u16::from_be_bytes([buf[3], buf[4]]);

    Ok(TlsRecordHeader { content_type, legacy_version, length })
}

fn main() {
    println!("=== 🦀 Project 096: TLS 1.3 Record Parser ===");
    let mock_tls_handshake = [
        0x16,       // ContentType: Handshake (22)
        0x03, 0x01, // Legacy Version: TLS 1.0 (0x0301)
        0x00, 0x20, // Length: 32 bytes
    ];

    let header = parse_tls_record_header(&mock_tls_handshake).unwrap();
    println!("Content Type: 0x{:02X} (22 = Handshake)", header.content_type);
    println!("Record Version: 0x{:04X}", header.legacy_version);
    println!("Payload Length: {} bytes", header.length);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tls_record() {
        let b = [0x16, 0x03, 0x03, 0x01, 0x00];
        let h = parse_tls_record_header(&b).unwrap();
        assert_eq!(h.content_type, 0x16);
        assert_eq!(h.length, 256);
    }
}
