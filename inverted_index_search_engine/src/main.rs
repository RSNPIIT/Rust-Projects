//! Project 084: Inverted Index Search Engine
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
