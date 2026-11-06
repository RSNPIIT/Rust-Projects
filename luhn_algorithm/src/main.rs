//! Project 018: Luhn Algorithm Validator
//! Demonstrates the Luhn checksum formula (Mod 10).

pub fn is_valid_luhn(card_number: &str) -> bool {
    let digits: Vec<u32> = card_number
        .chars()
        .filter(|c| !c.is_whitespace() && *c != '-')
        .filter_map(|c| c.to_digit(10))
        .collect();

    if digits.len() <= 1 {
        return false;
    }

    let mut sum = 0;
    for (i, &digit) in digits.iter().rev().enumerate() {
        if i % 2 == 1 {
            let doubled = digit * 2;
            sum += if doubled > 9 { doubled - 9 } else { doubled };
        } else {
            sum += digit;
        }
    }
    sum % 10 == 0
}

fn main() {
    println!("=== 🦀 Project 018: Luhn Algorithm Validator ===");
    let cards = [
        ("49927398716", true),
        ("49927398717", false),
        ("1234-5678-9012-3456", false),
        ("79927398713", true),
    ];

    for (card, expected) in cards {
        let valid = is_valid_luhn(card);
        println!("Card: {:<22} Valid: {} (Expected: {})", card, valid, expected);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_luhn() {
        assert!(is_valid_luhn("79927398713"));
        assert!(!is_valid_luhn("79927398714"));
    }
}
