//! Project 038: LRU Cache
//! Demonstrates O(1) cache access and eviction using index-based doubly linked nodes.

use std::collections::HashMap;

struct Node<K, V> {
    key: K,
    val: V,
    prev: Option<usize>,
    next: Option<usize>,
}

pub struct LruCache<K: std::hash::Hash + Eq + Clone, V: Clone> {
    capacity: usize,
    map: HashMap<K, usize>,
    nodes: Vec<Node<K, V>>,
    head: Option<usize>,
    tail: Option<usize>,
}

impl<K: std::hash::Hash + Eq + Clone, V: Clone> LruCache<K, V> {
    pub fn new(capacity: usize) -> Self {
        assert!(capacity > 0);
        Self {
            capacity,
            map: HashMap::new(),
            nodes: Vec::new(),
            head: None,
            tail: None,
        }
    }

    pub fn put(&mut self, key: K, val: V) {
        if let Some(&idx) = self.map.get(&key) {
            self.nodes[idx].val = val;
            self.move_to_head(idx);
            return;
        }

        let new_idx = self.nodes.len();
        self.nodes.push(Node {
            key: key.clone(),
            val,
            prev: None,
            next: self.head,
        });

        if let Some(h) = self.head {
            self.nodes[h].prev = Some(new_idx);
        }
        self.head = Some(new_idx);
        if self.tail.is_none() {
            self.tail = Some(new_idx);
        }
        self.map.insert(key, new_idx);

        if self.map.len() > self.capacity {
            self.evict_tail();
        }
    }

    pub fn get(&mut self, key: &K) -> Option<V> {
        let &idx = self.map.get(key)?;
        self.move_to_head(idx);
        Some(self.nodes[idx].val.clone())
    }

    fn move_to_head(&mut self, idx: usize) {
        if Some(idx) == self.head { return; }
        // Unlink
        let p = self.nodes[idx].prev;
        let n = self.nodes[idx].next;
        if let Some(p_idx) = p { self.nodes[p_idx].next = n; }
        if let Some(n_idx) = n { self.nodes[n_idx].prev = p; }
        if Some(idx) == self.tail { self.tail = p; }

        // Attach to head
        self.nodes[idx].prev = None;
        self.nodes[idx].next = self.head;
        if let Some(h) = self.head { self.nodes[h].prev = Some(idx); }
        self.head = Some(idx);
    }

    fn evict_tail(&mut self) {
        if let Some(t) = self.tail {
            let key = self.nodes[t].key.clone();
            self.map.remove(&key);
            self.tail = self.nodes[t].prev;
            if let Some(new_tail) = self.tail {
                self.nodes[new_tail].next = None;
            } else {
                self.head = None;
            }
        }
    }
}

fn main() {
    println!("=== 🦀 Project 038: LRU Cache ===");
    let mut cache = LruCache::new(2);
    cache.put("a", 1);
    cache.put("b", 2);
    println!("Get 'a': {:?}", cache.get(&"a"));
    cache.put("c", 3); // evicts 'b'
    println!("Get 'b' (evicted): {:?}", cache.get(&"b"));
    println!("Get 'c': {:?}", cache.get(&"c"));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_lru_eviction() {
        let mut cache = LruCache::new(2);
        cache.put("k1", 100);
        cache.put("k2", 200);
        assert_eq!(cache.get(&"k1"), Some(100));
        cache.put("k3", 300);
        assert_eq!(cache.get(&"k2"), None);
        assert_eq!(cache.get(&"k3"), Some(300));
    }
}
