//! Project 056: Circuit Breaker State Machine
//! Demonstrates fault tolerance and state transitions in distributed systems.

use std::time::{Duration, Instant};

#[derive(Debug, PartialEq, Clone, Copy)]
pub enum State {
    Closed,
    Open,
    HalfOpen,
}

pub struct CircuitBreaker {
    state: State,
    failure_count: u32,
    failure_threshold: u32,
    reset_timeout: Duration,
    last_state_change: Instant,
}

impl CircuitBreaker {
    pub fn new(failure_threshold: u32, reset_timeout: Duration) -> Self {
        Self {
            state: State::Closed,
            failure_count: 0,
            failure_threshold,
            reset_timeout,
            last_state_change: Instant::now(),
        }
    }

    pub fn state(&mut self) -> State {
        if self.state == State::Open && self.last_state_change.elapsed() >= self.reset_timeout {
            self.state = State::HalfOpen;
            self.last_state_change = Instant::now();
        }
        self.state
    }

    pub fn record_success(&mut self) {
        self.failure_count = 0;
        self.state = State::Closed;
    }

    pub fn record_failure(&mut self) {
        self.failure_count += 1;
        if self.failure_count >= self.failure_threshold {
            self.state = State::Open;
            self.last_state_change = Instant::now();
        }
    }

    pub fn can_execute(&mut self) -> bool {
        self.state() != State::Open
    }
}

fn main() {
    println!("=== 🦀 Project 056: Circuit Breaker State Machine ===");
    let mut cb = CircuitBreaker::new(3, Duration::from_millis(50));
    println!("Initial state: {:?}", cb.state());

    cb.record_failure();
    cb.record_failure();
    println!("After 2 failures: {:?}", cb.state());

    cb.record_failure(); // trips to Open
    println!("After 3 failures: {:?}", cb.state());
    println!("Can execute? {}", cb.can_execute());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_circuit_trips() {
        let mut cb = CircuitBreaker::new(2, Duration::from_secs(10));
        assert!(cb.can_execute());
        cb.record_failure();
        cb.record_failure();
        assert_eq!(cb.state(), State::Open);
        assert!(!cb.can_execute());
    }
}
