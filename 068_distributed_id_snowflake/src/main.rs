//! Project 068: Twitter Snowflake ID Generator
//! Demonstrates 64-bit k-ordered unique distributed ID generation.

pub struct Snowflake {
    epoch: u64,
    datacenter_id: u64,
    worker_id: u64,
    sequence: u64,
    last_timestamp: u64,
}

impl Snowflake {
    pub fn new(datacenter_id: u64, worker_id: u64) -> Self {
        Self {
            epoch: 1700000000000, // Custom epoch
            datacenter_id: datacenter_id & 0x1F, // 5 bits
            worker_id: worker_id & 0x1F,         // 5 bits
            sequence: 0,
            last_timestamp: 0,
        }
    }

    pub fn generate(&mut self, current_millis: u64) -> u64 {
        let mut timestamp = current_millis;
        if timestamp == self.last_timestamp {
            self.sequence = (self.sequence + 1) & 0xFFF; // 12 bits
            if self.sequence == 0 {
                timestamp += 1;
            }
        } else {
            self.sequence = 0;
        }
        self.last_timestamp = timestamp;

        let time_part = (timestamp - self.epoch) << 22;
        let dc_part = self.datacenter_id << 17;
        let worker_part = self.worker_id << 12;

        time_part | dc_part | worker_part | self.sequence
    }
}

fn main() {
    println!("=== 🦀 Project 068: Twitter Snowflake ID Generator ===");
    let mut sf = Snowflake::new(1, 2);
    let sim_time = 1710000000000;

    for _ in 0..5 {
        let id = sf.generate(sim_time);
        println!("Generated 64-bit Snowflake ID: {} (0x{:016X})", id, id);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_snowflake_uniqueness() {
        let mut sf = Snowflake::new(1, 1);
        let id1 = sf.generate(1710000000000);
        let id2 = sf.generate(1710000000000);
        assert_ne!(id1, id2);
    }
}
