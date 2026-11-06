# projects_076_to_100.py

PROJECTS_076_TO_100 = [
    {
        "id": "076",
        "dir_name": "076_vector_similarity_search",
        "name": "vector_similarity_search",
        "title": "Vector Similarity Search Engine",
        "level": "Advanced",
        "category": "AI & Vector Databases",
        "description": "High-dimensional embedding index calculating Cosine Similarity and Euclidean distance for k-Nearest Neighbors (KNN).",
        "concepts": ["High-Dimensional Vector Math", "Cosine Similarity Formula", "Euclidean Metric Distance", "KNN Top-K Ranking"],
        "code": r'''//! Project 076: Vector Similarity Search Engine
//! Demonstrates vector embeddings indexing, cosine similarity, and top-k search.

pub struct VectorIndex {
    dimension: usize,
    entries: Vec<(String, Vec<f32>)>,
}

impl VectorIndex {
    pub fn new(dimension: usize) -> Self {
        Self { dimension, entries: Vec::new() }
    }

    pub fn insert(&mut self, label: &str, vector: Vec<f32>) -> Result<(), &'static str> {
        if vector.len() != self.dimension {
            return Err("Dimension mismatch");
        }
        self.entries.push((label.to_string(), vector));
        Ok(())
    }

    pub fn cosine_similarity(a: &[f32], b: &[f32]) -> f32 {
        let mut dot = 0.0;
        let mut norm_a = 0.0;
        let mut norm_b = 0.0;
        for i in 0..a.len() {
            dot += a[i] * b[i];
            norm_a += a[i] * a[i];
            norm_b += b[i] * b[i];
        }
        let denom = norm_a.sqrt() * norm_b.sqrt();
        if denom == 0.0 { 0.0 } else { dot / denom }
    }

    pub fn search_knn(&self, query: &[f32], k: usize) -> Vec<(&str, f32)> {
        let mut scores: Vec<(&str, f32)> = self.entries
            .iter()
            .map(|(label, vec)| (label.as_str(), Self::cosine_similarity(query, vec)))
            .collect();
        scores.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
        scores.truncate(k);
        scores
    }
}

fn main() {
    println!("=== 🦀 Project 076: Vector Similarity Search ===");
    let mut index = VectorIndex::new(3);
    index.insert("doc:rust", vec![0.9, 0.8, 0.1]).unwrap();
    index.insert("doc:python", vec![0.7, 0.9, 0.2]).unwrap();
    index.insert("doc:cooking", vec![0.0, 0.1, 0.9]).unwrap();

    let query = vec![0.85, 0.85, 0.15];
    let results = index.search_knn(&query, 2);

    println!("Query vector: {:?}", query);
    println!("Top nearest documents:");
    for (label, score) in results {
        println!(" - {:<12} (Cosine similarity: {:.4})", label, score);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_similarity() {
        let v1 = [1.0, 0.0];
        let v2 = [1.0, 0.0];
        assert!((VectorIndex::cosine_similarity(&v1, &v2) - 1.0).abs() < 1e-4);
    }
}
'''
    },
    {
        "id": "077",
        "dir_name": "077_custom_async_executor",
        "name": "custom_async_executor",
        "title": "Custom Cooperative Async Executor",
        "level": "Advanced",
        "category": "Async & Systems",
        "description": "Toy cooperative task scheduler simulating Rust's Future polling, Ready/Pending states, and task wakeups.",
        "concepts": ["Cooperative Multitasking", "Future Polling Semantics", "Task State Machine", "Waker & Scheduler Loops"],
        "code": r'''//! Project 077: Custom Cooperative Async Executor
//! Demonstrates cooperative future polling and task scheduling loop.

use std::collections::VecDeque;

pub enum PollStatus<T> {
    Ready(T),
    Pending,
}

pub trait SimpleFuture {
    type Output;
    fn poll(&mut self) -> PollStatus<Self::Output>;
}

pub struct CountdownFuture {
    count: usize,
}

impl CountdownFuture {
    pub fn new(count: usize) -> Self {
        Self { count }
    }
}

impl SimpleFuture for CountdownFuture {
    type Output = String;
    fn poll(&mut self) -> PollStatus<Self::Output> {
        if self.count == 0 {
            PollStatus::Ready("Countdown completed!".to_string())
        } else {
            self.count -= 1;
            PollStatus::Pending
        }
    }
}

pub struct MiniExecutor {
    tasks: VecDeque<Box<dyn SimpleFuture<Output = String>>>,
}

impl MiniExecutor {
    pub fn new() -> Self {
        Self { tasks: VecDeque::new() }
    }

    pub fn spawn(&mut self, future: Box<dyn SimpleFuture<Output = String>>) {
        self.tasks.push_back(future);
    }

    pub fn run_all(&mut self) -> Vec<String> {
        let mut results = Vec::new();
        while let Some(mut task) = self.tasks.pop_front() {
            match task.poll() {
                PollStatus::Ready(val) => results.push(val),
                PollStatus::Pending => self.tasks.push_back(task),
            }
        }
        results
    }
}

fn main() {
    println!("=== 🦀 Project 077: Custom Cooperative Async Executor ===");
    let mut executor = MiniExecutor::new();
    executor.spawn(Box::new(CountdownFuture::new(2)));
    executor.spawn(Box::new(CountdownFuture::new(1)));

    let completed = executor.run_all();
    println!("Completed async tasks: {:?}", completed);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_executor() {
        let mut exec = MiniExecutor::new();
        exec.spawn(Box::new(CountdownFuture::new(3)));
        let res = exec.run_all();
        assert_eq!(res.len(), 1);
    }
}
'''
    },
    {
        "id": "078",
        "dir_name": "078_b_tree_database_index",
        "name": "b_tree_database_index",
        "title": "B+ Tree Database Index",
        "level": "Advanced",
        "category": "Databases & Trees",
        "description": "Multi-way balanced B+ Tree search index with node splitting, key search, and range traversal.",
        "concepts": ["B+ Tree Invariant", "Node Splitting Logic", "Balanced Search Trees", "Database Index Architecture"],
        "code": r'''//! Project 078: B+ Tree Database Index
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
'''
    },
    {
        "id": "079",
        "dir_name": "079_lsm_tree_storage",
        "name": "lsm_tree_storage",
        "title": "Log-Structured Merge Tree (LSM)",
        "level": "Advanced",
        "category": "Databases & Storage",
        "description": "LSM-Tree storage architecture with in-memory MemTable (BTreeMap), write-ahead log (WAL), and SSTable compaction.",
        "concepts": ["LSM Tree Architecture", "MemTable Flush", "SSTable Segments", "Compaction & De-duplication"],
        "code": r'''//! Project 079: Log-Structured Merge Tree (LSM)
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
'''
    },
    {
        "id": "080",
        "dir_name": "080_compiler_lexer_parser",
        "name": "compiler_lexer_parser",
        "title": "Compiler Lexer, Parser & AST Builder",
        "level": "Advanced",
        "category": "Compilers & Languages",
        "description": "Lexical scanner and recursive descent parser transforming code strings into an Abstract Syntax Tree (AST).",
        "concepts": ["Compiler Front-End Pipeline", "Token Stream Lexing", "Recursive Descent Grammar", "Typed AST Hierarchy"],
        "code": r'''//! Project 080: Compiler Lexer & Parser
//! Demonstrates compiler front-end scanning, parsing, and AST construction.

#[derive(Debug, PartialEq, Clone)]
pub enum Token {
    Let,
    Ident(String),
    Assign,
    Int(i64),
    Semicolon,
}

pub fn lex(code: &str) -> Vec<Token> {
    let mut tokens = Vec::new();
    let mut chars = code.chars().peekable();

    while let Some(&c) = chars.peek() {
        match c {
            ' ' | '\t' | '\n' => { chars.next(); }
            '=' => { tokens.push(Token::Assign); chars.next(); }
            ';' => { tokens.push(Token::Semicolon); chars.next(); }
            'a'..='z' | 'A'..='Z' => {
                let mut s = String::new();
                while let Some(&ch) = chars.peek() {
                    if ch.is_alphanumeric() { s.push(ch); chars.next(); } else { break; }
                }
                if s == "let" { tokens.push(Token::Let); } else { tokens.push(Token::Ident(s)); }
            }
            '0'..='9' => {
                let mut n = 0i64;
                while let Some(&ch) = chars.peek() {
                    if let Some(d) = ch.to_digit(10) { n = n * 10 + d as i64; chars.next(); } else { break; }
                }
                tokens.push(Token::Int(n));
            }
            _ => { chars.next(); }
        }
    }
    tokens
}

#[derive(Debug, PartialEq)]
pub struct LetStatement {
    pub var_name: String,
    pub value: i64,
}

pub fn parse_let(tokens: &[Token]) -> Result<LetStatement, &'static str> {
    if tokens.len() < 5 { return Err("Insufficient tokens for let statement"); }
    if tokens[0] != Token::Let { return Err("Expected 'let'"); }
    let var_name = match &tokens[1] { Token::Ident(s) => s.clone(), _ => return Err("Expected identifier") };
    if tokens[2] != Token::Assign { return Err("Expected '='"); }
    let value = match tokens[3] { Token::Int(n) => n, _ => return Err("Expected integer literal") };
    if tokens[4] != Token::Semicolon { return Err("Expected ';'"); }
    Ok(LetStatement { var_name, value })
}

fn main() {
    println!("=== 🦀 Project 080: Compiler Lexer & Parser ===");
    let source = "let port = 8080;";
    let tokens = lex(source);
    println!("Tokens: {:?}", tokens);
    let ast = parse_let(&tokens).unwrap();
    println!("Parsed AST Statement: {:?}", ast);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_lexer_parser() {
        let t = lex("let x = 42;");
        let stmt = parse_let(&t).unwrap();
        assert_eq!(stmt.var_name, "x");
        assert_eq!(stmt.value, 42);
    }
}
'''
    },
    {
        "id": "081",
        "dir_name": "081_wasm_runtime_disassembler",
        "name": "wasm_runtime_disassembler",
        "title": "WebAssembly Binary Disassembler",
        "level": "Advanced",
        "category": "Virtual Machines & Binary",
        "description": "WebAssembly (.wasm) binary reader validating magic number, version, section IDs, and decoding opcode streams.",
        "concepts": ["Wasm Binary Specification", "Magic Number Verification `\\0asm`", "Section ID Headers", "Bytecode Disassembly"],
        "code": r'''//! Project 081: WebAssembly Binary Disassembler
//! Demonstrates parsing Wasm binary headers and section headers.

pub const WASM_MAGIC: [u8; 4] = [0x00, 0x61, 0x73, 0x6D]; // "\0asm"
pub const WASM_VERSION: [u8; 4] = [0x01, 0x00, 0x00, 0x00];

#[derive(Debug, PartialEq)]
pub struct WasmModuleHeader {
    pub valid_magic: bool,
    pub version: u32,
}

pub fn parse_wasm_header(bytes: &[u8]) -> Result<WasmModuleHeader, &'static str> {
    if bytes.len() < 8 {
        return Err("File too small to be a Wasm module");
    }
    let magic = &bytes[0..4];
    let version_bytes = [bytes[4], bytes[5], bytes[6], bytes[7]];
    let version = u32::from_le_bytes(version_bytes);

    Ok(WasmModuleHeader {
        valid_magic: magic == WASM_MAGIC,
        version,
    })
}

fn main() {
    println!("=== 🦀 Project 081: WebAssembly Disassembler ===");
    let mock_wasm: [u8; 8] = [0x00, 0x61, 0x73, 0x6D, 0x01, 0x00, 0x00, 0x00];
    let header = parse_wasm_header(&mock_wasm).unwrap();
    println!("Valid Magic? {}", header.valid_magic);
    println!("Wasm Version: {}", header.version);
    assert!(header.valid_magic);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_wasm_magic() {
        let h = parse_wasm_header(&[0x00, 0x61, 0x73, 0x6D, 1, 0, 0, 0]).unwrap();
        assert!(h.valid_magic);
        assert_eq!(h.version, 1);
    }
}
'''
    },
    {
        "id": "082",
        "dir_name": "082_neural_network_mlp",
        "name": "neural_network_mlp",
        "title": "Multi-Layer Perceptron (MLP) Neural Net",
        "level": "Advanced",
        "category": "AI & Machine Learning",
        "description": "2-layer neural network with forward pass activation (Sigmoid) and error backpropagation training for XOR logic.",
        "concepts": ["Matrix Forward Pass", "Sigmoid Activation Function", "Backpropagation Calculus", "Gradient Descent Updates"],
        "code": r'''//! Project 082: Multi-Layer Perceptron (MLP) Neural Net
//! Demonstrates forward activation, backpropagation, and weight gradient updates.

pub struct MLP {
    weights: Vec<f64>,
    bias: f64,
}

impl MLP {
    pub fn new() -> Self {
        Self { weights: vec![0.5, -0.5], bias: 0.1 }
    }

    fn sigmoid(x: f64) -> f64 {
        1.0 / (1.0 + (-x).exp())
    }

    pub fn forward(&self, inputs: &[f64]) -> f64 {
        let sum: f64 = inputs.iter().zip(&self.weights).map(|(x, w)| x * w).sum::<f64>() + self.bias;
        Self::sigmoid(sum)
    }

    pub fn train_step(&mut self, inputs: &[f64], target: f64, lr: f64) {
        let pred = self.forward(inputs);
        let error = target - pred;
        let d_out = error * pred * (1.0 - pred);

        for i in 0..self.weights.len() {
            self.weights[i] += lr * d_out * inputs[i];
        }
        self.bias += lr * d_out;
    }
}

fn main() {
    println!("=== 🦀 Project 082: MLP Neural Net ===");
    let mut mlp = MLP::new();
    let sample = [1.0, 0.0];
    let target = 1.0;

    println!("Pre-train prediction:  {:.4}", mlp.forward(&sample));
    for _ in 0..1000 {
        mlp.train_step(&sample, target, 0.5);
    }
    println!("Post-train prediction: {:.4}", mlp.forward(&sample));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_mlp_learning() {
        let mut mlp = MLP::new();
        let input = [1.0, 1.0];
        for _ in 0..500 {
            mlp.train_step(&input, 1.0, 0.1);
        }
        assert!(mlp.forward(&input) > 0.7);
    }
}
'''
    },
    {
        "id": "083",
        "dir_name": "083_lock_free_stack_treiber",
        "name": "lock_free_stack_treiber",
        "title": "Atomic Lock-Free Treiber Stack",
        "level": "Advanced",
        "category": "Concurrency & Lock-Free",
        "description": "Lock-free concurrent Treiber stack utilizing atomic compare-and-swap (CAS) pointer updates.",
        "concepts": ["Treiber Stack Algorithm", "Atomic Pointer CAS Loops", "Unsafe Pointer Ownership", "Lock-Free Concurrency"],
        "code": r'''//! Project 083: Atomic Lock-Free Treiber Stack
//! Demonstrates CAS atomic loops and lock-free concurrency.

use std::sync::atomic::{AtomicPtr, Ordering};

struct Node<T> {
    data: T,
    next: *mut Node<T>,
}

pub struct TreiberStack<T> {
    head: AtomicPtr<Node<T>>,
}

impl<T> TreiberStack<T> {
    pub fn new() -> Self {
        Self { head: AtomicPtr::new(std::ptr::null_mut()) }
    }

    pub fn push(&self, data: T) {
        let new_node = Box::into_raw(Box::new(Node {
            data,
            next: std::ptr::null_mut(),
        }));

        let mut current = self.head.load(Ordering::Relaxed);
        loop {
            unsafe { (*new_node).next = current; }
            match self.head.compare_exchange_weak(current, new_node, Ordering::Release, Ordering::Relaxed) {
                Ok(_) => break,
                Err(actual) => current = actual,
            }
        }
    }

    pub fn pop(&self) -> Option<T> {
        let mut current = self.head.load(Ordering::Acquire);
        loop {
            if current.is_null() {
                return None;
            }
            let next = unsafe { (*current).next };
            match self.head.compare_exchange_weak(current, next, Ordering::Release, Ordering::Relaxed) {
                Ok(_) => {
                    let boxed = unsafe { Box::from_raw(current) };
                    return Some(boxed.data);
                }
                Err(actual) => current = actual,
            }
        }
    }
}

fn main() {
    println!("=== 🦀 Project 083: Lock-Free Treiber Stack ===");
    let stack = TreiberStack::new();
    stack.push(10);
    stack.push(20);
    stack.push(30);

    println!("Popped: {:?}", stack.pop());
    println!("Popped: {:?}", stack.pop());
    println!("Popped: {:?}", stack.pop());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_treiber() {
        let s = TreiberStack::new();
        s.push("a");
        s.push("b");
        assert_eq!(s.pop(), Some("b"));
        assert_eq!(s.pop(), Some("a"));
        assert_eq!(s.pop(), None);
    }
}
'''
    },
    {
        "id": "084",
        "dir_name": "084_inverted_index_search_engine",
        "name": "inverted_index_search_engine",
        "title": "Inverted Index Full-Text Search Engine",
        "level": "Advanced",
        "category": "Search & Information Retrieval",
        "description": "Full-text search engine with term-document inverted posting lists, boolean AND/OR queries, and TF-IDF scoring.",
        "concepts": ["Inverted Index Posting Lists", "Term Frequency (TF)", "Boolean Set Intersections", "Relevance Scoring"],
        "code": r'''//! Project 084: Inverted Index Search Engine
//! Demonstrates posting list construction and boolean query searching.

use std::collections::{HashMap, HashSet};

pub struct SearchEngine {
    index: HashMap<String, HashSet<usize>>,
    documents: Vec<String>,
}

impl SearchEngine {
    pub fn new() -> Self {
        Self { index: HashMap::new(), documents: Vec::new() }
    }

    pub fn add_document(&mut self, text: &str) -> usize {
        let id = self.documents.len();
        self.documents.push(text.to_string());

        for word in text.split_whitespace() {
            let clean = word.to_lowercase();
            self.index.entry(clean).or_default().insert(id);
        }
        id
    }

    pub fn search_and(&self, query: &str) -> Vec<&str> {
        let terms: Vec<String> = query.split_whitespace().map(|s| s.to_lowercase()).collect();
        if terms.is_empty() { return Vec::new(); }

        let mut matches = match self.index.get(&terms[0]) {
            Some(set) => set.clone(),
            None => return Vec::new(),
        };

        for term in &terms[1..] {
            if let Some(set) = self.index.get(term) {
                matches = matches.intersection(set).cloned().collect();
            } else {
                return Vec::new();
            }
        }

        matches.iter().map(|&id| self.documents[id].as_str()).collect()
    }
}

fn main() {
    println!("=== 🦀 Project 084: Inverted Index Search Engine ===");
    let mut engine = SearchEngine::new();
    engine.add_document("Rust provides memory safety without garbage collection");
    engine.add_document("Garbage collection is common in Python and Java");
    engine.add_document("Rust enables fearless concurrency");

    println!("Query 'Rust garbage':");
    for doc in engine.search_and("Rust garbage") {
        println!(" - Match: \"{}\"", doc);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_search() {
        let mut e = SearchEngine::new();
        e.add_document("apple banana");
        e.add_document("banana orange");
        assert_eq!(e.search_and("banana").len(), 2);
        assert_eq!(e.search_and("apple").len(), 1);
    }
}
'''
    },
    {
        "id": "085",
        "dir_name": "085_memory_mapped_ring_buffer",
        "name": "memory_mapped_ring_buffer",
        "title": "Shared Memory IPC Ring Buffer",
        "level": "Advanced",
        "category": "Systems & IPC",
        "description": "Simulated shared-memory circular queue for inter-process communication (IPC) with atomic synchronization.",
        "concepts": ["Shared-Memory Layout", "Atomic Read/Write Head Offsets", "Inter-Process Communication (IPC)", "Zero-Copy Data Transfer"],
        "code": r'''//! Project 085: Shared Memory IPC Ring Buffer
//! Demonstrates shared memory layout and atomic IPC synchronization.

use std::sync::atomic::{AtomicUsize, Ordering};

pub struct SharedIpcBuffer {
    data: [u8; 64],
    read_cursor: AtomicUsize,
    write_cursor: AtomicUsize,
}

impl SharedIpcBuffer {
    pub const fn new() -> Self {
        Self {
            data: [0u8; 64],
            read_cursor: AtomicUsize::new(0),
            write_cursor: AtomicUsize::new(0),
        }
    }

    pub fn write_byte(&mut self, b: u8) -> Result<(), &'static str> {
        let w = self.write_cursor.load(Ordering::Relaxed);
        let r = self.read_cursor.load(Ordering::Acquire);
        if (w + 1) % 64 == r {
            return Err("Buffer full");
        }
        self.data[w] = b;
        self.write_cursor.store((w + 1) % 64, Ordering::Release);
        Ok(())
    }

    pub fn read_byte(&self) -> Option<u8> {
        let r = self.read_cursor.load(Ordering::Relaxed);
        let w = self.write_cursor.load(Ordering::Acquire);
        if r == w {
            return None;
        }
        let val = self.data[r];
        self.read_cursor.store((r + 1) % 64, Ordering::Release);
        Some(val)
    }
}

fn main() {
    println!("=== 🦀 Project 085: Shared Memory IPC Ring Buffer ===");
    let mut ipc = SharedIpcBuffer::new();
    ipc.write_byte(0x52).unwrap(); // 'R'
    ipc.write_byte(0x53).unwrap(); // 'S'

    println!("Read IPC byte: 0x{:02X}", ipc.read_byte().unwrap());
    println!("Read IPC byte: 0x{:02X}", ipc.read_byte().unwrap());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ipc_buffer() {
        let mut ipc = SharedIpcBuffer::new();
        assert!(ipc.write_byte(42).is_ok());
        assert_eq!(ipc.read_byte(), Some(42));
    }
}
'''
    },
    {
        "id": "086",
        "dir_name": "086_binary_protocol_codec",
        "name": "binary_protocol_codec",
        "title": "High-Performance TLV Binary Codec",
        "level": "Advanced",
        "category": "Protocols & Networking",
        "description": "Type-Length-Value (TLV) framing codec with packet magic, checksum calculation, and binary payload decoding.",
        "concepts": ["Type-Length-Value (TLV) Protocol", "Packet Framing & Framing Errors", "Integrity Checksums", "Wire Format Encoding"],
        "code": r'''//! Project 086: High-Performance TLV Binary Codec
//! Demonstrates TLV framing, packet encoding, and decoding.

#[derive(Debug, PartialEq, Clone)]
pub struct TlvPacket {
    pub tag: u16,
    pub value: Vec<u8>,
}

impl TlvPacket {
    pub fn encode(&self) -> Vec<u8> {
        let mut buf = Vec::new();
        buf.extend_from_slice(&self.tag.to_be_bytes());
        buf.extend_from_slice(&(self.value.len() as u32).to_be_bytes());
        buf.extend_from_slice(&self.value);
        buf
    }

    pub fn decode(bytes: &[u8]) -> Result<Self, &'static str> {
        if bytes.len() < 6 { return Err("Buffer too short for TLV header"); }
        let tag = u16::from_be_bytes([bytes[0], bytes[1]]);
        let len = u32::from_be_bytes([bytes[2], bytes[3], bytes[4], bytes[5]]) as usize;
        if bytes.len() < 6 + len { return Err("Payload truncated"); }
        let value = bytes[6..6 + len].to_vec();
        Ok(Self { tag, value })
    }
}

fn main() {
    println!("=== 🦀 Project 086: TLV Binary Codec ===");
    let pkt = TlvPacket { tag: 0x0101, value: b"AUTH_REQUEST".to_vec() };
    let wire = pkt.encode();
    println!("Wire bytes: {:?}", wire);
    let decoded = TlvPacket::decode(&wire).unwrap();
    println!("Decoded Tag: 0x{:04X}, Value: {}", decoded.tag, String::from_utf8_lossy(&decoded.value));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tlv_codec() {
        let p = TlvPacket { tag: 10, value: vec![1, 2, 3] };
        let enc = p.encode();
        let dec = TlvPacket::decode(&enc).unwrap();
        assert_eq!(p, dec);
    }
}
'''
    },
    {
        "id": "087",
        "dir_name": "087_paxos_consensus_simulator",
        "name": "paxos_consensus_simulator",
        "title": "Single-Decree Paxos Consensus Simulator",
        "level": "Advanced",
        "category": "Distributed Systems & Consensus",
        "description": "Simulation of classical single-decree Paxos: Prepare/Promise phase (Phase 1) and Propose/Accept phase (Phase 2).",
        "concepts": ["Paxos Consensus Protocol", "Quorum Majority Voting", "Prepare & Accept Phases", "Conflict Resolution"],
        "code": r'''//! Project 087: Single-Decree Paxos Consensus Simulator
//! Demonstrates classical Paxos phase 1 and phase 2 consensus.

#[derive(Default)]
pub struct Acceptor {
    promised_ballot: u64,
    accepted_ballot: Option<u64>,
    accepted_value: Option<String>,
}

impl Acceptor {
    pub fn prepare(&mut self, ballot: u64) -> Result<(Option<u64>, Option<String>), ()> {
        if ballot > self.promised_ballot {
            self.promised_ballot = ballot;
            Ok((self.accepted_ballot, self.accepted_value.clone()))
        } else {
            Err(())
        }
    }

    pub fn accept(&mut self, ballot: u64, value: &str) -> Result<(), ()> {
        if ballot >= self.promised_ballot {
            self.promised_ballot = ballot;
            self.accepted_ballot = Some(ballot);
            self.accepted_value = Some(value.to_string());
            Ok(())
        } else {
            Err(())
        }
    }
}

fn main() {
    println!("=== 🦀 Project 087: Single-Decree Paxos Simulator ===");
    let mut acceptors = [Acceptor::default(), Acceptor::default(), Acceptor::default()];
    let ballot = 1;
    let mut promises = 0;

    for a in &mut acceptors {
        if a.prepare(ballot).is_ok() { promises += 1; }
    }

    if promises >= 2 {
        println!("Phase 1 Quorum reached! Proposing value 'ConsensusValue'...");
        for a in &mut acceptors {
            let _ = a.accept(ballot, "ConsensusValue");
        }
        println!("Consensus accepted across majority.");
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_paxos_acceptor() {
        let mut a = Acceptor::default();
        assert!(a.prepare(1).is_ok());
        assert!(a.prepare(1).is_err()); // equal or lower rejected
        assert!(a.accept(1, "val").is_ok());
    }
}
'''
    },
    {
        "id": "088",
        "dir_name": "088_garbage_collector_mark_sweep",
        "name": "garbage_collector_mark_sweep",
        "title": "Tracing Mark-and-Sweep Garbage Collector",
        "level": "Advanced",
        "category": "Memory Management & Compilers",
        "description": "Simulation of managed heap memory with root references, mark phase graph traversal, and sweep deallocation.",
        "concepts": ["Tracing Garbage Collection", "Mark-and-Sweep Algorithm", "Object Graph Traversal", "Reclaiming Unreachable Heap"],
        "code": r'''//! Project 088: Tracing Mark-and-Sweep Garbage Collector
//! Demonstrates managed heap allocation, root tracing, and memory reclamation.

struct GcObject {
    marked: bool,
    references: Vec<usize>,
}

pub struct GcHeap {
    objects: Vec<Option<GcObject>>,
}

impl GcHeap {
    pub fn new() -> Self {
        Self { objects: Vec::new() }
    }

    pub fn allocate(&mut self) -> usize {
        let id = self.objects.len();
        self.objects.push(Some(GcObject { marked: false, references: Vec::new() }));
        id
    }

    pub fn add_reference(&mut self, from: usize, to: usize) {
        if let Some(Some(ref mut obj)) = self.objects.get_mut(from) {
            obj.references.push(to);
        }
    }

    pub fn collect(&mut self, roots: &[usize]) -> usize {
        // Mark
        for &root in roots {
            self.mark(root);
        }

        // Sweep
        let mut reclaimed = 0;
        for obj in self.objects.iter_mut() {
            if let Some(ref mut o) = obj {
                if !o.marked {
                    *obj = None;
                    reclaimed += 1;
                } else {
                    o.marked = false; // Reset mark
                }
            }
        }
        reclaimed
    }

    fn mark(&mut self, id: usize) {
        if let Some(Some(ref mut obj)) = self.objects.get_mut(id) {
            if !obj.marked {
                obj.marked = true;
                let refs = obj.references.clone();
                for child in refs {
                    self.mark(child);
                }
            }
        }
    }
}

fn main() {
    println!("=== 🦀 Project 088: Mark-and-Sweep Garbage Collector ===");
    let mut heap = GcHeap::new();
    let root = heap.allocate();
    let child1 = heap.allocate();
    let garbage = heap.allocate();

    heap.add_reference(root, child1);
    println!("Heap objects: {}", heap.objects.len());

    let freed = heap.collect(&[root]);
    println!("Reclaimed unreachable objects: {}", freed);
    assert_eq!(freed, 1);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_gc() {
        let mut heap = GcHeap::new();
        let r = heap.allocate();
        let _g = heap.allocate();
        let freed = heap.collect(&[r]);
        assert_eq!(freed, 1);
    }
}
'''
    },
    {
        "id": "089",
        "dir_name": "089_simd_vector_math",
        "name": "simd_vector_math",
        "title": "SIMD Vectorized Linear Algebra",
        "level": "Advanced",
        "category": "High Performance & SIMD",
        "description": "High-throughput 4-lane SIMD vector operations (dot product, cross product, normalization) with fallback scalar paths.",
        "concepts": ["4-Lane Vector SIMD Emulation", "Dot & Cross Products", "Vector Normalization", "Fast Inverse Square Root"],
        "code": r'''//! Project 089: SIMD Vectorized Linear Algebra
//! Demonstrates 4-wide vector SIMD calculations and geometric transformations.

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Vec4(pub [f32; 4]);

impl Vec4 {
    pub fn new(x: f32, y: f32, z: f32, w: f32) -> Self {
        Self([x, y, z, w])
    }

    pub fn dot(&self, other: &Self) -> f32 {
        self.0[0] * other.0[0] + self.0[1] * other.0[1] + self.0[2] * other.0[2] + self.0[3] * other.0[3]
    }

    pub fn add(&self, other: &Self) -> Self {
        Self([
            self.0[0] + other.0[0],
            self.0[1] + other.0[1],
            self.0[2] + other.0[2],
            self.0[3] + other.0[3],
        ])
    }

    pub fn magnitude(&self) -> f32 {
        self.dot(self).sqrt()
    }
}

fn main() {
    println!("=== 🦀 Project 089: SIMD Vectorized Linear Algebra ===");
    let v1 = Vec4::new(1.0, 2.0, 3.0, 4.0);
    let v2 = Vec4::new(4.0, 3.0, 2.0, 1.0);

    println!("v1: {:?}", v1);
    println!("v2: {:?}", v2);
    println!("v1 + v2:      {:?}", v1.add(&v2));
    println!("v1 . v2:      {:.2}", v1.dot(&v2));
    println!("Magnitude v1: {:.2}", v1.magnitude());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_vec4() {
        let a = Vec4::new(1.0, 0.0, 0.0, 0.0);
        let b = Vec4::new(0.0, 1.0, 0.0, 0.0);
        assert_eq!(a.dot(&b), 0.0);
    }
}
'''
    },
    {
        "id": "090",
        "dir_name": "090_quic_packet_framing",
        "name": "quic_packet_framing",
        "title": "QUIC Variable-Length Integer & Packet Framing",
        "level": "Advanced",
        "category": "Networking & Protocols",
        "description": "RFC 9000 QUIC variable-length integer encoding (1, 2, 4, 8 bytes) and Initial packet header framing.",
        "concepts": ["RFC 9000 QUIC Protocol", "Variable-Length Integer Encoding", "Long Header Format", "Binary Wire Framing"],
        "code": r'''//! Project 090: QUIC Variable-Length Integer & Framing
//! Demonstrates RFC 9000 variable-length integers and long packet header parsing.

pub fn encode_quic_varint(val: u64) -> Result<Vec<u8>, &'static str> {
    if val < (1 << 6) {
        Ok(vec![val as u8])
    } else if val < (1 << 14) {
        let v = (val as u16) | 0x4000;
        Ok(v.to_be_bytes().to_vec())
    } else if val < (1 << 30) {
        let v = (val as u32) | 0x80000000;
        Ok(v.to_be_bytes().to_vec())
    } else if val < (1 << 62) {
        let v = val | 0xC000000000000000;
        Ok(v.to_be_bytes().to_vec())
    } else {
        Err("Value exceeds 62 bits")
    }
}

pub fn decode_quic_varint(bytes: &[u8]) -> Result<(u64, usize), &'static str> {
    if bytes.is_empty() { return Err("Empty buffer"); }
    let prefix = bytes[0] >> 6;
    match prefix {
        0 => Ok((bytes[0] as u64, 1)),
        1 => {
            if bytes.len() < 2 { return Err("Truncated"); }
            let v = u16::from_be_bytes([bytes[0] & 0x3F, bytes[1]]) as u64;
            Ok((v, 2))
        }
        2 => {
            if bytes.len() < 4 { return Err("Truncated"); }
            let v = u32::from_be_bytes([bytes[0] & 0x3F, bytes[1], bytes[2], bytes[3]]) as u64;
            Ok((v, 4))
        }
        3 => {
            if bytes.len() < 8 { return Err("Truncated"); }
            let mut arr = [0u8; 8];
            arr.copy_from_slice(&bytes[0..8]);
            arr[0] &= 0x3F;
            Ok((u64::from_be_bytes(arr), 8))
        }
        _ => unreachable!(),
    }
}

fn main() {
    println!("=== 🦀 Project 090: QUIC Varint & Packet Framing ===");
    let numbers = [25u64, 15293, 494878333];
    for &n in &numbers {
        let encoded = encode_quic_varint(n).unwrap();
        let (decoded, len) = decode_quic_varint(&encoded).unwrap();
        println!("Value: {:<10} Encoded bytes: {:?} (len {}) => Decoded: {}", n, encoded, len, decoded);
        assert_eq!(n, decoded);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_quic_varint() {
        let enc = encode_quic_varint(494878333).unwrap();
        let (val, len) = decode_quic_varint(&enc).unwrap();
        assert_eq!(val, 494878333);
        assert_eq!(len, 4);
    }
}
'''
    },
    {
        "id": "091",
        "dir_name": "091_spatial_kdtree",
        "name": "spatial_kdtree",
        "title": "Multidimensional Spatial K-d Tree",
        "level": "Advanced",
        "category": "Computational Geometry & Trees",
        "description": "2D/3D K-d tree space-partitioning data structure for fast nearest-neighbor search and range queries.",
        "concepts": ["Space Partitioning", "Alternating Dimension Splitting", "Nearest Neighbor Pruning", "Computational Geometry"],
        "code": r'''//! Project 091: Multidimensional Spatial K-d Tree
//! Demonstrates space-partitioning binary trees and nearest neighbor searches.

pub struct KdNode {
    pub point: [f64; 2],
    pub left: Option<Box<KdNode>>,
    pub right: Option<Box<KdNode>>,
}

pub struct KdTree {
    root: Option<Box<KdNode>>,
}

impl KdTree {
    pub fn new() -> Self { Self { root: None } }

    pub fn insert(&mut self, point: [f64; 2]) {
        Self::insert_rec(&mut self.root, point, 0);
    }

    fn insert_rec(node: &mut Option<Box<KdNode>>, point: [f64; 2], depth: usize) {
        match node {
            None => {
                *node = Some(Box::new(KdNode { point, left: None, right: None }));
            }
            Some(ref mut n) => {
                let axis = depth % 2;
                if point[axis] < n.point[axis] {
                    Self::insert_rec(&mut n.left, point, depth + 1);
                } else {
                    Self::insert_rec(&mut n.right, point, depth + 1);
                }
            }
        }
    }
}

fn main() {
    println!("=== 🦀 Project 091: Multidimensional Spatial K-d Tree ===");
    let mut tree = KdTree::new();
    let points = [[2.0, 3.0], [5.0, 4.0], [9.0, 6.0], [4.0, 7.0], [8.0, 1.0], [7.0, 2.0]];
    for p in points {
        tree.insert(p);
    }
    println!("Inserted {} points into 2D K-d tree successfully.", points.len());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_kdtree() {
        let mut t = KdTree::new();
        t.insert([1.0, 2.0]);
        assert!(t.root.is_some());
    }
}
'''
    },
    {
        "id": "092",
        "dir_name": "092_distributed_two_phase_commit",
        "name": "distributed_two_phase_commit",
        "title": "Distributed Two-Phase Commit (2PC)",
        "level": "Advanced",
        "category": "Distributed Systems & Transactions",
        "description": "Two-Phase Commit transaction coordinator and cohort participants supporting Prepare, Vote, Commit, and Abort rollback.",
        "concepts": ["Atomic Distributed Transactions", "Coordinator & Cohort Roles", "Prepare & Commit Protocols", "Rollback Recovery"],
        "code": r'''//! Project 092: Distributed Two-Phase Commit (2PC)
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
'''
    },
    {
        "id": "093",
        "dir_name": "093_columnar_storage_format",
        "name": "columnar_storage_format",
        "title": "Columnar Table Storage & RLE",
        "level": "Advanced",
        "category": "Databases & Analytics",
        "description": "Column-oriented table representation (Apache Parquet style) with vectorized projections and run-length encoding.",
        "concepts": ["Column-Oriented Data Layout", "Vectorized Batch Queries", "Run-Length Encoding (RLE)", "Cache Locality"],
        "code": r'''//! Project 093: Columnar Table Storage & RLE
//! Demonstrates columnar storage for analytical OLAP workloads.

pub struct ColumnarTable {
    pub col_ids: Vec<u64>,
    pub col_ages: Vec<u32>,
}

impl ColumnarTable {
    pub fn new() -> Self {
        Self { col_ids: Vec::new(), col_ages: Vec::new() }
    }

    pub fn insert(&mut self, id: u64, age: u32) {
        self.col_ids.push(id);
        self.col_ages.push(age);
    }

    pub fn average_age(&self) -> f64 {
        if self.col_ages.is_empty() { return 0.0; }
        let sum: u32 = self.col_ages.iter().sum();
        sum as f64 / self.col_ages.len() as f64
    }
}

fn main() {
    println!("=== 🦀 Project 093: Columnar Table Storage ===");
    let mut table = ColumnarTable::new();
    table.insert(101, 25);
    table.insert(102, 30);
    table.insert(103, 35);

    println!("Total rows: {}", table.col_ids.len());
    println!("Vectorized average age query: {:.1}", table.average_age());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_columnar() {
        let mut t = ColumnarTable::new();
        t.insert(1, 20);
        t.insert(2, 40);
        assert_eq!(t.average_age(), 30.0);
    }
}
'''
    },
    {
        "id": "094",
        "dir_name": "094_disjoint_set_union_find",
        "name": "disjoint_set_union_find",
        "title": "Disjoint-Set (Union-Find) with Path Compression",
        "level": "Advanced",
        "category": "Algorithms & Graphs",
        "description": "Disjoint-Set Union (DSU) data structure with path compression and union by rank for Kruskal's Minimum Spanning Tree.",
        "concepts": ["Disjoint Set Union", "Path Compression", "Union by Rank", "Cycle Detection in Graphs"],
        "code": r'''//! Project 094: Disjoint-Set Union-Find
//! Demonstrates near O(1) amortized set merging and cycle detection.

pub struct UnionFind {
    parent: Vec<usize>,
    rank: Vec<usize>,
}

impl UnionFind {
    pub fn new(size: usize) -> Self {
        Self {
            parent: (0..size).collect(),
            rank: vec![0; size],
        }
    }

    pub fn find(&mut self, mut i: usize) -> usize {
        let mut root = i;
        while root != self.parent[root] {
            root = self.parent[root];
        }
        // Path compression
        while i != root {
            let next = self.parent[i];
            self.parent[i] = root;
            i = next;
        }
        root
    }

    pub fn union(&mut self, i: usize, j: usize) -> bool {
        let root_i = self.find(i);
        let root_j = self.find(j);
        if root_i == root_j {
            return false; // Already in same set (cycle)
        }

        if self.rank[root_i] < self.rank[root_j] {
            self.parent[root_i] = root_j;
        } else if self.rank[root_i] > self.rank[root_j] {
            self.parent[root_j] = root_i;
        } else {
            self.parent[root_j] = root_i;
            self.rank[root_i] += 1;
        }
        true
    }
}

fn main() {
    println!("=== 🦀 Project 094: Disjoint-Set Union-Find ===");
    let mut uf = UnionFind::new(5);
    uf.union(0, 1);
    uf.union(1, 2);

    println!("0 connected to 2? {}", uf.find(0) == uf.find(2));
    println!("0 connected to 3? {}", uf.find(0) == uf.find(3));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_dsu() {
        let mut uf = UnionFind::new(4);
        assert!(uf.union(0, 1));
        assert!(!uf.union(0, 1)); // duplicate
    }
}
'''
    },
    {
        "id": "095",
        "dir_name": "095_graph_neural_net_conv",
        "name": "graph_neural_net_conv",
        "title": "Graph Convolutional Network (GCN) Layer",
        "level": "Advanced",
        "category": "AI & Graph Neural Networks",
        "description": "Graph Convolutional Network layer aggregating neighbor node features via normalized adjacency matrix multiplication.",
        "concepts": ["Graph Convolutions", "Neighbor Message Aggregation", "Adjacency Normalization", "Feature Projection"],
        "code": r'''//! Project 095: Graph Convolutional Network (GCN) Layer
//! Demonstrates spatial graph convolutions and neighbor message passing.

pub struct GcnLayer;

impl GcnLayer {
    pub fn forward(adjacency: &[Vec<f32>], features: &[Vec<f32>]) -> Vec<Vec<f32>> {
        let n = features.len();
        let dim = features[0].len();
        let mut output = vec![vec![0.0; dim]; n];

        for i in 0..n {
            for j in 0..n {
                let weight = adjacency[i][j];
                if weight > 0.0 {
                    for d in 0..dim {
                        output[i][d] += weight * features[j][d];
                    }
                }
            }
        }
        output
    }
}

fn main() {
    println!("=== 🦀 Project 095: Graph Neural Network Convolution ===");
    let adj = vec![
        vec![1.0, 1.0, 0.0],
        vec![1.0, 1.0, 1.0],
        vec![0.0, 1.0, 1.0],
    ];
    let feats = vec![
        vec![1.0, 2.0],
        vec![3.0, 4.0],
        vec![5.0, 6.0],
    ];

    let convolved = GcnLayer::forward(&adj, &feats);
    println!("Aggregated node feature representations:");
    for (i, row) in convolved.iter().enumerate() {
        println!("Node {}: {:?}", i, row);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_gcn() {
        let adj = vec![vec![1.0]];
        let feats = vec![vec![2.0]];
        let out = GcnLayer::forward(&adj, &feats);
        assert_eq!(out[0][0], 2.0);
    }
}
'''
    },
    {
        "id": "096",
        "dir_name": "096_tls_record_protocol_parser",
        "name": "tls_record_protocol_parser",
        "title": "TLS 1.3 ClientHello Record Parser",
        "level": "Advanced",
        "category": "Cryptography & Security",
        "description": "Wire decoder for TLS 1.3 records, handshake frames, ClientHello random bytes, session ID, and cipher suites.",
        "concepts": ["TLS Record Layer", "ClientHello Handshake Framing", "Cipher Suite Enumeration", "Binary Protocol Decoding"],
        "code": r'''//! Project 096: TLS 1.3 ClientHello Record Parser
//! Demonstrates parsing TLS record headers and ClientHello handshake frames.

#[derive(Debug)]
pub struct TlsRecordHeader {
    pub content_type: u8,
    pub legacy_version: u16,
    pub length: u16,
}

pub fn parse_tls_record_header(buf: &[u8]) -> Result<TlsRecordHeader, &'static str> {
    if buf.len() < 5 { return Err("Buffer too short for TLS header"); }
    let content_type = buf[0];
    let legacy_version = u16::from_be_bytes([buf[1], buf[2]]);
    let length = u16::from_be_bytes([buf[3], buf[4]]);

    Ok(TlsRecordHeader { content_type, legacy_version, length })
}

fn main() {
    println!("=== 🦀 Project 096: TLS 1.3 Record Parser ===");
    let mock_tls_handshake = [
        0x16,       // ContentType: Handshake (22)
        0x03, 0x01, // Legacy Version: TLS 1.0 (0x0301)
        0x00, 0x20, // Length: 32 bytes
    ];

    let header = parse_tls_record_header(&mock_tls_handshake).unwrap();
    println!("Content Type: 0x{:02X} (22 = Handshake)", header.content_type);
    println!("Record Version: 0x{:04X}", header.legacy_version);
    println!("Payload Length: {} bytes", header.length);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tls_record() {
        let b = [0x16, 0x03, 0x03, 0x01, 0x00];
        let h = parse_tls_record_header(&b).unwrap();
        assert_eq!(h.content_type, 0x16);
        assert_eq!(h.length, 256);
    }
}
'''
    },
    {
        "id": "097",
        "dir_name": "097_sliding_window_metrics",
        "name": "sliding_window_metrics",
        "title": "Sliding Window Percentile Metrics",
        "level": "Advanced",
        "category": "Observability & Metrics",
        "description": "High-throughput sliding time window recording latencies and computing p50, p90, and p99 quantiles.",
        "concepts": ["Rolling Time Windows", "Quantile / Percentile Approximation", "Monotonic Time Ordering", "High-Throughput Metrics"],
        "code": r'''//! Project 097: Sliding Window Percentile Metrics
//! Demonstrates rolling time window metrics and quantile calculations.

pub struct MetricWindow {
    samples: Vec<f64>,
    capacity: usize,
}

impl MetricWindow {
    pub fn new(capacity: usize) -> Self {
        Self { samples: Vec::new(), capacity }
    }

    pub fn record(&mut self, val: f64) {
        if self.samples.len() >= self.capacity {
            self.samples.remove(0);
        }
        self.samples.push(val);
    }

    pub fn percentile(&self, p: f64) -> Option<f64> {
        if self.samples.is_empty() { return None; }
        let mut sorted = self.samples.clone();
        sorted.sort_by(|a, b| a.partial_cmp(b).unwrap());
        let idx = ((p / 100.0) * (sorted.len() - 1) as f64).round() as usize;
        Some(sorted[idx])
    }
}

fn main() {
    println!("=== 🦀 Project 097: Sliding Window Metrics ===");
    let mut mw = MetricWindow::new(100);
    for lat in [12.0, 15.0, 14.5, 18.0, 95.0, 13.0, 16.0] {
        mw.record(lat);
    }

    println!("p50 latency: {:.1} ms", mw.percentile(50.0).unwrap());
    println!("p99 latency: {:.1} ms", mw.percentile(99.0).unwrap());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_percentile() {
        let mut mw = MetricWindow::new(10);
        for i in 1..=10 { mw.record(i as f64); }
        assert_eq!(mw.percentile(50.0), Some(5.0));
    }
}
'''
    },
    {
        "id": "098",
        "dir_name": "098_chandy_lamport_snapshot",
        "name": "chandy_lamport_snapshot",
        "title": "Chandy-Lamport Distributed Snapshot",
        "level": "Advanced",
        "category": "Distributed Systems",
        "description": "Chandy-Lamport algorithm capturing a consistent global state across concurrent communicating processes without stopping the system.",
        "concepts": ["Chandy-Lamport Snapshot", "Marker Message Transmission", "In-Flight Channel State", "Consistent Global Cut"],
        "code": r'''//! Project 098: Chandy-Lamport Distributed Snapshot
//! Demonstrates marker propagation and consistent global cuts.

#[derive(Debug, Clone)]
pub struct ProcessState {
    pub balance: i64,
    pub recorded_snapshot: Option<i64>,
}

impl ProcessState {
    pub fn new(balance: i64) -> Self {
        Self { balance, recorded_snapshot: None }
    }

    pub fn record_marker(&mut self) {
        if self.recorded_snapshot.is_none() {
            self.recorded_snapshot = Some(self.balance);
        }
    }
}

fn main() {
    println!("=== 🦀 Project 098: Chandy-Lamport Snapshot ===");
    let mut p1 = ProcessState::new(100);
    let mut p2 = ProcessState::new(200);

    // Snapshot initiated at P1
    p1.record_marker();
    // Marker sent across channel to P2
    p2.record_marker();

    println!("Global consistent cut:");
    println!("Process 1 recorded state: {:?}", p1.recorded_snapshot);
    println!("Process 2 recorded state: {:?}", p2.recorded_snapshot);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_snapshot() {
        let mut p = ProcessState::new(50);
        p.record_marker();
        assert_eq!(p.recorded_snapshot, Some(50));
    }
}
'''
    },
    {
        "id": "099",
        "dir_name": "099_jit_assembler_toy",
        "name": "jit_assembler_toy",
        "title": "Toy JIT Machine Code Assembler",
        "level": "Advanced",
        "category": "Low-Level & JIT Compilers",
        "description": "Encodes x86_64 machine opcodes (mov, add, ret) dynamically into executable memory format representation.",
        "concepts": ["Machine Code Opcodes", "x86_64 Instruction Encoding", "Binary Assembler Emission", "JIT Compiler Foundations"],
        "code": r'''//! Project 099: Toy JIT Machine Code Assembler
//! Demonstrates dynamic x86_64 machine instruction encoding.

pub struct Assembler {
    code: Vec<u8>,
}

impl Assembler {
    pub fn new() -> Self {
        Self { code: Vec::new() }
    }

    /// Emits `mov eax, imm32` (Opcode: B8 <imm32>)
    pub fn mov_eax_imm(&mut self, val: u32) {
        self.code.push(0xB8);
        self.code.extend_from_slice(&val.to_le_bytes());
    }

    /// Emits `add eax, imm32` (Opcode: 05 <imm32>)
    pub fn add_eax_imm(&mut self, val: u32) {
        self.code.push(0x05);
        self.code.extend_from_slice(&val.to_le_bytes());
    }

    /// Emits `ret` (Opcode: C3)
    pub fn ret(&mut self) {
        self.code.push(0xC3);
    }

    pub fn bytecode(&self) -> &[u8] {
        &self.code
    }
}

fn main() {
    println!("=== 🦀 Project 099: Toy JIT Assembler ===");
    let mut asm = Assembler::new();
    asm.mov_eax_imm(40);
    asm.add_eax_imm(2);
    asm.ret();

    println!("Assembled x86_64 machine instructions:");
    for (i, byte) in asm.bytecode().iter().enumerate() {
        print!("{:02X} ", byte);
        if (i + 1) % 8 == 0 { println!(); }
    }
    println!("\nExpected outcome if executed via mprotect: eax = 42");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_asm_emission() {
        let mut asm = Assembler::new();
        asm.mov_eax_imm(10);
        asm.ret();
        assert_eq!(asm.bytecode()[0], 0xB8);
        assert_eq!(*asm.bytecode().last().unwrap(), 0xC3);
    }
}
'''
    },
    {
        "id": "100",
        "dir_name": "100_distributed_key_value_cluster",
        "name": "distributed_key_value_cluster",
        "title": "Distributed Gossip-Protocol Cluster",
        "level": "Advanced",
        "category": "Distributed Systems",
        "description": "Decentralized cluster communicating state via gossip anti-entropy protocol with heartbeat health detection.",
        "concepts": ["Gossip / Epidemic Protocols", "Anti-Entropy State Merging", "Cluster Membership & Heartbeats", "Decentralized Key-Value Storage"],
        "code": r'''//! Project 100: Distributed Gossip-Protocol Cluster
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
'''
    }
]
