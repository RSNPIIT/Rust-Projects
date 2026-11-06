//! Project 030: Levenshtein Distance & Fuzzy Matcher
//! Demonstrates 2D dynamic programming and string similarity metrics.

use std::cmp::min;

pub fn levenshtein(s1: &str, s2: &str) -> usize {
    let v1: Vec<char> = s1.chars().collect();
    let v2: Vec<char> = s2.chars().collect();
    let len1 = v1.len();
    let len2 = v2.len();

    let mut dp = vec![vec![0; len2 + 1]; len1 + 1];

    for i in 0..=len1 { dp[i][0] = i; }
    for j in 0..=len2 { dp[0][j] = j; }

    for i in 1..=len1 {
        for j in 1..=len2 {
            let cost = if v1[i - 1] == v2[j - 1] { 0 } else { 1 };
            dp[i][j] = min(
                dp[i - 1][j] + 1, // deletion
                min(
                    dp[i][j - 1] + 1, // insertion
                    dp[i - 1][j - 1] + cost, // substitution
                ),
            );
        }
    }

    dp[len1][len2]
}

pub fn similarity(s1: &str, s2: &str) -> f64 {
    let max_len = s1.len().max(s2.len());
    if max_len == 0 { return 1.0; }
    1.0 - (levenshtein(s1, s2) as f64 / max_len as f64)
}

fn main() {
    println!("=== 🦀 Project 030: Levenshtein Distance ===");
    let pairs = [
        ("kitten", "sitting"),
        ("rosettacode", "raisethysword"),
        ("rust", "trust"),
    ];

    for (a, b) in pairs {
        let dist = levenshtein(a, b);
        let sim = similarity(a, b);
        println!("{:>12} vs {:<14} => Dist: {}, Sim: {:.1}%", a, b, dist, sim * 100.0);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_levenshtein() {
        assert_eq!(levenshtein("kitten", "sitting"), 3);
        assert_eq!(levenshtein("flaw", "lawn"), 2);
    }
}
