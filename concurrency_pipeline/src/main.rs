//! Project 054: Concurrent Stream Pipeline
//! Demonstrates multi-stage stream processing using synchronized channels.

use std::sync::mpsc;
use std::thread;

pub fn run_pipeline(inputs: Vec<i32>) -> Vec<i32> {
    let (tx1, rx1) = mpsc::channel();
    let (tx2, rx2) = mpsc::channel();

    // Stage 1: Filter even numbers
    thread::spawn(move || {
        for n in inputs {
            if n % 2 == 0 {
                let _ = tx1.send(n);
            }
        }
    });

    // Stage 2: Square values
    thread::spawn(move || {
        while let Ok(n) = rx1.recv() {
            let _ = tx2.send(n * n);
        }
    });

    // Stage 3: Collect
    let mut results = Vec::new();
    while let Ok(val) = rx2.recv() {
        results.push(val);
    }
    results
}

fn main() {
    println!("=== 🦀 Project 054: Concurrent Stream Pipeline ===");
    let data: Vec<i32> = (1..=10).collect();
    println!("Input numbers: {:?}", data);
    let out = run_pipeline(data);
    println!("Even squares:  {:?}", out);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_pipeline() {
        let res = run_pipeline(vec![1, 2, 3, 4]);
        assert_eq!(res, vec![4, 16]);
    }
}
