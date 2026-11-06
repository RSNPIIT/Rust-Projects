//! Project 077: Custom Cooperative Async Executor
//! Demonstrates cooperative future polling and task scheduling loop.

use std::collections::VecDeque;

pub enum PollStatus<T> {
    Ready(T),
    Pending,
}

pub trait SimpleFuture {
    type Output;
    fn poll(&mut self) -> PollStatus<Self::Output>;
}

pub struct CountdownFuture {
    count: usize,
}

impl CountdownFuture {
    pub fn new(count: usize) -> Self {
        Self { count }
    }
}

impl SimpleFuture for CountdownFuture {
    type Output = String;
    fn poll(&mut self) -> PollStatus<Self::Output> {
        if self.count == 0 {
            PollStatus::Ready("Countdown completed!".to_string())
        } else {
            self.count -= 1;
            PollStatus::Pending
        }
    }
}

pub struct MiniExecutor {
    tasks: VecDeque<Box<dyn SimpleFuture<Output = String>>>,
}

impl MiniExecutor {
    pub fn new() -> Self {
        Self { tasks: VecDeque::new() }
    }

    pub fn spawn(&mut self, future: Box<dyn SimpleFuture<Output = String>>) {
        self.tasks.push_back(future);
    }

    pub fn run_all(&mut self) -> Vec<String> {
        let mut results = Vec::new();
        while let Some(mut task) = self.tasks.pop_front() {
            match task.poll() {
                PollStatus::Ready(val) => results.push(val),
                PollStatus::Pending => self.tasks.push_back(task),
            }
        }
        results
    }
}

fn main() {
    println!("=== 🦀 Project 077: Custom Cooperative Async Executor ===");
    let mut executor = MiniExecutor::new();
    executor.spawn(Box::new(CountdownFuture::new(2)));
    executor.spawn(Box::new(CountdownFuture::new(1)));

    let completed = executor.run_all();
    println!("Completed async tasks: {:?}", completed);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_executor() {
        let mut exec = MiniExecutor::new();
        exec.spawn(Box::new(CountdownFuture::new(3)));
        let res = exec.run_all();
        assert_eq!(res.len(), 1);
    }
}
