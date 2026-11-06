//! Project 095: Graph Convolutional Network (GCN) Layer
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
