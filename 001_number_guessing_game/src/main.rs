//! Project 001: Number Guessing Game
//! Demonstrates standard I/O, control flow, custom PRNG, and game loop logic.

use std::cmp::Ordering;

/// A simple linear congruential generator (LCG) for deterministic pseudo-random numbers
/// without requiring external crates.
#[derive(Debug)]
pub struct SimpleRng {
    state: u64,
}

impl SimpleRng {
    pub fn new(seed: u64) -> Self {
        Self { state: seed }
    }

    pub fn gen_range(&mut self, min: u32, max: u32) -> u32 {
        self.state = self.state.wrapping_mul(6364136223846793005).wrapping_add(1);
        let val = ((self.state >> 33) as u32) % (max - min + 1);
        min + val
    }
}

pub struct GuessingGame {
    secret_number: u32,
    attempts: u32,
    is_solved: bool,
}

impl GuessingGame {
    pub fn new(secret_number: u32) -> Self {
        Self {
            secret_number,
            attempts: 0,
            is_solved: false,
        }
    }

    pub fn make_guess(&mut self, guess: u32) -> Ordering {
        self.attempts += 1;
        let ord = guess.cmp(&self.secret_number);
        if ord == Ordering::Equal {
            self.is_solved = true;
        }
        ord
    }

    pub fn attempts(&self) -> u32 {
        self.attempts
    }

    pub fn is_solved(&self) -> bool {
        self.is_solved
    }
}

fn main() {
    println!("=== 🦀 Project 001: Number Guessing Game ===");
    let mut rng = SimpleRng::new(42);
    let secret = rng.gen_range(1, 100);
    println!("Generating a secret number between 1 and 100...");

    let mut game = GuessingGame::new(secret);
    let simulated_guesses = [50, 75, 62, secret];

    for &guess in &simulated_guesses {
        print!("Guessing {}: ", guess);
        match game.make_guess(guess) {
            Ordering::Less => println!("Too small!"),
            Ordering::Greater => println!("Too big!"),
            Ordering::Equal => {
                println!("You win! Solved in {} attempts.", game.attempts());
                break;
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_game_logic() {
        let mut game = GuessingGame::new(42);
        assert_eq!(game.make_guess(20), Ordering::Less);
        assert_eq!(game.make_guess(60), Ordering::Greater);
        assert_eq!(game.make_guess(42), Ordering::Equal);
        assert!(game.is_solved());
        assert_eq!(game.attempts(), 3);
    }

    #[test]
    fn test_rng_bounds() {
        let mut rng = SimpleRng::new(12345);
        for _ in 0..100 {
            let n = rng.gen_range(10, 20);
            assert!(n >= 10 && n <= 20);
        }
    }
}
