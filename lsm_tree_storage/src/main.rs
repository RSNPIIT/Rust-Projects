//! Project 079: Log-Structured Merge Tree (LSM)
//! Demonstrates in-memory MemTable, SSTables, and layered key search.

use std::collections::BTreeMap;

pub struct LsmTree {
    memtable: BTreeMap<String, String>,
    memtable_threshold: usize,
    sstables: Vec<BTreeMap<String, String>>,
}

impl LsmTree {
    pub fn new(threshold: usize) -> Self {
        Self {
            memtable: BTreeMap::new(),
            memtable_threshold: threshold,
            sstables: Vec::new(),
        }
    }

    pub fn put(&mut self, key: &str, val: &str) {
        self.memtable.insert(key.to_string(), val.to_string());
        if self.memtable.len() >= self.memtable_threshold {
            let flushed = std::mem::take(&mut self.memtable);
            self.sstables.push(flushed);
        }
    }

    pub fn get(&self, key: &str) -> Option<&str> {
        if let Some(val) = self.memtable.get(key) {
            return Some(val);
        }
        for sstable in self.sstables.iter().rev() {
            if let Some(val) = sstable.get(key) {
                return Some(val);
            }
        }
        None
    }
}

fn main() {
    println!("=== 🦀 Project 079: LSM-Tree Storage Engine ===");
    let mut lsm = LsmTree::new(2);
    lsm.put("user_1", "Alice");
    lsm.put("user_2", "Bob"); // flushes to SSTable #1
    lsm.put("user_3", "Charlie");

    println!("Get user_1: {:?}", lsm.get("user_1"));
    println!("Get user_3: {:?}", lsm.get("user_3"));
    println!("Flushed SSTables: {}", lsm.sstables.len());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_lsm() {
        let mut lsm = LsmTree::new(2);
        lsm.put("a", "1");
        lsm.put("b", "2");
        lsm.put("a", "3");
        assert_eq!(lsm.get("a"), Some("3"));
    }
}
