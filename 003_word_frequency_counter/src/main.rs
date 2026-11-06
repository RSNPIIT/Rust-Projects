//! Project 003: Word Frequency Counter
//! Demonstrates HashMap, string slices, tokenization, and sorting by count.

use std::collections::HashMap;

pub struct WordCounter {
    counts: HashMap<String, usize>,
}

impl WordCounter {
    pub fn new() -> Self {
        Self { counts: HashMap::new() }
    }

    pub fn process_text(&mut self, text: &str) {
        for word in text.split_whitespace() {
            let cleaned: String = word
                .chars()
                .filter(|c| c.is_alphanumeric())
                .flat_map(|c| c.to_lowercase())
                .collect();

            if !cleaned.is_empty() {
                *self.counts.entry(cleaned).or_insert(0) += 1;
            }
        }
    }

    pub fn top_words(&self, n: usize) -> Vec<(String, usize)> {
        let mut pairs: Vec<(String, usize)> = self.counts
            .iter()
            .map(|(w, &c)| (w.clone(), c))
            .collect();
        pairs.sort_by(|a, b| b.1.cmp(&a.1).then_with(|| a.0.cmp(&b.0)));
        pairs.truncate(n);
        pairs
    }

    pub fn total_unique(&self) -> usize {
        self.counts.len()
    }
}

fn main() {
    println!("=== 🦀 Project 003: Word Frequency Counter ===");
    let passage = "To be, or not to be, that is the question: \
                   Whether 'tis nobler in the mind to suffer \
                   The slings and arrows of outrageous fortune, \
                   Or to take arms against a sea of troubles";

    let mut counter = WordCounter::new();
    counter.process_text(passage);

    println!("Total unique words: {}", counter.total_unique());
    println!("\nTop 5 frequent words:");
    for (word, count) in counter.top_words(5) {
        println!(" - {:<12}: {}", word, count);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_frequency_counting() {
        let mut counter = WordCounter::new();
        counter.process_text("Rust rust RUST, programming in Rust!");
        assert_eq!(counter.counts.get("rust"), Some(&4));
        assert_eq!(counter.counts.get("programming"), Some(&1));
        assert_eq!(counter.counts.get("in"), Some(&1));
    }
}
