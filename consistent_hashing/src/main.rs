//! Project 052: Consistent Hashing Ring
//! Demonstrates consistent hashing with virtual nodes for distributed data routing.

use std::collections::BTreeMap;

pub struct ConsistentHashRing {
    replicas: usize,
    ring: BTreeMap<u64, String>,
}

fn hash_str(s: &str) -> u64 {
    let mut h: u64 = 14695981039346656037;
    for b in s.bytes() {
        h = (h ^ (b as u64)).wrapping_mul(1099511628211);
    }
    h
}

impl ConsistentHashRing {
    pub fn new(replicas: usize) -> Self {
        Self { replicas, ring: BTreeMap::new() }
    }

    pub fn add_node(&mut self, node: &str) {
        for i in 0..self.replicas {
            let vnode_key = format!("{}:{}", node, i);
            let h = hash_str(&vnode_key);
            self.ring.insert(h, node.to_string());
        }
    }

    pub fn get_node(&self, key: &str) -> Option<&str> {
        if self.ring.is_empty() { return None; }
        let h = hash_str(key);
        // Find first node with hash >= h, or wrap to ring beginning
        let node = self.ring.range(h..).next().or_else(|| self.ring.iter().next());
        node.map(|(_, name)| name.as_str())
    }
}

fn main() {
    println!("=== 🦀 Project 052: Consistent Hashing Ring ===");
    let mut ring = ConsistentHashRing::new(3);
    ring.add_node("cache-srv-01");
    ring.add_node("cache-srv-02");
    ring.add_node("cache-srv-03");

    let keys = ["user_1001", "session_abc", "product_55", "order_99"];
    for k in keys {
        println!("Key '{}' routed to => {}", k, ring.get_node(k).unwrap());
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_consistent_hash() {
        let mut ring = ConsistentHashRing::new(3);
        ring.add_node("nodeA");
        ring.add_node("nodeB");
        assert!(ring.get_node("key1").is_some());
    }
}
