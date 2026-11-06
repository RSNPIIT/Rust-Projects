//! Project 028: Precision Stopwatch & Lap Timer
//! Demonstrates monotonic time measurement and lap calculations.

use std::time::{Duration, Instant};

pub struct Stopwatch {
    start_time: Option<Instant>,
    accumulated: Duration,
    laps: Vec<Duration>,
}

impl Stopwatch {
    pub fn new() -> Self {
        Self { start_time: None, accumulated: Duration::ZERO, laps: Vec::new() }
    }

    pub fn start(&mut self) {
        if self.start_time.is_none() {
            self.start_time = Some(Instant::now());
        }
    }

    pub fn pause(&mut self) {
        if let Some(st) = self.start_time.take() {
            self.accumulated += st.elapsed();
        }
    }

    pub fn elapsed(&self) -> Duration {
        self.accumulated + self.start_time.map_or(Duration::ZERO, |st| st.elapsed())
    }

    pub fn lap(&mut self) -> Duration {
        let total = self.elapsed();
        let prev_total: Duration = self.laps.iter().sum();
        let lap_dur = total.saturating_sub(prev_total);
        self.laps.push(lap_dur);
        lap_dur
    }

    pub fn get_laps(&self) -> &[Duration] {
        &self.laps
    }
}

fn main() {
    println!("=== 🦀 Project 028: Precision Stopwatch & Lap Timer ===");
    let mut sw = Stopwatch::new();
    sw.start();

    // Simulate work
    let _sum: u64 = (0..500_000).sum();
    let lap1 = sw.lap();

    let _sum2: u64 = (0..1_000_000).sum();
    let lap2 = sw.lap();

    sw.pause();
    println!("Lap 1: {:?}, Lap 2: {:?}, Total: {:?}", lap1, lap2, sw.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_stopwatch() {
        let mut sw = Stopwatch::new();
        sw.start();
        sw.pause();
        assert!(sw.elapsed() >= Duration::ZERO);
    }
}
