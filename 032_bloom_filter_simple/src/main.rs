//! Project 032: Probabilistic Bloom Filter
//! Demonstrates space-efficient set membership with zero false negatives.

pub struct SimpleBloomFilter {
    bits: Vec<bool>,
    size: usize,
}

impl SimpleBloomFilter {
    pub fn new(size: usize) -> Self {
        Self { bits: vec![false; size], size }
    }

    fn hash1(&self, s: &str) -> usize {
        let mut h: u64 = 5381;
        for b in s.bytes() {
            h = ((h << 5).wrapping_add(h)).wrapping_add(b as u64);
        }
        (h as usize) % self.size
    }

    fn hash2(&self, s: &str) -> usize {
        let mut h: u64 = 0;
        for b in s.bytes() {
            h = (b as u64).wrapping_add(h << 6).wrapping_add(h << 16).wrapping_sub(h);
        }
        (h as usize) % self.size
    }

    pub fn insert(&mut self, item: &str) {
        let h1 = self.hash1(item);
        let h2 = self.hash2(item);
        self.bits[h1] = true;
        self.bits[h2] = true;
    }

    pub fn contains(&self, item: &str) -> bool {
        let h1 = self.hash1(item);
        let h2 = self.hash2(item);
        self.bits[h1] && self.bits[h2]
    }
}

fn main() {
    println!("=== 🦀 Project 032: Probabilistic Bloom Filter ===");
    let mut bf = SimpleBloomFilter::new(100);
    bf.insert("apple");
    bf.insert("banana");
    bf.insert("orange");

    println!("Contains 'apple':  {}", bf.contains("apple"));
    println!("Contains 'banana': {}", bf.contains("banana"));
    println!("Contains 'grape':  {}", bf.contains("grape"));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bloom() {
        let mut bf = SimpleBloomFilter::new(256);
        bf.insert("test_key");
        assert!(bf.contains("test_key"));
    }
}
