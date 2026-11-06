//! Project 007: Fibonacci Generator
//! Demonstrates implementing the Iterator trait, recursion, and memoization.

use std::collections::HashMap;

pub struct Fibonacci {
    curr: u128,
    next: u128,
}

impl Fibonacci {
    pub fn new() -> Self {
        Self { curr: 0, next: 1 }
    }
}

impl Iterator for Fibonacci {
    type Item = u128;

    fn next(&mut self) -> Option<Self::Item> {
        let current = self.curr;
        let new_next = self.curr.checked_add(self.next)?;
        self.curr = self.next;
        self.next = new_next;
        Some(current)
    }
}

pub fn fib_memo(n: u32, memo: &mut HashMap<u32, u128>) -> u128 {
    if n <= 1 {
        return n as u128;
    }
    if let Some(&val) = memo.get(&n) {
        return val;
    }
    let val = fib_memo(n - 1, memo) + fib_memo(n - 2, memo);
    memo.insert(n, val);
    val
}

fn main() {
    println!("=== 🦀 Project 007: Fibonacci Generator ===");
    println!("First 15 Fibonacci numbers using custom Iterator:");
    let fib = Fibonacci::new();
    let seq: Vec<u128> = fib.take(15).collect();
    println!("{:?}", seq);

    let mut memo = HashMap::new();
    let n = 30;
    println!("Fibonacci({}) using memoization: {}", n, fib_memo(n, &mut memo));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_fibonacci_iterator() {
        let fib = Fibonacci::new();
        let expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34];
        let actual: Vec<u128> = fib.take(10).collect();
        assert_eq!(actual, expected);
    }
}
