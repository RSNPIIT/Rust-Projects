//! Project 065: Binary DNS Packet Parser
//! Demonstrates RFC 1035 DNS header flags and question label parsing.

#[derive(Debug)]
pub struct DnsHeader {
    pub id: u16,
    pub is_response: bool,
    pub question_count: u16,
    pub answer_count: u16,
}

pub fn parse_dns_header(buf: &[u8]) -> Result<DnsHeader, &'static str> {
    if buf.len() < 12 {
        return Err("Buffer too short for DNS header");
    }
    let id = u16::from_be_bytes([buf[0], buf[1]]);
    let flags = u16::from_be_bytes([buf[2], buf[3]]);
    let is_response = (flags & 0x8000) != 0;
    let question_count = u16::from_be_bytes([buf[4], buf[5]]);
    let answer_count = u16::from_be_bytes([buf[6], buf[7]]);

    Ok(DnsHeader { id, is_response, question_count, answer_count })
}

pub fn parse_dns_domain(buf: &[u8], mut offset: usize) -> Result<(String, usize), &'static str> {
    let mut parts = Vec::new();
    while offset < buf.len() {
        let len = buf[offset] as usize;
        if len == 0 {
            offset += 1;
            break;
        }
        offset += 1;
        if offset + len > buf.len() {
            return Err("Label exceeds buffer");
        }
        let part = std::str::from_utf8(&buf[offset..offset + len]).map_err(|_| "Invalid UTF-8")?;
        parts.push(part);
        offset += len;
    }
    Ok((parts.join("."), offset))
}

fn main() {
    println!("=== 🦀 Project 065: Binary DNS Packet Parser ===");
    let mut packet = vec![
        0x1A, 0x2B, // ID: 0x1A2B
        0x01, 0x00, // Standard query
        0x00, 0x01, // QDCOUNT: 1
        0x00, 0x00, // ANCOUNT: 0
        0x00, 0x00, // NSCOUNT: 0
        0x00, 0x00, // ARCOUNT: 0
        // QNAME: \x06google\x03com\x00
        6, b'g', b'o', b'o', b'g', b'l', b'e',
        3, b'c', b'o', b'm',
        0,
    ];

    let header = parse_dns_header(&packet).unwrap();
    println!("Parsed Header: {:?}", header);
    let (domain, _) = parse_dns_domain(&packet, 12).unwrap();
    println!("Queried Domain: {}", domain);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_dns_header() {
        let bytes = [0x12, 0x34, 0x80, 0x00, 0x00, 0x01, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00];
        let h = parse_dns_header(&bytes).unwrap();
        assert_eq!(h.id, 0x1234);
        assert!(h.is_response);
        assert_eq!(h.question_count, 1);
        assert_eq!(h.answer_count, 2);
    }
}
