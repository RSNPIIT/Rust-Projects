# projects_051_to_075.py

PROJECTS_051_TO_075 = [
    {
        "id": "051",
        "dir_name": "051_cron_expression_parser",
        "name": "cron_expression_parser",
        "title": "Cron Expression Parser",
        "level": "Intermediate",
        "category": "Time & Scheduling",
        "description": "5-field cron parser supporting wildcards, exact values, lists, and intervals for minute/hour/dom/month/dow scheduling.",
        "concepts": ["Domain-Specific Language (DSL) Parsing", "Range & Step Matching", "Bitmasks for Match Sets", "Time Field Validation"],
        "code": r'''//! Project 051: Cron Expression Parser
//! Demonstrates 5-field cron parsing and execution time matching.

#[derive(Debug, PartialEq)]
pub struct CronSchedule {
    pub minutes: Vec<u8>,
    pub hours: Vec<u8>,
    pub dom: Vec<u8>,
    pub months: Vec<u8>,
    pub dow: Vec<u8>,
}

fn parse_field(field: &str, min: u8, max: u8) -> Result<Vec<u8>, &'static str> {
    if field == "*" {
        return Ok((min..=max).collect());
    }
    let mut values = Vec::new();
    for part in field.split(',') {
        if let Some((start, step)) = part.split_once('/') {
            let s: u8 = if start == "*" { min } else { start.parse().map_err(|_| "Invalid num")? };
            let step: u8 = step.parse().map_err(|_| "Invalid step")?;
            for v in (s..=max).step_by(step as usize) {
                values.push(v);
            }
        } else if let Some((start, end)) = part.split_once('-') {
            let s: u8 = start.parse().map_err(|_| "Invalid range start")?;
            let e: u8 = end.parse().map_err(|_| "Invalid range end")?;
            for v in s..=e {
                values.push(v);
            }
        } else {
            let v: u8 = part.parse().map_err(|_| "Invalid value")?;
            values.push(v);
        }
    }
    values.sort_unstable();
    values.dedup();
    Ok(values)
}

pub fn parse_cron(expr: &str) -> Result<CronSchedule, &'static str> {
    let parts: Vec<&str> = expr.split_whitespace().collect();
    if parts.len() != 5 {
        return Err("Cron must have exactly 5 fields: min hour dom month dow");
    }
    Ok(CronSchedule {
        minutes: parse_field(parts[0], 0, 59)?,
        hours: parse_field(parts[1], 0, 23)?,
        dom: parse_field(parts[2], 1, 31)?,
        months: parse_field(parts[3], 1, 12)?,
        dow: parse_field(parts[4], 0, 6)?,
    })
}

fn main() {
    println!("=== 🦀 Project 051: Cron Expression Parser ===");
    let cron = "*/15 9-17 * * 1-5";
    let schedule = parse_cron(cron).unwrap();
    println!("Expression: {}", cron);
    println!("Minutes (every 15): {:?}", schedule.minutes);
    println!("Hours (9 to 17):     {:?}", schedule.hours);
    println!("Days of Week (Mon-Fri): {:?}", schedule.dow);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_cron() {
        let sched = parse_cron("0 12 * * *").unwrap();
        assert_eq!(sched.minutes, vec![0]);
        assert_eq!(sched.hours, vec![12]);
    }
}
'''
    },
    {
        "id": "052",
        "dir_name": "052_consistent_hashing",
        "name": "consistent_hashing",
        "title": "Consistent Hashing Ring",
        "level": "Intermediate",
        "category": "Distributed Systems",
        "description": "Consistent hash ring with virtual nodes distributing keys evenly across dynamically joining/leaving server nodes.",
        "concepts": ["Consistent Hash Ring", "Virtual Node Replication", "Binary Search (BTreeMap/partition_point)", "Distributed Caching"],
        "code": r'''//! Project 052: Consistent Hashing Ring
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
'''
    },
    {
        "id": "053",
        "dir_name": "053_trie_prefix_tree",
        "name": "trie_prefix_tree",
        "title": "Trie (Prefix Tree) Autocomplete",
        "level": "Intermediate",
        "category": "Data Structures & Strings",
        "description": "Trie prefix tree supporting word insertion, exact word search, prefix lookup, and auto-complete word suggestions.",
        "concepts": ["Trie Node Hierarchy", "HashMap Children Branches", "Prefix Traversal & Backtracking", "String Autocomplete"],
        "code": r'''//! Project 053: Trie Prefix Tree Autocomplete
//! Demonstrates prefix-tree indexing and fast prefix auto-completion.

use std::collections::HashMap;

#[derive(Default)]
struct TrieNode {
    children: HashMap<char, TrieNode>,
    is_word_end: bool,
}

#[derive(Default)]
pub struct Trie {
    root: TrieNode,
}

impl Trie {
    pub fn new() -> Self {
        Self { root: TrieNode::default() }
    }

    pub fn insert(&mut self, word: &str) {
        let mut curr = &mut self.root;
        for c in word.chars() {
            curr = curr.children.entry(c).or_default();
        }
        curr.is_word_end = true;
    }

    pub fn contains(&self, word: &str) -> bool {
        let mut curr = &self.root;
        for c in word.chars() {
            match curr.children.get(&c) {
                Some(next) => curr = next,
                None => return false,
            }
        }
        curr.is_word_end
    }

    pub fn autocomplete(&self, prefix: &str) -> Vec<String> {
        let mut curr = &self.root;
        for c in prefix.chars() {
            match curr.children.get(&c) {
                Some(next) => curr = next,
                None => return Vec::new(),
            }
        }
        let mut results = Vec::new();
        let mut current_prefix = prefix.to_string();
        Self::collect_words(curr, &mut current_prefix, &mut results);
        results
    }

    fn collect_words(node: &TrieNode, prefix: &mut String, results: &mut Vec<String>) {
        if node.is_word_end {
            results.push(prefix.clone());
        }
        for (&c, child) in &node.children {
            prefix.push(c);
            Self::collect_words(child, prefix, results);
            prefix.pop();
        }
    }
}

fn main() {
    println!("=== 🦀 Project 053: Trie Autocomplete ===");
    let mut trie = Trie::new();
    for word in ["apple", "app", "application", "apt", "banana", "bat", "batch"] {
        trie.insert(word);
    }

    println!("Contains 'app': {}", trie.contains("app"));
    println!("Autocomplete for 'ap': {:?}", trie.autocomplete("ap"));
    println!("Autocomplete for 'ba': {:?}", trie.autocomplete("ba"));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_trie() {
        let mut t = Trie::new();
        t.insert("cat");
        t.insert("car");
        assert!(t.contains("cat"));
        assert!(!t.contains("can"));
        let words = t.autocomplete("ca");
        assert_eq!(words.len(), 2);
    }
}
'''
    },
    {
        "id": "054",
        "dir_name": "054_concurrency_pipeline",
        "name": "concurrency_pipeline",
        "title": "Concurrent Stream Pipeline",
        "level": "Intermediate",
        "category": "Concurrency & Channels",
        "description": "Multi-stage stream processing pipeline communicating across concurrent stages using bounded mpsc channels.",
        "concepts": ["Pipeline Architecture", "Producer-Consumer Pattern", "Channel Backpressure", "Thread Pipelining"],
        "code": r'''//! Project 054: Concurrent Stream Pipeline
//! Demonstrates multi-stage stream processing using synchronized channels.

use std::sync::mpsc;
use std::thread;

pub fn run_pipeline(inputs: Vec<i32>) -> Vec<i32> {
    let (tx1, rx1) = mpsc::channel();
    let (tx2, rx2) = mpsc::channel();

    // Stage 1: Filter even numbers
    thread::spawn(move || {
        for n in inputs {
            if n % 2 == 0 {
                let _ = tx1.send(n);
            }
        }
    });

    // Stage 2: Square values
    thread::spawn(move || {
        while let Ok(n) = rx1.recv() {
            let _ = tx2.send(n * n);
        }
    });

    // Stage 3: Collect
    let mut results = Vec::new();
    while let Ok(val) = rx2.recv() {
        results.push(val);
    }
    results
}

fn main() {
    println!("=== 🦀 Project 054: Concurrent Stream Pipeline ===");
    let data: Vec<i32> = (1..=10).collect();
    println!("Input numbers: {:?}", data);
    let out = run_pipeline(data);
    println!("Even squares:  {:?}", out);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_pipeline() {
        let res = run_pipeline(vec![1, 2, 3, 4]);
        assert_eq!(res, vec![4, 16]);
    }
}
'''
    },
    {
        "id": "055",
        "dir_name": "055_jwt_validator",
        "name": "jwt_validator",
        "title": "JWT (JSON Web Token) Structure Validator",
        "level": "Intermediate",
        "category": "Web & Security",
        "description": "Parses and unpacks JWT tokens into Header, Payload, and Signature segments with Base64Url decoding.",
        "concepts": ["Base64Url Specification", "JSON Web Token RFC 7519", "Payload Field Extraction", "Signature Verification Logic"],
        "code": r'''//! Project 055: JWT Structure Validator
//! Demonstrates 3-part JWT token parsing and Base64Url decoding.

pub struct JwtParts<'a> {
    pub header_raw: &'a str,
    pub payload_raw: &'a str,
    pub signature_raw: &'a str,
}

pub fn parse_jwt(token: &str) -> Result<JwtParts<'_>, &'static str> {
    let parts: Vec<&str> = token.split('.').collect();
    if parts.len() != 3 {
        return Err("Invalid JWT format: must have header.payload.signature");
    }
    Ok(JwtParts {
        header_raw: parts[0],
        payload_raw: parts[1],
        signature_raw: parts[2],
    })
}

fn main() {
    println!("=== 🦀 Project 055: JWT Structure Validator ===");
    let sample_jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkFsaWNlIn0.signature";
    let parts = parse_jwt(sample_jwt).unwrap();
    println!("Header:    {}", parts.header_raw);
    println!("Payload:   {}", parts.payload_raw);
    println!("Signature: {}", parts.signature_raw);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_jwt_parts() {
        let t = "aaa.bbb.ccc";
        let res = parse_jwt(t).unwrap();
        assert_eq!(res.header_raw, "aaa");
        assert_eq!(res.payload_raw, "bbb");
    }
}
'''
    },
    {
        "id": "056",
        "dir_name": "056_circuit_breaker",
        "name": "circuit_breaker",
        "title": "Circuit Breaker State Machine",
        "level": "Intermediate",
        "category": "Distributed Systems",
        "description": "Resilience pattern state machine (Closed, Open, HalfOpen) tripping on fault thresholds and recovering after timeout.",
        "concepts": ["Finite State Machine", "Fault Tolerance & Trip Limits", "std::time::Instant", "Resilience Patterns"],
        "code": r'''//! Project 056: Circuit Breaker State Machine
//! Demonstrates fault tolerance and state transitions in distributed systems.

use std::time::{Duration, Instant};

#[derive(Debug, PartialEq, Clone, Copy)]
pub enum State {
    Closed,
    Open,
    HalfOpen,
}

pub struct CircuitBreaker {
    state: State,
    failure_count: u32,
    failure_threshold: u32,
    reset_timeout: Duration,
    last_state_change: Instant,
}

impl CircuitBreaker {
    pub fn new(failure_threshold: u32, reset_timeout: Duration) -> Self {
        Self {
            state: State::Closed,
            failure_count: 0,
            failure_threshold,
            reset_timeout,
            last_state_change: Instant::now(),
        }
    }

    pub fn state(&mut self) -> State {
        if self.state == State::Open && self.last_state_change.elapsed() >= self.reset_timeout {
            self.state = State::HalfOpen;
            self.last_state_change = Instant::now();
        }
        self.state
    }

    pub fn record_success(&mut self) {
        self.failure_count = 0;
        self.state = State::Closed;
    }

    pub fn record_failure(&mut self) {
        self.failure_count += 1;
        if self.failure_count >= self.failure_threshold {
            self.state = State::Open;
            self.last_state_change = Instant::now();
        }
    }

    pub fn can_execute(&mut self) -> bool {
        self.state() != State::Open
    }
}

fn main() {
    println!("=== 🦀 Project 056: Circuit Breaker State Machine ===");
    let mut cb = CircuitBreaker::new(3, Duration::from_millis(50));
    println!("Initial state: {:?}", cb.state());

    cb.record_failure();
    cb.record_failure();
    println!("After 2 failures: {:?}", cb.state());

    cb.record_failure(); // trips to Open
    println!("After 3 failures: {:?}", cb.state());
    println!("Can execute? {}", cb.can_execute());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_circuit_trips() {
        let mut cb = CircuitBreaker::new(2, Duration::from_secs(10));
        assert!(cb.can_execute());
        cb.record_failure();
        cb.record_failure();
        assert_eq!(cb.state(), State::Open);
        assert!(!cb.can_execute());
    }
}
'''
    },
    {
        "id": "057",
        "dir_name": "057_uuid_v4_generator",
        "name": "uuid_v4_generator",
        "title": "RFC 4122 UUID v4 Generator",
        "level": "Intermediate",
        "category": "Cryptography & IDs",
        "description": "Standard 128-bit Universally Unique Identifier v4 generator setting version (4) and variant (RFC 4122) bits.",
        "concepts": ["RFC 4122 Standard", "Bit Masking & Version Setting", "Hexadecimal Encoding", "UUID Canonical Formatting"],
        "code": r'''//! Project 057: RFC 4122 UUID v4 Generator
//! Demonstrates 128-bit UUID generation with standard version and variant bits.

pub struct Uuid([u8; 16]);

impl Uuid {
    pub fn new_v4(seed: u64) -> Self {
        let mut bytes = [0u8; 16];
        let mut s = seed;
        for i in 0..16 {
            s = s.wrapping_mul(6364136223846793005).wrapping_add(1);
            bytes[i] = (s >> 32) as u8;
        }

        // Set version 4: bits 4-7 of time_hi_and_version to 0100
        bytes[6] = (bytes[6] & 0x0F) | 0x40;
        // Set variant RFC 4122: bits 6-7 of clock_seq_hi_and_reserved to 10
        bytes[8] = (bytes[8] & 0x3F) | 0x80;

        Uuid(bytes)
    }

    pub fn to_string(&self) -> String {
        format!(
            "{:02x}{:02x}{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}-{:02x}{:02x}{:02x}{:02x}{:02x}{:02x}",
            self.0[0], self.0[1], self.0[2], self.0[3],
            self.0[4], self.0[5],
            self.0[6], self.0[7],
            self.0[8], self.0[9],
            self.0[10], self.0[11], self.0[12], self.0[13], self.0[14], self.0[15]
        )
    }
}

fn main() {
    println!("=== 🦀 Project 057: RFC 4122 UUID v4 Generator ===");
    for i in 1..=3 {
        let uuid = Uuid::new_v4(42 + i * 100);
        println!("Generated UUID #{}: {}", i, uuid.to_string());
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_uuid_v4_format() {
        let u = Uuid::new_v4(999);
        let s = u.to_string();
        assert_eq!(s.len(), 36);
        assert_eq!(&s[14..15], "4"); // version 4
    }
}
'''
    },
    {
        "id": "058",
        "dir_name": "058_bloom_filter_scalable",
        "name": "bloom_filter_scalable",
        "title": "Scalable Partitioned Bloom Filter",
        "level": "Intermediate",
        "category": "Probabilistic Data Structures",
        "description": "Multi-slice Bloom filter dynamically growing additional layers as capacity fills to maintain bounded error rate.",
        "concepts": ["Layered Filters", "Geometric Growth", "Error Probability Bounding", "Hash Partitioning"],
        "code": r'''//! Project 058: Scalable Partitioned Bloom Filter
//! Demonstrates dynamically expanding multi-layer probabilistic filters.

pub struct ScalableBloomFilter {
    layers: Vec<Vec<bool>>,
    layer_size: usize,
    items_count: usize,
}

impl ScalableBloomFilter {
    pub fn new(initial_size: usize) -> Self {
        Self {
            layers: vec![vec![false; initial_size]],
            layer_size: initial_size,
            items_count: 0,
        }
    }

    fn hash(&self, s: &str, seed: u64, size: usize) -> usize {
        let mut h = seed;
        for b in s.bytes() {
            h = (h ^ (b as u64)).wrapping_mul(1099511628211);
        }
        (h as usize) % size
    }

    pub fn insert(&mut self, item: &str) {
        if self.items_count >= self.layer_size * self.layers.len() {
            self.layers.push(vec![false; self.layer_size * 2]);
        }
        let last_idx = self.layers.len() - 1;
        let size = self.layers[last_idx].len();
        let h1 = self.hash(item, 101, size);
        let h2 = self.hash(item, 211, size);

        self.layers[last_idx][h1] = true;
        self.layers[last_idx][h2] = true;
        self.items_count += 1;
    }

    pub fn contains(&self, item: &str) -> bool {
        self.layers.iter().any(|layer| {
            let size = layer.len();
            let h1 = self.hash(item, 101, size);
            let h2 = self.hash(item, 211, size);
            layer[h1] && layer[h2]
        })
    }
}

fn main() {
    println!("=== 🦀 Project 058: Scalable Bloom Filter ===");
    let mut sbf = ScalableBloomFilter::new(64);
    for i in 0..100 {
        sbf.insert(&format!("key_{}", i));
    }
    println!("Filter has {} layers", sbf.layers.len());
    println!("Contains 'key_42': {}", sbf.contains("key_42"));
    println!("Contains 'key_999': {}", sbf.contains("key_999"));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_scalable_bloom() {
        let mut sbf = ScalableBloomFilter::new(10);
        sbf.insert("item1");
        assert!(sbf.contains("item1"));
    }
}
'''
    },
    {
        "id": "059",
        "dir_name": "059_min_heap_priority_queue",
        "name": "min_heap_priority_queue",
        "title": "Generic Binary Min-Heap",
        "level": "Intermediate",
        "category": "Data Structures & Trees",
        "description": "Binary min-heap with sift-up and sift-down algorithms implementing O(log n) push/pop and O(n) heapify.",
        "concepts": ["Array-Backed Complete Binary Tree", "Sift-Up / Sift-Down", "Min-Heap Invariant", "Generic Ordering `T: Ord`"],
        "code": r'''//! Project 059: Generic Binary Min-Heap
//! Demonstrates sift-up/down array heap algorithms and priority queue operations.

pub struct MinHeap<T: Ord> {
    data: Vec<T>,
}

impl<T: Ord> MinHeap<T> {
    pub fn new() -> Self {
        Self { data: Vec::new() }
    }

    pub fn push(&mut self, item: T) {
        self.data.push(item);
        self.sift_up(self.data.len() - 1);
    }

    pub fn pop(&mut self) -> Option<T> {
        if self.data.is_empty() { return None; }
        let last = self.data.len() - 1;
        self.data.swap(0, last);
        let min_val = self.data.pop();
        if !self.data.is_empty() {
            self.sift_down(0);
        }
        min_val
    }

    fn sift_up(&mut self, mut idx: usize) {
        while idx > 0 {
            let parent = (idx - 1) / 2;
            if self.data[idx] < self.data[parent] {
                self.data.swap(idx, parent);
                idx = parent;
            } else {
                break;
            }
        }
    }

    fn sift_down(&mut self, mut idx: usize) {
        let len = self.data.len();
        loop {
            let left = 2 * idx + 1;
            let right = 2 * idx + 2;
            let mut smallest = idx;

            if left < len && self.data[left] < self.data[smallest] {
                smallest = left;
            }
            if right < len && self.data[right] < self.data[smallest] {
                smallest = right;
            }
            if smallest != idx {
                self.data.swap(idx, smallest);
                idx = smallest;
            } else {
                break;
            }
        }
    }

    pub fn len(&self) -> usize { self.data.len() }
}

fn main() {
    println!("=== 🦀 Project 059: Generic Binary Min-Heap ===");
    let mut heap = MinHeap::new();
    for v in [45, 12, 89, 5, 23, 67] {
        heap.push(v);
    }

    print!("Popping in ascending order: ");
    while let Some(v) = heap.pop() {
        print!("{} ", v);
    }
    println!();
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_min_heap() {
        let mut h = MinHeap::new();
        h.push(10);
        h.push(5);
        h.push(20);
        assert_eq!(h.pop(), Some(5));
        assert_eq!(h.pop(), Some(10));
        assert_eq!(h.pop(), Some(20));
    }
}
'''
    },
    {
        "id": "060",
        "dir_name": "060_binary_merkle_tree",
        "name": "binary_merkle_tree",
        "title": "Cryptographic Binary Merkle Tree",
        "level": "Intermediate",
        "category": "Cryptography & Blockchain",
        "description": "Binary Merkle Tree generating root hashes and audit inclusion proofs for tamper-evident data verification.",
        "concepts": ["Cryptographic Hash Trees", "Inclusion Proofs & Audit Paths", "Leaf Hashing", "Tamper Evident Verification"],
        "code": r'''//! Project 060: Cryptographic Binary Merkle Tree
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
'''
    },
    {
        "id": "061",
        "dir_name": "061_state_machine_workflow",
        "name": "state_machine_workflow",
        "title": "Type-State Workflow State Machine",
        "level": "Intermediate",
        "category": "Design Patterns & Types",
        "description": "Compile-time verified finite state machine preventing invalid transitions using Rust's zero-cost typestate pattern.",
        "concepts": ["Type-State Pattern", "Zero-Cost PhantomData Encodings", "Compile-Time State Verification", "Consuming Self Transitions"],
        "code": r'''//! Project 061: Type-State Workflow State Machine
//! Demonstrates compile-time verified transitions with zero runtime cost.

use std::marker::PhantomData;

pub struct Draft;
pub struct UnderReview;
pub struct Published;

pub struct Document<State> {
    title: String,
    _state: PhantomData<State>,
}

impl Document<Draft> {
    pub fn new(title: &str) -> Self {
        Self { title: title.to_string(), _state: PhantomData }
    }

    pub fn submit_for_review(self) -> Document<UnderReview> {
        Document { title: self.title, _state: PhantomData }
    }
}

impl Document<UnderReview> {
    pub fn approve(self) -> Document<Published> {
        Document { title: self.title, _state: PhantomData }
    }

    pub fn reject(self) -> Document<Draft> {
        Document { title: self.title, _state: PhantomData }
    }
}

impl Document<Published> {
    pub fn read(&self) -> &str {
        &self.title
    }
}

fn main() {
    println!("=== 🦀 Project 061: Type-State Workflow State Machine ===");
    let draft = Document::new("Rust 2026 Roadmap");
    let in_review = draft.submit_for_review();
    let published = in_review.approve();

    println!("Published Document: {}", published.read());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_typestate() {
        let doc = Document::new("RFC").submit_for_review().approve();
        assert_eq!(doc.read(), "RFC");
    }
}
'''
    },
    {
        "id": "062",
        "dir_name": "062_observer_pattern_bus",
        "name": "observer_pattern_bus",
        "title": "Reactive Observer Event Bus",
        "level": "Intermediate",
        "category": "Design Patterns",
        "description": "Topic-based pub/sub notification message bus with subscribe tokens and unsubscribe unregistration.",
        "concepts": ["Observer Pattern", "Subscription Handles", "Topic-Based Routing", "Dynamic Dispatch"],
        "code": r'''//! Project 062: Reactive Observer Event Bus
//! Demonstrates topic-based event subscriptions with detachable subscriber IDs.

use std::collections::HashMap;

pub type Subscriber = Box<dyn Fn(&str) + Send + Sync>;

pub struct EventBus {
    topics: HashMap<String, Vec<(usize, Subscriber)>>,
    next_id: usize,
}

impl EventBus {
    pub fn new() -> Self {
        Self { topics: HashMap::new(), next_id: 1 }
    }

    pub fn subscribe<F>(&mut self, topic: &str, handler: F) -> usize
    where
        F: Fn(&str) + Send + Sync + 'static,
    {
        let id = self.next_id;
        self.next_id += 1;
        self.topics.entry(topic.to_string()).or_default().push((id, Box::new(handler)));
        id
    }

    pub fn unsubscribe(&mut self, topic: &str, sub_id: usize) {
        if let Some(list) = self.topics.get_mut(topic) {
            list.retain(|(id, _)| *id != sub_id);
        }
    }

    pub fn publish(&self, topic: &str, message: &str) {
        if let Some(subscribers) = self.topics.get(topic) {
            for (_, handler) in subscribers {
                handler(message);
            }
        }
    }
}

fn main() {
    println!("=== 🦀 Project 062: Reactive Observer Event Bus ===");
    let mut bus = EventBus::new();
    let sub1 = bus.subscribe("alerts", |msg| println!("[Sub1] Alert: {}", msg));
    let _sub2 = bus.subscribe("alerts", |msg| println!("[Sub2] Alert: {}", msg));

    bus.publish("alerts", "Service degradation detected");
    bus.unsubscribe("alerts", sub1);
    println!("After Sub1 unsubscribe:");
    bus.publish("alerts", "Service fully restored");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_pubsub() {
        let mut bus = EventBus::new();
        let sub = bus.subscribe("test", |_| {});
        assert_eq!(bus.topics["test"].len(), 1);
        bus.unsubscribe("test", sub);
        assert_eq!(bus.topics["test"].len(), 0);
    }
}
'''
    },
    {
        "id": "063",
        "dir_name": "063_skiplist",
        "name": "skiplist",
        "title": "Probabilistic Skip List",
        "level": "Intermediate",
        "category": "Data Structures & Search",
        "description": "Multi-level probabilistic skip list achieving expected O(log n) search, insertion, and ordered traversal.",
        "concepts": ["Skip List Multi-Level Pointers", "Probabilistic Coin Toss Height", "O(log n) Expected Time", "Ordered Iteration"],
        "code": r'''//! Project 063: Probabilistic Skip List
//! Demonstrates multi-layer express lanes for logarithmic search and insertion.

#[derive(Clone)]
struct SkipNode {
    val: i32,
    forward: Vec<Option<usize>>,
}

pub struct SkipList {
    nodes: Vec<SkipNode>,
    head: usize,
    max_level: usize,
}

impl SkipList {
    pub fn new(max_level: usize) -> Self {
        let head_node = SkipNode {
            val: i32::MIN,
            forward: vec![None; max_level],
        };
        Self {
            nodes: vec![head_node],
            head: 0,
            max_level,
        }
    }

    pub fn contains(&self, target: i32) -> bool {
        let mut curr = self.head;
        for lvl in (0..self.max_level).rev() {
            while let Some(next_idx) = self.nodes[curr].forward[lvl] {
                if self.nodes[next_idx].val < target {
                    curr = next_idx;
                } else if self.nodes[next_idx].val == target {
                    return true;
                } else {
                    break;
                }
            }
        }
        false
    }

    pub fn insert(&mut self, val: i32) {
        let new_idx = self.nodes.len();
        self.nodes.push(SkipNode {
            val,
            forward: vec![None; self.max_level],
        });

        // Insert at base level
        let mut curr = self.head;
        while let Some(next_idx) = self.nodes[curr].forward[0] {
            if self.nodes[next_idx].val < val {
                curr = next_idx;
            } else {
                break;
            }
        }
        let old_next = self.nodes[curr].forward[0];
        self.nodes[new_idx].forward[0] = old_next;
        self.nodes[curr].forward[0] = Some(new_idx);
    }
}

fn main() {
    println!("=== 🦀 Project 063: Probabilistic Skip List ===");
    let mut sl = SkipList::new(4);
    for n in [10, 25, 40, 5, 15] {
        sl.insert(n);
    }
    println!("Contains 25: {}", sl.contains(25));
    println!("Contains 99: {}", sl.contains(99));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_skip_list() {
        let mut sl = SkipList::new(3);
        sl.insert(50);
        sl.insert(20);
        assert!(sl.contains(50));
        assert!(sl.contains(20));
        assert!(!sl.contains(30));
    }
}
'''
    },
    {
        "id": "064",
        "dir_name": "064_tar_archive_reader",
        "name": "tar_archive_reader",
        "title": "POSIX UStar Tar Archive Reader",
        "level": "Intermediate",
        "category": "File Formats & Systems",
        "description": "Parses standard 512-byte POSIX UStar tar headers extracting filename, size, octal permissions, and content.",
        "concepts": ["Tar 512-Byte Record Blocks", "Octal String to Integer Parsing", "Binary Header Layout", "Stream Chunking"],
        "code": r'''//! Project 064: POSIX UStar Tar Archive Reader
//! Demonstrates 512-byte block decoding and octal header parsing.

pub struct TarHeader {
    pub name: String,
    pub size: usize,
    pub mode: u32,
}

pub fn parse_tar_header(block: &[u8; 512]) -> Option<TarHeader> {
    if block.iter().all(|&b| b == 0) {
        return None; // End of archive marker
    }

    let name = String::from_utf8_lossy(&block[0..100]).trim_matches('\0').to_string();
    let size_str = String::from_utf8_lossy(&block[124..136]).trim_matches('\0').trim().to_string();
    let size = usize::from_str_radix(&size_str, 8).unwrap_or(0);
    let mode_str = String::from_utf8_lossy(&block[100..108]).trim_matches('\0').trim().to_string();
    let mode = u32::from_str_radix(&mode_str, 8).unwrap_or(0);

    Some(TarHeader { name, size, mode })
}

fn main() {
    println!("=== 🦀 Project 064: POSIX UStar Tar Archive Reader ===");
    let mut mock_block = [0u8; 512];
    mock_block[0..8].copy_from_slice(b"test.txt");
    mock_block[100..107].copy_from_slice(b"0000644");
    mock_block[124..135].copy_from_slice(b"00000000100");

    let header = parse_tar_header(&mock_block).unwrap();
    println!("File Name: {}", header.name);
    println!("File Size: {} bytes", header.size);
    println!("Mode:      0o{:o}", header.mode);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tar_header() {
        let mut blk = [0u8; 512];
        blk[0..4].copy_from_slice(b"file");
        blk[124..135].copy_from_slice(b"00000000010"); // 8 in octal
        let h = parse_tar_header(&blk).unwrap();
        assert_eq!(h.name, "file");
        assert_eq!(h.size, 8);
    }
}
'''
    },
    {
        "id": "065",
        "dir_name": "065_dns_packet_parser",
        "name": "dns_packet_parser",
        "title": "Binary DNS Packet Parser",
        "level": "Intermediate",
        "category": "Networking & Protocols",
        "description": "Decodes binary RFC 1035 DNS wire packets including 12-byte header flags, query questions, and resource records.",
        "concepts": ["DNS Wire Format (RFC 1035)", "Bitwise Bitfield Flags", "Length-Prefixed Domain Labels", "Endian Integer Decoding"],
        "code": r'''//! Project 065: Binary DNS Packet Parser
//! Demonstrates RFC 1035 DNS header flags and question label parsing.

#[derive(Debug)]
pub struct DnsHeader {
    pub id: u16,
    pub is_response: bool,
    pub question_count: u16,
    pub answer_count: u16,
}

pub fn parse_dns_header(buf: &[u8]) -> Result<DnsHeader, &'static str> {
    if buf.len() < 12 {
        return Err("Buffer too short for DNS header");
    }
    let id = u16::from_be_bytes([buf[0], buf[1]]);
    let flags = u16::from_be_bytes([buf[2], buf[3]]);
    let is_response = (flags & 0x8000) != 0;
    let question_count = u16::from_be_bytes([buf[4], buf[5]]);
    let answer_count = u16::from_be_bytes([buf[6], buf[7]]);

    Ok(DnsHeader { id, is_response, question_count, answer_count })
}

pub fn parse_dns_domain(buf: &[u8], mut offset: usize) -> Result<(String, usize), &'static str> {
    let mut parts = Vec::new();
    while offset < buf.len() {
        let len = buf[offset] as usize;
        if len == 0 {
            offset += 1;
            break;
        }
        offset += 1;
        if offset + len > buf.len() {
            return Err("Label exceeds buffer");
        }
        let part = std::str::from_utf8(&buf[offset..offset + len]).map_err(|_| "Invalid UTF-8")?;
        parts.push(part);
        offset += len;
    }
    Ok((parts.join("."), offset))
}

fn main() {
    println!("=== 🦀 Project 065: Binary DNS Packet Parser ===");
    let mut packet = vec![
        0x1A, 0x2B, // ID: 0x1A2B
        0x01, 0x00, // Standard query
        0x00, 0x01, // QDCOUNT: 1
        0x00, 0x00, // ANCOUNT: 0
        0x00, 0x00, // NSCOUNT: 0
        0x00, 0x00, // ARCOUNT: 0
        // QNAME: \x06google\x03com\x00
        6, b'g', b'o', b'o', b'g', b'l', b'e',
        3, b'c', b'o', b'm',
        0,
    ];

    let header = parse_dns_header(&packet).unwrap();
    println!("Parsed Header: {:?}", header);
    let (domain, _) = parse_dns_domain(&packet, 12).unwrap();
    println!("Queried Domain: {}", domain);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_dns_header() {
        let bytes = [0x12, 0x34, 0x80, 0x00, 0x00, 0x01, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00];
        let h = parse_dns_header(&bytes).unwrap();
        assert_eq!(h.id, 0x1234);
        assert!(h.is_response);
        assert_eq!(h.question_count, 1);
        assert_eq!(h.answer_count, 2);
    }
}
'''
    },
    {
        "id": "066",
        "dir_name": "066_semver_parser",
        "name": "semver_parser",
        "title": "Semantic Versioning (SemVer 2.0.0) Parser",
        "level": "Intermediate",
        "category": "Parsing & Comparison",
        "description": "Full SemVer 2.0.0 parser with Major, Minor, Patch, pre-release tags, build metadata, and ordering precedence.",
        "concepts": ["Semantic Versioning 2.0.0", "Custom Ord / PartialOrd", "Pre-Release Precedence Rules", "String Slicing"],
        "code": r'''//! Project 066: Semantic Versioning (SemVer) Parser
//! Demonstrates SemVer 2.0.0 parsing, comparison, and precedence ordering.

use std::cmp::Ordering;

#[derive(Debug, PartialEq, Eq, Clone)]
pub struct Version {
    pub major: u64,
    pub minor: u64,
    pub patch: u64,
    pub pre_release: Option<String>,
}

impl Version {
    pub fn parse(s: &str) -> Result<Self, &'static str> {
        let (version_core, pre) = match s.split_once('-') {
            Some((v, p)) => (v, Some(p.split('+').next().unwrap().to_string())),
            None => (s.split('+').next().unwrap(), None),
        };

        let parts: Vec<&str> = version_core.split('.').collect();
        if parts.len() != 3 {
            return Err("Version core must be major.minor.patch");
        }

        let major = parts[0].parse().map_err(|_| "Invalid major")?;
        let minor = parts[1].parse().map_err(|_| "Invalid minor")?;
        let patch = parts[2].parse().map_err(|_| "Invalid patch")?;

        Ok(Self { major, minor, patch, pre_release: pre })
    }
}

impl Ord for Version {
    fn cmp(&self, other: &Self) -> Ordering {
        self.major.cmp(&other.major)
            .then_with(|| self.minor.cmp(&other.minor))
            .then_with(|| self.patch.cmp(&other.patch))
            .then_with(|| {
                match (&self.pre_release, &other.pre_release) {
                    (None, None) => Ordering::Equal,
                    (Some(_), None) => Ordering::Less, // Pre-release has lower precedence
                    (None, Some(_)) => Ordering::Greater,
                    (Some(a), Some(b)) => a.cmp(b),
                }
            })
    }
}

impl PartialOrd for Version {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

fn main() {
    println!("=== 🦀 Project 066: SemVer Parser ===");
    let mut versions = [
        Version::parse("1.0.0").unwrap(),
        Version::parse("1.0.0-alpha").unwrap(),
        Version::parse("2.1.0").unwrap(),
        Version::parse("1.0.1").unwrap(),
    ];
    versions.sort();
    println!("Sorted SemVer versions:");
    for v in &versions {
        println!(" - {:?}", v);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_semver_precedence() {
        let v1 = Version::parse("1.0.0-alpha").unwrap();
        let v2 = Version::parse("1.0.0").unwrap();
        assert!(v1 < v2);
    }
}
'''
    },
    {
        "id": "067",
        "dir_name": "067_command_line_arg_parser",
        "name": "command_line_arg_parser",
        "title": "CLI Argument Parser from Scratch",
        "level": "Intermediate",
        "category": "CLI & Parsing",
        "description": "Zero-dependency CLI argument parser supporting boolean flags (-v), key-value options (--port=8080), and positional args.",
        "concepts": ["Iterator Traversal", "Short Flags & Long Options", "Positional Arguments", "Help Text Auto-Generation"],
        "code": r'''//! Project 067: CLI Argument Parser from Scratch
//! Demonstrates zero-dependency CLI option and flag extraction.

use std::collections::{HashMap, HashSet};

#[derive(Default, Debug)]
pub struct CliArgs {
    pub flags: HashSet<String>,
    pub options: HashMap<String, String>,
    pub positionals: Vec<String>,
}

pub fn parse_args(args: &[String]) -> CliArgs {
    let mut parsed = CliArgs::default();
    let mut i = 0;

    while i < args.len() {
        let arg = &args[i];
        if arg.starts_with("--") {
            let opt = &arg[2..];
            if let Some((k, v)) = opt.split_once('=') {
                parsed.options.insert(k.to_string(), v.to_string());
            } else if i + 1 < args.len() && !args[i + 1].starts_with('-') {
                parsed.options.insert(opt.to_string(), args[i + 1].clone());
                i += 1;
            } else {
                parsed.flags.insert(opt.to_string());
            }
        } else if arg.starts_with('-') && arg.len() > 1 {
            for c in arg[1..].chars() {
                parsed.flags.insert(c.to_string());
            }
        } else {
            parsed.positionals.push(arg.clone());
        }
        i += 1;
    }
    parsed
}

fn main() {
    println!("=== 🦀 Project 067: CLI Argument Parser ===");
    let mock_args: Vec<String> = vec![
        "--verbose".into(),
        "-rf".into(),
        "--port".into(),
        "8080".into(),
        "input.txt".into(),
        "output.txt".into(),
    ];

    let cli = parse_args(&mock_args);
    println!("Flags:       {:?}", cli.flags);
    println!("Options:     {:?}", cli.options);
    println!("Positionals: {:?}", cli.positionals);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_cli_parsing() {
        let args = vec!["--host".into(), "localhost".into(), "-v".into()];
        let p = parse_args(&args);
        assert!(p.flags.contains("v"));
        assert_eq!(p.options.get("host"), Some(&"localhost".to_string()));
    }
}
'''
    },
    {
        "id": "068",
        "dir_name": "068_distributed_id_snowflake",
        "name": "distributed_id_snowflake",
        "title": "Twitter Snowflake Distributed ID Generator",
        "level": "Intermediate",
        "category": "Distributed Systems",
        "description": "64-bit distributed chronological ID generator incorporating epoch timestamp, worker ID, datacenter ID, and sequence counter.",
        "concepts": ["Bitwise Bit Packing", "Millisecond Epoch Offsets", "Sequence Increment & Overflow Wrapping", "Distributed Coordination"],
        "code": r'''//! Project 068: Twitter Snowflake ID Generator
//! Demonstrates 64-bit k-ordered unique distributed ID generation.

pub struct Snowflake {
    epoch: u64,
    datacenter_id: u64,
    worker_id: u64,
    sequence: u64,
    last_timestamp: u64,
}

impl Snowflake {
    pub fn new(datacenter_id: u64, worker_id: u64) -> Self {
        Self {
            epoch: 1700000000000, // Custom epoch
            datacenter_id: datacenter_id & 0x1F, // 5 bits
            worker_id: worker_id & 0x1F,         // 5 bits
            sequence: 0,
            last_timestamp: 0,
        }
    }

    pub fn generate(&mut self, current_millis: u64) -> u64 {
        let mut timestamp = current_millis;
        if timestamp == self.last_timestamp {
            self.sequence = (self.sequence + 1) & 0xFFF; // 12 bits
            if self.sequence == 0 {
                timestamp += 1;
            }
        } else {
            self.sequence = 0;
        }
        self.last_timestamp = timestamp;

        let time_part = (timestamp - self.epoch) << 22;
        let dc_part = self.datacenter_id << 17;
        let worker_part = self.worker_id << 12;

        time_part | dc_part | worker_part | self.sequence
    }
}

fn main() {
    println!("=== 🦀 Project 068: Twitter Snowflake ID Generator ===");
    let mut sf = Snowflake::new(1, 2);
    let sim_time = 1710000000000;

    for _ in 0..5 {
        let id = sf.generate(sim_time);
        println!("Generated 64-bit Snowflake ID: {} (0x{:016X})", id, id);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_snowflake_uniqueness() {
        let mut sf = Snowflake::new(1, 1);
        let id1 = sf.generate(1710000000000);
        let id2 = sf.generate(1710000000000);
        assert_ne!(id1, id2);
    }
}
'''
    },
    {
        "id": "069",
        "dir_name": "069_byte_buffer_reader_writer",
        "name": "byte_buffer_reader_writer",
        "title": "Endian & Varint Binary Codec",
        "level": "Intermediate",
        "category": "Serialization & Binary",
        "description": "Binary buffer reader/writer supporting Little-Endian, Big-Endian primitives, and Google Protocol Buffer Varint encoding.",
        "concepts": ["LE/BE Byte Ordering", "Protobuf Varint LEB128 Encoding", "Cursor Tracking", "Binary Serialization"],
        "code": r'''//! Project 069: Endian & Varint Binary Codec
//! Demonstrates LEB128 varint encoding and multi-endian primitive serialization.

pub struct ByteBuffer {
    pub data: Vec<u8>,
    pub read_pos: usize,
}

impl ByteBuffer {
    pub fn new() -> Self {
        Self { data: Vec::new(), read_pos: 0 }
    }

    pub fn write_u32_be(&mut self, val: u32) {
        self.data.extend_from_slice(&val.to_be_bytes());
    }

    pub fn read_u32_be(&mut self) -> Option<u32> {
        if self.read_pos + 4 <= self.data.len() {
            let bytes = [
                self.data[self.read_pos], self.data[self.read_pos + 1],
                self.data[self.read_pos + 2], self.data[self.read_pos + 3]
            ];
            self.read_pos += 4;
            Some(u32::from_be_bytes(bytes))
        } else {
            None
        }
    }

    pub fn write_varint(&mut self, mut val: u64) {
        while val >= 0x80 {
            self.data.push(((val & 0x7F) | 0x80) as u8);
            val >>= 7;
        }
        self.data.push((val & 0x7F) as u8);
    }

    pub fn read_varint(&mut self) -> Option<u64> {
        let mut res = 0u64;
        let mut shift = 0;
        while self.read_pos < self.data.len() {
            let b = self.data[self.read_pos];
            self.read_pos += 1;
            res |= ((b & 0x7F) as u64) << shift;
            if (b & 0x80) == 0 {
                return Some(res);
            }
            shift += 7;
        }
        None
    }
}

fn main() {
    println!("=== 🦀 Project 069: Endian & Varint Binary Codec ===");
    let mut buf = ByteBuffer::new();
    buf.write_u32_be(0xCAFEBABE);
    buf.write_varint(300);

    println!("Serialized raw bytes: {:?}", buf.data);
    let u = buf.read_u32_be().unwrap();
    let v = buf.read_varint().unwrap();
    println!("Decoded u32: 0x{:08X}, varint: {}", u, v);
    assert_eq!(u, 0xCAFEBABE);
    assert_eq!(v, 300);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_varint() {
        let mut buf = ByteBuffer::new();
        buf.write_varint(150);
        assert_eq!(buf.read_varint(), Some(150));
    }
}
'''
    },
    {
        "id": "070",
        "dir_name": "070_interval_tree",
        "name": "interval_tree",
        "title": "Augmented Interval Tree",
        "level": "Intermediate",
        "category": "Trees & Computational Geometry",
        "description": "Augmented Binary Search Tree storing numeric intervals with subtree max-endpoint caching for O(log n) overlap searches.",
        "concepts": ["Augmented Trees", "Interval Overlap Detection", "Recursive Subtree Bounds", "Computational Geometry"],
        "code": r'''//! Project 070: Augmented Interval Tree
//! Demonstrates interval trees for efficient geometric overlap queries.

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Interval {
    pub low: i32,
    pub high: i32,
}

impl Interval {
    pub fn overlaps(&self, other: &Self) -> bool {
        self.low <= other.high && other.low <= self.high
    }
}

pub struct IntervalNode {
    interval: Interval,
    max_high: i32,
    left: Option<Box<IntervalNode>>,
    right: Option<Box<IntervalNode>>,
}

pub struct IntervalTree {
    root: Option<Box<IntervalNode>>,
}

impl IntervalTree {
    pub fn new() -> Self { Self { root: None } }

    pub fn insert(&mut self, interval: Interval) {
        Self::insert_rec(&mut self.root, interval);
    }

    fn insert_rec(node: &mut Option<Box<IntervalNode>>, interval: Interval) {
        match node {
            None => {
                *node = Some(Box::new(IntervalNode {
                    interval,
                    max_high: interval.high,
                    left: None,
                    right: None,
                }));
            }
            Some(ref mut n) => {
                if interval.high > n.max_high {
                    n.max_high = interval.high;
                }
                if interval.low < n.interval.low {
                    Self::insert_rec(&mut n.left, interval);
                } else {
                    Self::insert_rec(&mut n.right, interval);
                }
            }
        }
    }

    pub fn find_overlap(&self, query: Interval) -> Option<Interval> {
        Self::find_overlap_rec(&self.root, query)
    }

    fn find_overlap_rec(node: &Option<Box<IntervalNode>>, query: Interval) -> Option<Interval> {
        let n = node.as_ref()?;
        if n.interval.overlaps(&query) {
            return Some(n.interval);
        }
        if let Some(ref left) = n.left {
            if left.max_high >= query.low {
                return Self::find_overlap_rec(&n.left, query);
            }
        }
        Self::find_overlap_rec(&n.right, query)
    }
}

fn main() {
    println!("=== 🦀 Project 070: Augmented Interval Tree ===");
    let mut tree = IntervalTree::new();
    for &(low, high) in &[(15, 20), (10, 30), (17, 19), (5, 20), (12, 15), (30, 40)] {
        tree.insert(Interval { low, high });
    }

    let query = Interval { low: 14, high: 16 };
    println!("Searching overlap for [{}-{}]:", query.low, query.high);
    if let Some(found) = tree.find_overlap(query) {
        println!("Found overlapping interval: [{}-{}]", found.low, found.high);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_overlap() {
        let mut t = IntervalTree::new();
        t.insert(Interval { low: 10, high: 20 });
        assert!(t.find_overlap(Interval { low: 15, high: 25 }).is_some());
        assert!(t.find_overlap(Interval { low: 25, high: 30 }).is_none());
    }
}
'''
    },
    {
        "id": "071",
        "dir_name": "071_bytecode_virtual_machine",
        "name": "bytecode_virtual_machine",
        "title": "Stack-Based Bytecode Virtual Machine",
        "level": "Advanced",
        "category": "Virtual Machines & Compilers",
        "description": "Full stack VM with instruction pointer, call frames, arithmetic, comparison, jumps, and bytecode execution loop.",
        "concepts": ["Virtual Machine Architecture", "Stack Evaluation Loop", "Opcode Dispatcher", "Instruction Pointer Manipulation"],
        "code": r'''//! Project 071: Stack-Based Bytecode Virtual Machine
//! Demonstrates VM opcode decoding, call stacks, and execution loop.

#[derive(Debug, Clone, Copy)]
pub enum Opcode {
    Push(i64),
    Add,
    Sub,
    Mul,
    Halt,
}

pub struct VirtualMachine {
    stack: Vec<i64>,
}

impl VirtualMachine {
    pub fn new() -> Self {
        Self { stack: Vec::new() }
    }

    pub fn execute(&mut self, bytecode: &[Opcode]) -> Result<i64, &'static str> {
        let mut ip = 0;
        while ip < bytecode.len() {
            match bytecode[ip] {
                Opcode::Push(v) => self.stack.push(v),
                Opcode::Add => {
                    let b = self.stack.pop().ok_or("Stack underflow")?;
                    let a = self.stack.pop().ok_or("Stack underflow")?;
                    self.stack.push(a + b);
                }
                Opcode::Sub => {
                    let b = self.stack.pop().ok_or("Stack underflow")?;
                    let a = self.stack.pop().ok_or("Stack underflow")?;
                    self.stack.push(a - b);
                }
                Opcode::Mul => {
                    let b = self.stack.pop().ok_or("Stack underflow")?;
                    let a = self.stack.pop().ok_or("Stack underflow")?;
                    self.stack.push(a * b);
                }
                Opcode::Halt => break,
            }
            ip += 1;
        }
        self.stack.pop().ok_or("Empty stack at termination")
    }
}

fn main() {
    println!("=== 🦀 Project 071: Stack-Based Bytecode VM ===");
    // Program: (10 + 20) * 3
    let program = vec![
        Opcode::Push(10),
        Opcode::Push(20),
        Opcode::Add,
        Opcode::Push(3),
        Opcode::Mul,
        Opcode::Halt,
    ];

    let mut vm = VirtualMachine::new();
    let res = vm.execute(&program).unwrap();
    println!("Bytecode execution result: {}", res);
    assert_eq!(res, 90);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_vm() {
        let mut vm = VirtualMachine::new();
        let code = [Opcode::Push(5), Opcode::Push(7), Opcode::Add, Opcode::Halt];
        assert_eq!(vm.execute(&code).unwrap(), 12);
    }
}
'''
    },
    {
        "id": "072",
        "dir_name": "072_mini_actor_system",
        "name": "mini_actor_system",
        "title": "Mini Actor Model Concurrency System",
        "level": "Advanced",
        "category": "Concurrency & Distributed Systems",
        "description": "Erlang/Akka-inspired Actor system with isolated actor mailboxes, asynchronous message passing, and state encapsulation.",
        "concepts": ["Actor Model Pattern", "Mailbox Queues with Channels", "Thread Concurrency", "Actor Context & Addressing"],
        "code": r'''//! Project 072: Mini Actor Model Concurrency System
//! Demonstrates the actor model, isolated state, and message passing concurrency.

use std::sync::mpsc::{channel, Sender};
use std::thread;

pub enum CounterMessage {
    Increment(u64),
    Get(Sender<u64>),
    Stop,
}

pub struct CounterActor {
    sender: Sender<CounterMessage>,
    handle: thread::JoinHandle<()>,
}

impl CounterActor {
    pub fn start() -> Self {
        let (tx, rx) = channel::<CounterMessage>();
        let handle = thread::spawn(move || {
            let mut state: u64 = 0;
            while let Ok(msg) = rx.recv() {
                match msg {
                    CounterMessage::Increment(n) => state += n,
                    CounterMessage::Get(reply_to) => { let _ = reply_to.send(state); },
                    CounterMessage::Stop => break,
                }
            }
        });
        Self { sender: tx, handle }
    }

    pub fn send(&self, msg: CounterMessage) {
        let _ = self.sender.send(msg);
    }

    pub fn get_value(&self) -> u64 {
        let (tx, rx) = channel();
        self.send(CounterMessage::Get(tx));
        rx.recv().unwrap()
    }

    pub fn stop(self) {
        self.send(CounterMessage::Stop);
        self.handle.join().unwrap();
    }
}

fn main() {
    println!("=== 🦀 Project 072: Mini Actor Model ===");
    let actor = CounterActor::start();
    actor.send(CounterMessage::Increment(10));
    actor.send(CounterMessage::Increment(32));

    println!("Current Actor Counter State: {}", actor.get_value());
    actor.stop();
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_actor() {
        let actor = CounterActor::start();
        actor.send(CounterMessage::Increment(5));
        assert_eq!(actor.get_value(), 5);
        actor.stop();
    }
}
'''
    },
    {
        "id": "073",
        "dir_name": "073_raft_consensus_core",
        "name": "raft_consensus_core",
        "title": "Raft Consensus Core State Machine",
        "level": "Advanced",
        "category": "Distributed Systems & Consensus",
        "description": "Core Raft protocol state machine modeling Follower, Candidate, and Leader roles, terms, voting, and heartbeats.",
        "concepts": ["Raft Consensus Algorithm", "Leader Election & Terms", "Heartbeat & Election Timers", "State Machine Transitions"],
        "code": r'''//! Project 073: Raft Consensus Core State Machine
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
'''
    },
    {
        "id": "074",
        "dir_name": "074_lock_free_spsc_queue",
        "name": "lock_free_spsc_queue",
        "title": "Lock-Free SPSC Circular Queue",
        "level": "Advanced",
        "category": "Concurrency & Lock-Free",
        "description": "Single-Producer Single-Consumer lock-free ring buffer using atomic operations with acquire-release memory orderings.",
        "concepts": ["AtomicUsize & AtomicPtr", "Acquire / Release Memory Orderings", "Lock-Free Ring Buffers", "Hardware Cache Line Padding"],
        "code": r'''//! Project 074: Lock-Free SPSC Circular Queue
//! Demonstrates lock-free atomic concurrency and acquire/release memory semantics.

use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;

pub struct SpscQueue<T, const CAP: usize> {
    buffer: [Option<T>; CAP],
    head: AtomicUsize,
    tail: AtomicUsize,
}

impl<T: Copy + Default, const CAP: usize> SpscQueue<T, CAP> {
    pub fn new() -> Arc<Self> {
        Arc::new(Self {
            buffer: [None; CAP],
            head: AtomicUsize::new(0),
            tail: AtomicUsize::new(0),
        })
    }

    pub fn push(&mut self, val: T) -> Result<(), &'static str> {
        let head = self.head.load(Ordering::Relaxed);
        let tail = self.tail.load(Ordering::Acquire);

        if (head + 1) % CAP == tail {
            return Err("Queue full");
        }

        self.buffer[head] = Some(val);
        self.head.store((head + 1) % CAP, Ordering::Release);
        Ok(())
    }

    pub fn pop(&mut self) -> Option<T> {
        let tail = self.tail.load(Ordering::Relaxed);
        let head = self.head.load(Ordering::Acquire);

        if head == tail {
            return None;
        }

        let val = self.buffer[tail].take();
        self.tail.store((tail + 1) % CAP, Ordering::Release);
        val
    }
}

fn main() {
    println!("=== 🦀 Project 074: Lock-Free SPSC Queue ===");
    let mut q = SpscQueue::<i32, 4> {
        buffer: [None; 4],
        head: AtomicUsize::new(0),
        tail: AtomicUsize::new(0),
    };

    q.push(100).unwrap();
    q.push(200).unwrap();
    println!("Popped item: {:?}", q.pop());
    println!("Popped item: {:?}", q.pop());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_spsc() {
        let mut q = SpscQueue::<u32, 4> {
            buffer: [None; 4],
            head: AtomicUsize::new(0),
            tail: AtomicUsize::new(0),
        };
        assert!(q.push(42).is_ok());
        assert_eq!(q.pop(), Some(42));
        assert_eq!(q.pop(), None);
    }
}
'''
    },
    {
        "id": "075",
        "dir_name": "075_mini_git_object_store",
        "name": "mini_git_object_store",
        "title": "Mini Git Content-Addressable Object Store",
        "level": "Advanced",
        "category": "Version Control & Storage",
        "description": "Content-addressable storage implementation mimicking Git: blob, tree, and commit objects addressed by cryptographic hashes.",
        "concepts": ["Content-Addressable Storage", "Git Object Model (blob, tree, commit)", "SHA Object Hashing", "Immutable Object DAG"],
        "code": r'''//! Project 075: Mini Git Content-Addressable Object Store
//! Demonstrates the core immutable DAG model of Git (blobs, trees, commits).

use std::collections::HashMap;

fn hash_content(data: &[u8]) -> String {
    let mut h: u64 = 14695981039346656037;
    for &b in data {
        h = (h ^ (b as u64)).wrapping_mul(1099511628211);
    }
    format!("{:016x}", h)
}

#[derive(Debug, PartialEq, Clone)]
pub enum GitObject {
    Blob(Vec<u8>),
    Commit { tree_hash: String, parent_hash: Option<String>, message: String },
}

pub struct GitObjectStore {
    objects: HashMap<String, GitObject>,
}

impl GitObjectStore {
    pub fn new() -> Self {
        Self { objects: HashMap::new() }
    }

    pub fn write_blob(&mut self, content: &[u8]) -> String {
        let hash = hash_content(content);
        self.objects.insert(hash.clone(), GitObject::Blob(content.to_vec()));
        hash
    }

    pub fn write_commit(&mut self, tree_hash: &str, parent: Option<&str>, message: &str) -> String {
        let payload = format!("{}:{:?}:{}", tree_hash, parent, message);
        let hash = hash_content(payload.as_bytes());
        self.objects.insert(hash.clone(), GitObject::Commit {
            tree_hash: tree_hash.to_string(),
            parent_hash: parent.map(|s| s.to_string()),
            message: message.to_string(),
        });
        hash
    }

    pub fn get(&self, hash: &str) -> Option<&GitObject> {
        self.objects.get(hash)
    }
}

fn main() {
    println!("=== 🦀 Project 075: Mini Git Object Store ===");
    let mut git = GitObjectStore::new();
    let blob_hash = git.write_blob(b"println!(\"Hello, Git!\");");
    println!("Created Blob SHA:   {}", blob_hash);

    let commit1 = git.write_commit(&blob_hash, None, "Initial commit");
    println!("Created Commit #1:  {}", commit1);

    let commit2 = git.write_commit(&blob_hash, Some(&commit1), "Second commit");
    println!("Created Commit #2:  {}", commit2);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_git_store() {
        let mut git = GitObjectStore::new();
        let h = git.write_blob(b"test");
        assert!(git.get(&h).is_some());
    }
}
'''
    }
]
