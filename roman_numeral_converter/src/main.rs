//! Project 015: Roman Numeral Converter
//! Demonstrates integer to Roman numeral conversion and parsing.

const ROMAN_SYMBOLS: &[(u32, &str)] = &[
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
];

pub fn to_roman(mut num: u32) -> Result<String, &'static str> {
    if num == 0 || num > 3999 {
        return Err("Number must be between 1 and 3999");
    }
    let mut result = String::new();
    for &(val, sym) in ROMAN_SYMBOLS {
        while num >= val {
            result.push_str(sym);
            num -= val;
        }
    }
    Ok(result)
}

pub fn from_roman(s: &str) -> Result<u32, &'static str> {
    let mut total = 0;
    let mut chars = s.chars().peekable();

    while let Some(c) = chars.next() {
        let val = match c {
            'M' => 1000,
            'D' => 500,
            'C' => match chars.peek() {
                Some('M') => { chars.next(); 900 }
                Some('D') => { chars.next(); 400 }
                _ => 100,
            },
            'L' => 50,
            'X' => match chars.peek() {
                Some('C') => { chars.next(); 90 }
                Some('L') => { chars.next(); 40 }
                _ => 10,
            },
            'V' => 5,
            'I' => match chars.peek() {
                Some('X') => { chars.next(); 9 }
                Some('V') => { chars.next(); 4 }
                _ => 1,
            },
            _ => return Err("Invalid Roman character"),
        };
        total += val;
    }
    Ok(total)
}

fn main() {
    println!("=== 🦀 Project 015: Roman Numeral Converter ===");
    let numbers = [1984, 2024, 49, 3999];
    for &n in &numbers {
        let roman = to_roman(n).unwrap();
        let decoded = from_roman(&roman).unwrap();
        println!("{:<5} -> {:<10} -> {:<5}", n, roman, decoded);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_roman_conversion() {
        assert_eq!(to_roman(1984).unwrap(), "MCMLXXXIV");
        assert_eq!(from_roman("MCMLXXXIV").unwrap(), 1984);
        assert_eq!(to_roman(2024).unwrap(), "MMXXIV");
        assert_eq!(from_roman("MMXXIV").unwrap(), 2024);
    }
}
