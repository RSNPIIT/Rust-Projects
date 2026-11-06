//! Project 076: Vector Similarity Search Engine
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
