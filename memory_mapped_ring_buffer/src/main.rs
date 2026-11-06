//! Project 085: Shared Memory IPC Ring Buffer
//! Demonstrates shared memory layout and atomic IPC synchronization.

use std::sync::atomic::{AtomicUsize, Ordering};

pub struct SharedIpcBuffer {
    data: [u8; 64],
    read_cursor: AtomicUsize,
    write_cursor: AtomicUsize,
}

impl SharedIpcBuffer {
    pub const fn new() -> Self {
        Self {
            data: [0u8; 64],
            read_cursor: AtomicUsize::new(0),
            write_cursor: AtomicUsize::new(0),
        }
    }

    pub fn write_byte(&mut self, b: u8) -> Result<(), &'static str> {
        let w = self.write_cursor.load(Ordering::Relaxed);
        let r = self.read_cursor.load(Ordering::Acquire);
        if (w + 1) % 64 == r {
            return Err("Buffer full");
        }
        self.data[w] = b;
        self.write_cursor.store((w + 1) % 64, Ordering::Release);
        Ok(())
    }

    pub fn read_byte(&self) -> Option<u8> {
        let r = self.read_cursor.load(Ordering::Relaxed);
        let w = self.write_cursor.load(Ordering::Acquire);
        if r == w {
            return None;
        }
        let val = self.data[r];
        self.read_cursor.store((r + 1) % 64, Ordering::Release);
        Some(val)
    }
}

fn main() {
    println!("=== 🦀 Project 085: Shared Memory IPC Ring Buffer ===");
    let mut ipc = SharedIpcBuffer::new();
    ipc.write_byte(0x52).unwrap(); // 'R'
    ipc.write_byte(0x53).unwrap(); // 'S'

    println!("Read IPC byte: 0x{:02X}", ipc.read_byte().unwrap());
    println!("Read IPC byte: 0x{:02X}", ipc.read_byte().unwrap());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ipc_buffer() {
        let mut ipc = SharedIpcBuffer::new();
        assert!(ipc.write_byte(42).is_ok());
        assert_eq!(ipc.read_byte(), Some(42));
    }
}
