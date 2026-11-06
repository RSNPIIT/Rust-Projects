//! Project 043: Huffman Coding & Compression
//! Demonstrates Huffman tree construction, prefix coding, and bitstream compression.

use std::cmp::Ordering;
use std::collections::{BinaryHeap, HashMap};

#[derive(Debug, Eq, PartialEq)]
enum Node {
    Leaf(char, usize),
    Internal(usize, Box<Node>, Box<Node>),
}

impl Node {
    fn freq(&self) -> usize {
        match self {
            Node::Leaf(_, f) => *f,
            Node::Internal(f, _, _) => *f,
        }
    }
}

impl Ord for Node {
    fn cmp(&self, other: &Self) -> Ordering {
        other.freq().cmp(&self.freq())
    }
}

impl PartialOrd for Node {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

pub struct HuffmanCoder {
    root: Option<Node>,
    table: HashMap<char, String>,
}

impl HuffmanCoder {
    pub fn build(text: &str) -> Self {
        let mut freq_map = HashMap::new();
        for c in text.chars() {
            *freq_map.entry(c).or_insert(0) += 1;
        }

        let mut heap: BinaryHeap<Node> = freq_map
            .into_iter()
            .map(|(c, f)| Node::Leaf(c, f))
            .collect();

        while heap.len() > 1 {
            let left = Box::new(heap.pop().unwrap());
            let right = Box::new(heap.pop().unwrap());
            let sum_freq = left.freq() + right.freq();
            heap.push(Node::Internal(sum_freq, left, right));
        }

        let root = heap.pop();
        let mut table = HashMap::new();
        if let Some(ref r) = root {
            Self::build_table(r, String::new(), &mut table);
        }

        Self { root, table }
    }

    fn build_table(node: &Node, prefix: String, table: &mut HashMap<char, String>) {
        match node {
            Node::Leaf(c, _) => {
                table.insert(*c, if prefix.is_empty() { "0".to_string() } else { prefix });
            }
            Node::Internal(_, left, right) => {
                Self::build_table(left, format!("{}0", prefix), table);
                Self::build_table(right, format!("{}1", prefix), table);
            }
        }
    }

    pub fn encode(&self, text: &str) -> String {
        let mut bitstream = String::new();
        for c in text.chars() {
            if let Some(code) = self.table.get(&c) {
                bitstream.push_str(code);
            }
        }
        bitstream
    }
}

fn main() {
    println!("=== 🦀 Project 043: Huffman Coding ===");
    let msg = "ABRACADABRA";
    let coder = HuffmanCoder::build(msg);
    let encoded = coder.encode(msg);

    println!("Original: {}", msg);
    println!("Bitstream: {}", encoded);
    println!("Original bits: {} vs Huffman bits: {}", msg.len() * 8, encoded.len());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_huffman_encoding() {
        let coder = HuffmanCoder::build("AAAAABBBCC");
        let enc = coder.encode("ABC");
        assert!(!enc.is_empty());
    }
}
