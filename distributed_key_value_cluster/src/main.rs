//! Project 100: Distributed Gossip-Protocol Cluster
//! Demonstrates decentralized anti-entropy gossip replication and node heartbeats.

use std::collections::HashMap;

#[derive(Clone, Debug)]
pub struct ClusterNode {
    pub node_id: String,
    pub heartbeat: u64,
    pub store: HashMap<String, String>,
}

impl ClusterNode {
    pub fn new(node_id: &str) -> Self {
        Self {
            node_id: node_id.to_string(),
            heartbeat: 0,
            store: HashMap::new(),
        }
    }

    pub fn tick_heartbeat(&mut self) {
        self.heartbeat += 1;
    }

    pub fn set(&mut self, key: &str, val: &str) {
        self.store.insert(key.to_string(), val.to_string());
    }

    pub fn merge_gossip(&mut self, other: &ClusterNode) {
        for (k, v) in &other.store {
            self.store.entry(k.clone()).or_insert_with(|| v.clone());
        }
    }
}

fn main() {
    println!("=== 🦀 Project 100: Distributed Gossip Cluster ===");
    let mut node_a = ClusterNode::new("node-alpha");
    let mut node_b = ClusterNode::new("node-beta");

    node_a.set("cluster_name", "RustHyperCluster");
    node_b.set("version", "2.0.0");

    println!("Pre-Gossip Node A: {:?}", node_a.store);
    println!("Pre-Gossip Node B: {:?}", node_b.store);

    // Gossip anti-entropy exchange
    node_a.merge_gossip(&node_b);
    node_b.merge_gossip(&node_a);

    println!("\nPost-Gossip Node A: {:?}", node_a.store);
    println!("Post-Gossip Node B: {:?}", node_b.store);
    assert_eq!(node_a.store, node_b.store);
    println!("\n🎉 Congratulations on exploring all 100 Rust projects!");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_gossip_sync() {
        let mut a = ClusterNode::new("A");
        let mut b = ClusterNode::new("B");
        a.set("k1", "v1");
        b.merge_gossip(&a);
        assert_eq!(b.store.get("k1"), Some(&"v1".to_string()));
    }
}
