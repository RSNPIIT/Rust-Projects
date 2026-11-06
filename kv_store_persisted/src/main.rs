//! Project 037: Persistent Key-Value Store
//! Demonstrates append-only log architecture and in-memory key index.

use std::collections::HashMap;

#[derive(Debug, Clone, PartialEq)]
pub enum Command {
    Set(String, String),
    Remove(String),
}

pub struct KeyValueStore {
    log: Vec<Command>,
    index: HashMap<String, String>,
}

impl KeyValueStore {
    pub fn new() -> Self {
        Self { log: Vec::new(), index: HashMap::new() }
    }

    pub fn set(&mut self, key: &str, val: &str) {
        let cmd = Command::Set(key.to_string(), val.to_string());
        self.log.push(cmd);
        self.index.insert(key.to_string(), val.to_string());
    }

    pub fn get(&self, key: &str) -> Option<&str> {
        self.index.get(key).map(|s| s.as_str())
    }

    pub fn delete(&mut self, key: &str) -> bool {
        if self.index.remove(key).is_some() {
            self.log.push(Command::Remove(key.to_string()));
            true
        } else {
            false
        }
    }

    pub fn log_len(&self) -> usize {
        self.log.len()
    }
}

fn main() {
    println!("=== 🦀 Project 037: Persistent Key-Value Store ===");
    let mut store = KeyValueStore::new();
    store.set("user:101", "Alice");
    store.set("user:102", "Bob");
    println!("Get user:101: {:?}", store.get("user:101"));

    store.set("user:101", "Alice Updated");
    println!("Get user:101: {:?}", store.get("user:101"));

    store.delete("user:102");
    println!("Get user:102: {:?}", store.get("user:102"));
    println!("Total log entries: {}", store.log_len());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_kv_store() {
        let mut store = KeyValueStore::new();
        store.set("k1", "v1");
        assert_eq!(store.get("k1"), Some("v1"));
        assert!(store.delete("k1"));
        assert_eq!(store.get("k1"), None);
    }
}
