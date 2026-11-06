//! Project 013: Configurable Password Generator
//! Demonstrates character pool configuration, pseudo-random sampling, and entropy estimation.

pub struct PasswordConfig {
    pub length: usize,
    pub use_uppercase: bool,
    pub use_lowercase: bool,
    pub use_numbers: bool,
    pub use_symbols: bool,
}

impl Default for PasswordConfig {
    fn default() -> Self {
        Self {
            length: 16,
            use_uppercase: true,
            use_lowercase: true,
            use_numbers: true,
            use_symbols: true,
        }
    }
}

pub fn generate_password(config: &PasswordConfig, mut seed: u64) -> (String, f64) {
    let mut pool = Vec::new();
    if config.use_uppercase { pool.extend(b'A'..=b'Z'); }
    if config.use_lowercase { pool.extend(b'a'..=b'z'); }
    if config.use_numbers { pool.extend(b'0'..=b'9'); }
    if config.use_symbols { pool.extend(b"!@#$%^&*()-_=+[]{}"); }

    if pool.is_empty() {
        return (String::new(), 0.0);
    }

    let mut result = String::with_capacity(config.length);
    for _ in 0..config.length {
        seed = seed.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        let idx = ((seed >> 32) as usize) % pool.len();
        result.push(pool[idx] as char);
    }

    let entropy = (config.length as f64) * (pool.len() as f64).log2();
    (result, entropy)
}

fn main() {
    println!("=== 🦀 Project 013: Configurable Password Generator ===");
    let config = PasswordConfig::default();
    let (pwd, entropy) = generate_password(&config, 987654321);
    println!("Generated Password: {}", pwd);
    println!("Estimated Entropy:  {:.1} bits", entropy);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_password_length() {
        let config = PasswordConfig { length: 24, ..Default::default() };
        let (pwd, _) = generate_password(&config, 12345);
        assert_eq!(pwd.len(), 24);
    }
}
