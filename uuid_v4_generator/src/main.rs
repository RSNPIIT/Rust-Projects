//! Project 057: RFC 4122 UUID v4 Generator
//! Demonstrates 128-bit UUID generation with standard version and variant bits.

pub struct Uuid([u8; 16]);

impl Uuid {
    pub fn new_v4(seed: u64) -> Self {
        let mut bytes = [0u8; 16];
        let mut s = seed;
        for i in 0..16 {
            s = s.wrapping_mul(6364136223846793005).wrapping_add(1);
            bytes[i] = (s >> 32) as u8;
        }

        // Set version 4: bits 4-7 of time_hi_and_version to 0100
        bytes[6] = (bytes[6] & 0x0F) | 0x40;
        // Set variant RFC 4122: bits 6-7 of clock_seq_hi_and_reserved to 10
        bytes[8] = (bytes[8] & 0x3F) | 0x80;

        Uuid(bytes)
    }

    pub fn to_string(&self) -> String {
        format!(
            "{:02x}{:02x}{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}",
            self.0[0], self.0[1], self.0[2], self.0[3],
            self.0[4], self.0[5],
            self.0[6], self.0[7],
            self.0[8], self.0[9],
            self.0[10], self.0[11], self.0[12], self.0[13], self.0[14], self.0[15]
        )
    }
}

fn main() {
    println!("=== 🦀 Project 057: RFC 4122 UUID v4 Generator ===");
    for i in 1..=3 {
        let uuid = Uuid::new_v4(42 + i * 100);
        println!("Generated UUID #{}: {}", i, uuid.to_string());
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_uuid_v4_format() {
        let u = Uuid::new_v4(999);
        let s = u.to_string();
        assert_eq!(s.len(), 36);
        assert_eq!(&s[14..15], "4"); // version 4
    }
}
