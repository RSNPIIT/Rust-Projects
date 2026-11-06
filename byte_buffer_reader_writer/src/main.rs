//! Project 069: Endian & Varint Binary Codec
//! Demonstrates LEB128 varint encoding and multi-endian primitive serialization.

pub struct ByteBuffer {
    pub data: Vec<u8>,
    pub read_pos: usize,
}

impl ByteBuffer {
    pub fn new() -> Self {
        Self { data: Vec::new(), read_pos: 0 }
    }

    pub fn write_u32_be(&mut self, val: u32) {
        self.data.extend_from_slice(&val.to_be_bytes());
    }

    pub fn read_u32_be(&mut self) -> Option<u32> {
        if self.read_pos + 4 <= self.data.len() {
            let bytes = [
                self.data[self.read_pos], self.data[self.read_pos + 1],
                self.data[self.read_pos + 2], self.data[self.read_pos + 3]
            ];
            self.read_pos += 4;
            Some(u32::from_be_bytes(bytes))
        } else {
            None
        }
    }

    pub fn write_varint(&mut self, mut val: u64) {
        while val >= 0x80 {
            self.data.push(((val & 0x7F) | 0x80) as u8);
            val >>= 7;
        }
        self.data.push((val & 0x7F) as u8);
    }

    pub fn read_varint(&mut self) -> Option<u64> {
        let mut res = 0u64;
        let mut shift = 0;
        while self.read_pos < self.data.len() {
            let b = self.data[self.read_pos];
            self.read_pos += 1;
            res |= ((b & 0x7F) as u64) << shift;
            if (b & 0x80) == 0 {
                return Some(res);
            }
            shift += 7;
        }
        None
    }
}

fn main() {
    println!("=== 🦀 Project 069: Endian & Varint Binary Codec ===");
    let mut buf = ByteBuffer::new();
    buf.write_u32_be(0xCAFEBABE);
    buf.write_varint(300);

    println!("Serialized raw bytes: {:?}", buf.data);
    let u = buf.read_u32_be().unwrap();
    let v = buf.read_varint().unwrap();
    println!("Decoded u32: 0x{:08X}, varint: {}", u, v);
    assert_eq!(u, 0xCAFEBABE);
    assert_eq!(v, 300);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_varint() {
        let mut buf = ByteBuffer::new();
        buf.write_varint(150);
        assert_eq!(buf.read_varint(), Some(150));
    }
}
