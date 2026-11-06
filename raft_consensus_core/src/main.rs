//! Project 073: Raft Consensus Core State Machine
//! Demonstrates Raft leader election, role transitions, and term voting.

#[derive(Debug, PartialEq, Clone, Copy)]
pub enum Role {
    Follower,
    Candidate,
    Leader,
}

pub struct RaftNode {
    pub id: usize,
    pub term: u64,
    pub role: Role,
    pub voted_for: Option<usize>,
    pub votes_received: usize,
}

impl RaftNode {
    pub fn new(id: usize) -> Self {
        Self {
            id,
            term: 0,
            role: Role::Follower,
            voted_for: None,
            votes_received: 0,
        }
    }

    pub fn start_election(&mut self, total_nodes: usize) {
        self.term += 1;
        self.role = Role::Candidate;
        self.voted_for = Some(self.id);
        self.votes_received = 1;

        if self.votes_received > total_nodes / 2 {
            self.role = Role::Leader;
        }
    }

    pub fn receive_vote(&mut self, total_nodes: usize) {
        if self.role == Role::Candidate {
            self.votes_received += 1;
            if self.votes_received > total_nodes / 2 {
                self.role = Role::Leader;
            }
        }
    }

    pub fn step_down(&mut self, higher_term: u64) {
        if higher_term > self.term {
            self.term = higher_term;
            self.role = Role::Follower;
            self.voted_for = None;
            self.votes_received = 0;
        }
    }
}

fn main() {
    println!("=== 🦀 Project 073: Raft Consensus Core ===");
    let mut node = RaftNode::new(1);
    println!("Node initialized as: {:?}", node.role);

    node.start_election(3);
    println!("Election started: Role = {:?}, Term = {}", node.role, node.term);

    node.receive_vote(3);
    println!("Vote received (majority reached): Role = {:?}", node.role);
    assert_eq!(node.role, Role::Leader);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_raft_election() {
        let mut n = RaftNode::new(0);
        n.start_election(3);
        n.receive_vote(3);
        assert_eq!(n.role, Role::Leader);
        n.step_down(10);
        assert_eq!(n.role, Role::Follower);
    }
}
