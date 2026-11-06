//! Project 083: Atomic Lock-Free Treiber Stack
//! Demonstrates CAS atomic loops and lock-free concurrency.

use std::sync::atomic::{AtomicPtr, Ordering};

struct Node<T> {
    data: T,
    next: *mut Node<T>,
}

pub struct TreiberStack<T> {
    head: AtomicPtr<Node<T>>,
}

impl<T> TreiberStack<T> {
    pub fn new() -> Self {
        Self { head: AtomicPtr::new(std::ptr::null_mut()) }
    }

    pub fn push(&self, data: T) {
        let new_node = Box::into_raw(Box::new(Node {
            data,
            next: std::ptr::null_mut(),
        }));

        let mut current = self.head.load(Ordering::Relaxed);
        loop {
            unsafe { (*new_node).next = current; }
            match self.head.compare_exchange_weak(current, new_node, Ordering::Release, Ordering::Relaxed) {
                Ok(_) => break,
                Err(actual) => current = actual,
            }
        }
    }

    pub fn pop(&self) -> Option<T> {
        let mut current = self.head.load(Ordering::Acquire);
        loop {
            if current.is_null() {
                return None;
            }
            let next = unsafe { (*current).next };
            match self.head.compare_exchange_weak(current, next, Ordering::Release, Ordering::Relaxed) {
                Ok(_) => {
                    let boxed = unsafe { Box::from_raw(current) };
                    return Some(boxed.data);
                }
                Err(actual) => current = actual,
            }
        }
    }
}

fn main() {
    println!("=== 🦀 Project 083: Lock-Free Treiber Stack ===");
    let stack = TreiberStack::new();
    stack.push(10);
    stack.push(20);
    stack.push(30);

    println!("Popped: {:?}", stack.pop());
    println!("Popped: {:?}", stack.pop());
    println!("Popped: {:?}", stack.pop());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_treiber() {
        let s = TreiberStack::new();
        s.push("a");
        s.push("b");
        assert_eq!(s.pop(), Some("b"));
        assert_eq!(s.pop(), Some("a"));
        assert_eq!(s.pop(), None);
    }
}
