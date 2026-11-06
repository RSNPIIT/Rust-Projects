//! Project 046: Bump Arena Memory Allocator
//! Demonstrates fast contiguous arena allocations and batch resets.

pub struct Arena {
    buffer: Vec<u8>,
    offset: usize,
}

impl Arena {
    pub fn with_capacity(capacity: usize) -> Self {
        Self {
            buffer: vec![0; capacity],
            offset: 0,
        }
    }

    pub fn alloc(&mut self, size: usize) -> Option<&mut [u8]> {
        // 8-byte alignment
        let aligned = (self.offset + 7) & !7;
        if aligned + size <= self.buffer.len() {
            let start = aligned;
            self.offset = aligned + size;
            Some(&mut self.buffer[start..start + size])
        } else {
            None
        }
    }

    pub fn reset(&mut self) {
        self.offset = 0;
    }

    pub fn used_bytes(&self) -> usize {
        self.offset
    }
}

fn main() {
    println!("=== 🦀 Project 046: Bump Arena Memory Allocator ===");
    let mut arena = Arena::with_capacity(1024);

    let chunk1 = arena.alloc(64).unwrap();
    chunk1[0] = 0xAA;
    println!("Allocated 64 bytes. Total used: {}", arena.used_bytes());

    let chunk2 = arena.alloc(128).unwrap();
    chunk2[0] = 0xBB;
    println!("Allocated 128 bytes. Total used: {}", arena.used_bytes());

    arena.reset();
    println!("Reset arena. Total used: {}", arena.used_bytes());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_arena_alloc() {
        let mut arena = Arena::with_capacity(100);
        let b1 = arena.alloc(20);
        assert!(b1.is_some());
        let b2 = arena.alloc(90);
        assert!(b2.is_none()); // exceeds capacity
    }
}
