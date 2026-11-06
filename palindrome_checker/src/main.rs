//! Project 006: Palindrome Checker
//! Demonstrates double-ended iterators, Unicode handling, and case normalization.

pub fn is_palindrome(s: &str) -> bool {
    let clean_chars: Vec<char> = s
        .chars()
        .filter(|c| c.is_alphanumeric())
        .flat_map(|c| c.to_lowercase())
        .collect();

    if clean_chars.is_empty() {
        return true;
    }

    let mut left = 0;
    let mut right = clean_chars.len() - 1;

    while left < right {
        if clean_chars[left] != clean_chars[right] {
            return false;
        }
        left += 1;
        right -= 1;
    }
    true
}

fn main() {
    println!("=== 🦀 Project 006: Palindrome Checker ===");
    let samples = [
        "A man, a plan, a canal: Panama",
        "race a car",
        "Was it a car or a cat I saw?",
        "No 'x' in Nixon",
        "Rustaceans",
    ];

    for s in samples {
        println!("\"{}\" -> {}", s, if is_palindrome(s) { "✅ PALINDROME" } else { "❌ NOT PALINDROME" });
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_palindromes() {
        assert!(is_palindrome("A man, a plan, a canal: Panama"));
        assert!(is_palindrome("Was it a car or a cat I saw?"));
        assert!(is_palindrome("racecar"));
        assert!(!is_palindrome("hello world"));
    }
}
