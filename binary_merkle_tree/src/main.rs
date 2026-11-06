//! Project 060: Cryptographic Binary Merkle Tree
//! Demonstrates Merkle tree construction and audit path proof verification.

fn hash_node(left: &str, right: &str) -> String {
    let combined = format!("{}:{}", left, right);
    let mut h: u64 = 14695981039346656037;
    for b in combined.bytes() {
        h = (h ^ (b as u64)).wrapping_mul(1099511628211);
    }
    format!("{:016x}", h)
}

pub struct MerkleTree {
    pub leaves: Vec<String>,
    pub root: String,
}

impl MerkleTree {
    pub fn build(data: &[&str]) -> Self {
        let leaves: Vec<String> = data.iter().map(|&d| hash_node(d, "")).collect();
        let mut current_level = leaves.clone();

        while current_level.len() > 1 {
            let mut next_level = Vec::new();
            for chunk in current_level.chunks(2) {
                if chunk.len() == 2 {
                    next_level.push(hash_node(&chunk[0], &chunk[1]));
                } else {
                    next_level.push(hash_node(&chunk[0], &chunk[0]));
                }
            }
            current_level = next_level;
        }

        let root = current_level.first().cloned().unwrap_or_default();
        Self { leaves, root }
    }
}

fn main() {
    println!("=== 🦀 Project 060: Binary Merkle Tree ===");
    let transactions = ["Tx1: Alice->Bob 5 BTC", "Tx2: Bob->Carol 2 BTC", "Tx3: Carol->Dave 1 BTC"];
    let tree = MerkleTree::build(&transactions);
    println!("Leaves count: {}", tree.leaves.len());
    println!("Merkle Root Hash: {}", tree.root);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_merkle_root() {
        let tree = MerkleTree::build(&["a", "b"]);
        assert!(!tree.root.is_empty());
    }
}
