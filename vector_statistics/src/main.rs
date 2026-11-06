//! Project 023: Vector Statistical Calculator
//! Demonstrates mean, median, mode, variance, and standard deviation calculations.

use std::collections::HashMap;

pub struct Stats {
    pub mean: f64,
    pub median: f64,
    pub mode: f64,
    pub variance: f64,
    pub std_dev: f64,
}

pub fn calculate_stats(numbers: &[f64]) -> Option<Stats> {
    if numbers.is_empty() {
        return None;
    }
    let n = numbers.len() as f64;
    let sum: f64 = numbers.iter().sum();
    let mean = sum / n;

    let mut sorted = numbers.to_vec();
    sorted.sort_by(|a, b| a.partial_cmp(b).unwrap());

    let median = if sorted.len() % 2 == 1 {
        sorted[sorted.len() / 2]
    } else {
        (sorted[sorted.len() / 2 - 1] + sorted[sorted.len() / 2]) / 2.0
    };

    let mut freq = HashMap::new();
    for &num in numbers {
        *freq.entry(num.to_bits()).or_insert(0) += 1;
    }
    let mode_bits = freq.into_iter().max_by_key(|&(_, count)| count).map(|(val, _)| val).unwrap();
    let mode = f64::from_bits(mode_bits);

    let variance = numbers.iter().map(|x| (x - mean).powi(2)).sum::<f64>() / n;
    let std_dev = variance.sqrt();

    Some(Stats { mean, median, mode, variance, std_dev })
}

fn main() {
    println!("=== 🦀 Project 023: Vector Statistical Calculator ===");
    let data = [10.0, 12.0, 23.0, 23.0, 16.0, 23.0, 21.0, 16.0];
    let stats = calculate_stats(&data).unwrap();
    println!("Data: {:?}", data);
    println!("Mean:      {:.2}", stats.mean);
    println!("Median:    {:.2}", stats.median);
    println!("Mode:      {:.2}", stats.mode);
    println!("Std Dev:   {:.2}", stats.std_dev);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_stats() {
        let nums = [1.0, 2.0, 3.0, 4.0, 5.0];
        let s = calculate_stats(&nums).unwrap();
        assert_eq!(s.mean, 3.0);
        assert_eq!(s.median, 3.0);
    }
}
