//! Project 009: Caesar Cipher Tool
//! Demonstrates character transformation and modular arithmetic encryption.

pub fn encrypt(text: &str, shift: i32) -> String {
    let normalized_shift = ((shift % 26) + 26) % 26;
    text.chars()
        .map(|c| {
            if c.is_ascii_lowercase() {
                let base = b'a';
                let offset = (c as u8 - base + normalized_shift as u8) % 26;
                (base + offset) as char
            } else if c.is_ascii_uppercase() {
                let base = b'A';
                let offset = (c as u8 - base + normalized_shift as u8) % 26;
                (base + offset) as char
            } else {
                c
            }
        })
        .collect()
}

pub fn decrypt(text: &str, shift: i32) -> String {
    encrypt(text, -shift)
}

fn main() {
    println!("=== 🦀 Project 009: Caesar Cipher Tool ===");
    let original = "Hello, Rustaceans! Secret Key: 1337.";
    let shift = 3;

    let ciphered = encrypt(original, shift);
    let recovered = decrypt(&ciphered, shift);

    println!("Original:  {}", original);
    println!("Encrypted: {}", ciphered);
    println!("Decrypted: {}", recovered);
    assert_eq!(original, recovered);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_caesar() {
        let msg = "The Quick Brown Fox Jumps Over The Lazy Dog";
        let encrypted = encrypt(msg, 5);
        assert_eq!(decrypt(&encrypted, 5), msg);
    }
}
