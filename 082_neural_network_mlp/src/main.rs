//! Project 082: Multi-Layer Perceptron (MLP) Neural Net
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
