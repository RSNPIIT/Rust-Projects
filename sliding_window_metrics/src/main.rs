//! Project 097: Sliding Window Percentile Metrics
//! Demonstrates rolling time window metrics and quantile calculations.

pub struct MetricWindow {
    samples: Vec<f64>,
    capacity: usize,
}

impl MetricWindow {
    pub fn new(capacity: usize) -> Self {
        Self { samples: Vec::new(), capacity }
    }

    pub fn record(&mut self, val: f64) {
        if self.samples.len() >= self.capacity {
            self.samples.remove(0);
        }
        self.samples.push(val);
    }

    pub fn percentile(&self, p: f64) -> Option<f64> {
        if self.samples.is_empty() { return None; }
        let mut sorted = self.samples.clone();
        sorted.sort_by(|a, b| a.partial_cmp(b).unwrap());
        let idx = ((p / 100.0) * (sorted.len() - 1) as f64).round() as usize;
        Some(sorted[idx])
    }
}

fn main() {
    println!("=== 🦀 Project 097: Sliding Window Metrics ===");
    let mut mw = MetricWindow::new(100);
    for lat in [12.0, 15.0, 14.5, 18.0, 95.0, 13.0, 16.0] {
        mw.record(lat);
    }

    println!("p50 latency: {:.1} ms", mw.percentile(50.0).unwrap());
    println!("p99 latency: {:.1} ms", mw.percentile(99.0).unwrap());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_percentile() {
        let mut mw = MetricWindow::new(10);
        for i in 1..=10 { mw.record(i as f64); }
        assert_eq!(mw.percentile(50.0), Some(5.0));
    }
}
