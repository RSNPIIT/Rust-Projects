//! Project 058: Scalable Partitioned Bloom Filter
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
