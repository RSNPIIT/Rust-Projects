//! Project 087: Single-Decree Paxos Consensus Simulator
//! Demonstrates classical Paxos phase 1 and phase 2 consensus.

#[derive(Default)]
pub struct Acceptor {
    promised_ballot: u64,
    accepted_ballot: Option<u64>,
    accepted_value: Option<String>,
}

impl Acceptor {
    pub fn prepare(&mut self, ballot: u64) -> Result<(Option<u64>, Option<String>), ()> {
        if ballot > self.promised_ballot {
            self.promised_ballot = ballot;
            Ok((self.accepted_ballot, self.accepted_value.clone()))
        } else {
            Err(())
        }
    }

    pub fn accept(&mut self, ballot: u64, value: &str) -> Result<(), ()> {
        if ballot >= self.promised_ballot {
            self.promised_ballot = ballot;
            self.accepted_ballot = Some(ballot);
            self.accepted_value = Some(value.to_string());
            Ok(())
        } else {
            Err(())
        }
    }
}

fn main() {
    println!("=== 🦀 Project 087: Single-Decree Paxos Simulator ===");
    let mut acceptors = [Acceptor::default(), Acceptor::default(), Acceptor::default()];
    let ballot = 1;
    let mut promises = 0;

    for a in &mut acceptors {
        if a.prepare(ballot).is_ok() { promises += 1; }
    }

    if promises >= 2 {
        println!("Phase 1 Quorum reached! Proposing value 'ConsensusValue'...");
        for a in &mut acceptors {
            let _ = a.accept(ballot, "ConsensusValue");
        }
        println!("Consensus accepted across majority.");
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_paxos_acceptor() {
        let mut a = Acceptor::default();
        assert!(a.prepare(1).is_ok());
        assert!(a.prepare(1).is_err()); // equal or lower rejected
        assert!(a.accept(1, "val").is_ok());
    }
}
