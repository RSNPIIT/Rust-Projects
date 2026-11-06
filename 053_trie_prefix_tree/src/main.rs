//! Project 053: Trie Prefix Tree Autocomplete
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
