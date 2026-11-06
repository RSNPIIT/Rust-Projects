//! Project 098: Chandy-Lamport Distributed Snapshot
//! Demonstrates marker propagation and consistent global cuts.

#[derive(Debug, Clone)]
pub struct ProcessState {
    pub balance: i64,
    pub recorded_snapshot: Option<i64>,
}

impl ProcessState {
    pub fn new(balance: i64) -> Self {
        Self { balance, recorded_snapshot: None }
    }

    pub fn record_marker(&mut self) {
        if self.recorded_snapshot.is_none() {
            self.recorded_snapshot = Some(self.balance);
        }
    }
}

fn main() {
    println!("=== 🦀 Project 098: Chandy-Lamport Snapshot ===");
    let mut p1 = ProcessState::new(100);
    let mut p2 = ProcessState::new(200);

    // Snapshot initiated at P1
    p1.record_marker();
    // Marker sent across channel to P2
    p2.record_marker();

    println!("Global consistent cut:");
    println!("Process 1 recorded state: {:?}", p1.recorded_snapshot);
    println!("Process 2 recorded state: {:?}", p2.recorded_snapshot);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_snapshot() {
        let mut p = ProcessState::new(50);
        p.record_marker();
        assert_eq!(p.recorded_snapshot, Some(50));
    }
}
