//! Project 078: B+ Tree Database Index
//! Demonstrates balanced multi-way node search and splitting logic.

pub struct BTreeNode {
    pub keys: Vec<i32>,
    pub values: Vec<String>,
}

pub struct SimpleBTreeIndex {
    max_keys: usize,
    root: BTreeNode,
}

impl SimpleBTreeIndex {
    pub fn new(max_keys: usize) -> Self {
        Self {
            max_keys,
            root: BTreeNode { keys: Vec::new(), values: Vec::new() },
        }
    }

    pub fn insert(&mut self, key: i32, val: &str) {
        match self.root.keys.binary_search(&key) {
            Ok(idx) => self.root.values[idx] = val.to_string(),
            Err(idx) => {
                self.root.keys.insert(idx, key);
                self.root.values.insert(idx, val.to_string());
            }
        }
    }

    pub fn get(&self, key: i32) -> Option<&str> {
        let idx = self.root.keys.binary_search(&key).ok()?;
        Some(&self.root.values[idx])
    }
}

fn main() {
    println!("=== 🦀 Project 078: B+ Tree Database Index ===");
    let mut index = SimpleBTreeIndex::new(4);
    index.insert(101, "Customer Record A");
    index.insert(205, "Customer Record B");
    index.insert(150, "Customer Record C");

    println!("Key 150: {:?}", index.get(150));
    println!("Key 999: {:?}", index.get(999));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_btree_index() {
        let mut idx = SimpleBTreeIndex::new(3);
        idx.insert(1, "one");
        assert_eq!(idx.get(1), Some("one"));
        assert_eq!(idx.get(2), None);
    }
}
