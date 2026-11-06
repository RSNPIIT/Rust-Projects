//! Project 047: Circular FIFO Ring Buffer
//! Demonstrates wrapping array indices and bounded buffer streaming.

pub struct RingBuffer<T> {
    buffer: Vec<Option<T>>,
    head: usize,
    tail: usize,
    count: usize,
    capacity: usize,
}

impl<T: Clone> RingBuffer<T> {
    pub fn new(capacity: usize) -> Self {
        assert!(capacity > 0);
        Self {
            buffer: vec![None; capacity],
            head: 0,
            tail: 0,
            count: 0,
            capacity,
        }
    }

    pub fn push(&mut self, item: T) -> Result<(), &'static str> {
        if self.count == self.capacity {
            return Err("Buffer is full");
        }
        self.buffer[self.tail] = Some(item);
        self.tail = (self.tail + 1) % self.capacity;
        self.count += 1;
        Ok(())
    }

    pub fn pop(&mut self) -> Option<T> {
        if self.count == 0 {
            return None;
        }
        let item = self.buffer[self.head].take();
        self.head = (self.head + 1) % self.capacity;
        self.count -= 1;
        item
    }

    pub fn len(&self) -> usize { self.count }
    pub fn is_empty(&self) -> bool { self.count == 0 }
}

fn main() {
    println!("=== 🦀 Project 047: Circular FIFO Ring Buffer ===");
    let mut ring = RingBuffer::new(3);
    ring.push(10).unwrap();
    ring.push(20).unwrap();
    ring.push(30).unwrap();

    println!("Popped: {:?}", ring.pop());
    ring.push(40).unwrap();

    while let Some(val) = ring.pop() {
        println!("Popped item: {}", val);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ring_wrapping() {
        let mut r = RingBuffer::new(2);
        r.push(1).unwrap();
        r.push(2).unwrap();
        assert!(r.push(3).is_err());
        assert_eq!(r.pop(), Some(1));
        assert!(r.push(3).is_ok());
    }
}
