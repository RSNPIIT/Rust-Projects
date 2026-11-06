//! Project 041: Token Bucket Rate Limiter
//! Demonstrates token replenishment rate limiting for network APIs.

use std::time::Instant;

pub struct TokenBucket {
    capacity: f64,
    tokens: f64,
    fill_rate_per_sec: f64,
    last_update: Instant,
}

impl TokenBucket {
    pub fn new(capacity: f64, fill_rate_per_sec: f64) -> Self {
        Self {
            capacity,
            tokens: capacity,
            fill_rate_per_sec,
            last_update: Instant::now(),
        }
    }

    fn replenish(&mut self) {
        let now = Instant::now();
        let elapsed = now.duration_since(self.last_update).as_secs_f64();
        self.tokens = (self.tokens + elapsed * self.fill_rate_per_sec).min(self.capacity);
        self.last_update = now;
    }

    pub fn try_consume(&mut self, amount: f64) -> bool {
        self.replenish();
        if self.tokens >= amount {
            self.tokens -= amount;
            true
        } else {
            false
        }
    }

    pub fn available_tokens(&mut self) -> f64 {
        self.replenish();
        self.tokens
    }
}

fn main() {
    println!("=== 🦀 Project 041: Token Bucket Rate Limiter ===");
    let mut limiter = TokenBucket::new(5.0, 2.0); // 5 max, 2 tokens per sec

    for i in 1..=7 {
        let allowed = limiter.try_consume(1.0);
        println!("Request {}: {}", i, if allowed { "✅ ALLOWED" } else { "❌ THROTTLED" });
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_limiter_burst() {
        let mut limiter = TokenBucket::new(3.0, 1.0);
        assert!(limiter.try_consume(1.0));
        assert!(limiter.try_consume(1.0));
        assert!(limiter.try_consume(1.0));
        assert!(!limiter.try_consume(1.0));
    }
}
