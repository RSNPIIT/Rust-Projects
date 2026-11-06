//! Project 074: Lock-Free SPSC Circular Queue
//! Demonstrates lock-free atomic concurrency and acquire/release memory semantics.

use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;

pub struct SpscQueue<T, const CAP: usize> {
    buffer: [Option<T>; CAP],
    head: AtomicUsize,
    tail: AtomicUsize,
}

impl<T: Copy + Default, const CAP: usize> SpscQueue<T, CAP> {
    pub fn new() -> Arc<Self> {
        Arc::new(Self {
            buffer: [None; CAP],
            head: AtomicUsize::new(0),
            tail: AtomicUsize::new(0),
        })
    }

    pub fn push(&mut self, val: T) -> Result<(), &'static str> {
        let head = self.head.load(Ordering::Relaxed);
        let tail = self.tail.load(Ordering::Acquire);

        if (head + 1) % CAP == tail {
            return Err("Queue full");
        }

        self.buffer[head] = Some(val);
        self.head.store((head + 1) % CAP, Ordering::Release);
        Ok(())
    }

    pub fn pop(&mut self) -> Option<T> {
        let tail = self.tail.load(Ordering::Relaxed);
        let head = self.head.load(Ordering::Acquire);

        if head == tail {
            return None;
        }

        let val = self.buffer[tail].take();
        self.tail.store((tail + 1) % CAP, Ordering::Release);
        val
    }
}

fn main() {
    println!("=== 🦀 Project 074: Lock-Free SPSC Queue ===");
    let mut q = SpscQueue::<i32, 4> {
        buffer: [None; 4],
        head: AtomicUsize::new(0),
        tail: AtomicUsize::new(0),
    };

    q.push(100).unwrap();
    q.push(200).unwrap();
    println!("Popped item: {:?}", q.pop());
    println!("Popped item: {:?}", q.pop());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_spsc() {
        let mut q = SpscQueue::<u32, 4> {
            buffer: [None; 4],
            head: AtomicUsize::new(0),
            tail: AtomicUsize::new(0),
        };
        assert!(q.push(42).is_ok());
        assert_eq!(q.pop(), Some(42));
        assert_eq!(q.pop(), None);
    }
}
