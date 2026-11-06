//! Project 092: Distributed Two-Phase Commit (2PC)
//! Demonstrates distributed transaction coordination and voting.

pub struct Participant {
    pub id: usize,
    pub can_commit: bool,
}

pub struct Coordinator;

impl Coordinator {
    pub fn execute_transaction(participants: &[Participant]) -> bool {
        // Phase 1: Prepare
        let all_agreed = participants.iter().all(|p| p.can_commit);

        // Phase 2: Commit or Abort
        all_agreed
    }
}

fn main() {
    println!("=== 🦀 Project 092: Distributed Two-Phase Commit ===");
    let cohorts = vec![
        Participant { id: 1, can_commit: true },
        Participant { id: 2, can_commit: true },
        Participant { id: 3, can_commit: false }, // Node votes NO
    ];

    let committed = Coordinator::execute_transaction(&cohorts);
    println!("Transaction outcome: {}", if committed { "✅ COMMITTED" } else { "❌ ABORTED & ROLLED BACK" });
    assert!(!committed);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_2pc() {
        let p = vec![Participant { id: 1, can_commit: true }, Participant { id: 2, can_commit: true }];
        assert!(Coordinator::execute_transaction(&p));
    }
}
