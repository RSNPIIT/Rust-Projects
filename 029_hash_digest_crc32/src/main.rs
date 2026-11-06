//! Project 029: CRC-32 Checksum Digest
//! Demonstrates IEEE 802.3 polynomial cyclic redundancy check.

pub struct Crc32 {
    table: [u32; 256],
}

impl Crc32 {
    pub const fn new() -> Self {
        let mut table = [0u32; 256];
        let poly = 0xEDB88320u32;
        let mut i = 0;
        while i < 256 {
            let mut crc = i as u32;
            let mut j = 0;
            while j < 8 {
                if (crc & 1) != 0 {
                    crc = (crc >> 1) ^ poly;
                } else {
                    crc >>= 1;
                }
                j += 1;
            }
            table[i] = crc;
            i += 1;
        }
        Self { table }
    }

    pub fn checksum(&self, bytes: &[u8]) -> u32 {
        let mut crc = 0xFFFFFFFFu32;
        for &b in bytes {
            let idx = ((crc ^ (b as u32)) & 0xFF) as usize;
            crc = (crc >> 8) ^ self.table[idx];
        }
        crc ^ 0xFFFFFFFFu32
    }
}

fn main() {
    println!("=== 🦀 Project 029: CRC-32 Checksum Digest ===");
    let crc = Crc32::new();
    let data = b"123456789";
    let hash = crc.checksum(data);
    println!("CRC-32(\"{}\") = 0x{:08X}", String::from_utf8_lossy(data), hash);
    assert_eq!(hash, 0xCBF43926);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_crc32_standard() {
        let crc = Crc32::new();
        assert_eq!(crc.checksum(b"123456789"), 0xCBF43926);
    }
}
