//! Project 014: Generic Stack & Queue
//! Demonstrates generic data structures, LIFO and FIFO access patterns.

use std::collections::VecDeque;

#[derive(Debug, Default)]
pub struct Stack<T> {
    items: Vec<T>,
}

impl<T> Stack<T> {
    pub fn new() -> Self { Self { items: Vec::new() } }
    pub fn push(&mut self, item: T) { self.items.push(item); }
    pub fn pop(&mut self) -> Option<T> { self.items.pop() }
    pub fn peek(&self) -> Option<&T> { self.items.last() }
    pub fn is_empty(&self) -> bool { self.items.is_empty() }
    pub fn len(&self) -> usize { self.items.len() }
}

#[derive(Debug, Default)]
pub struct Queue<T> {
    items: VecDeque<T>,
}

impl<T> Queue<T> {
    pub fn new() -> Self { Self { items: VecDeque::new() } }
    pub fn enqueue(&mut self, item: T) { self.items.push_back(item); }
    pub fn dequeue(&mut self) -> Option<T> { self.items.pop_front() }
    pub fn peek(&self) -> Option<&T> { self.items.front() }
    pub fn is_empty(&self) -> bool { self.items.is_empty() }
    pub fn len(&self) -> usize { self.items.len() }
}

fn main() {
    println!("=== 🦀 Project 014: Generic Stack & Queue ===");
    let mut stack = Stack::new();
    stack.push(10);
    stack.push(20);
    stack.push(30);
    println!("Stack Pop: {:?}", stack.pop());

    let mut queue = Queue::new();
    queue.enqueue("Task 1");
    queue.enqueue("Task 2");
    println!("Queue Dequeue: {:?}", queue.dequeue());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_stack_lifo() {
        let mut s = Stack::new();
        s.push(1); s.push(2);
        assert_eq!(s.pop(), Some(2));
        assert_eq!(s.pop(), Some(1));
    }

    #[test]
    fn test_queue_fifo() {
        let mut q = Queue::new();
        q.enqueue(1); q.enqueue(2);
        assert_eq!(q.dequeue(), Some(1));
        assert_eq!(q.dequeue(), Some(2));
    }
}
