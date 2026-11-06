# projects_001_to_025.py

PROJECTS_001_TO_025 = [
    {
        "id": "001",
        "dir_name": "001_number_guessing_game",
        "name": "number_guessing_game",
        "title": "Number Guessing Game",
        "level": "Simple",
        "category": "CLI & Game Logic",
        "description": "Interactive number guessing game with binary search hint system, input validation, and attempts tracking.",
        "concepts": ["Standard I/O", "Looping & Pattern Matching", "Parsing Strings to Numbers", "Pseudo-Random Number Generation (LCG)", "Unit Testing"],
        "code": r'''//! Project 001: Number Guessing Game
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
'''
    },
    {
        "id": "002",
        "dir_name": "002_temperature_converter",
        "name": "temperature_converter",
        "title": "Temperature Converter",
        "level": "Simple",
        "category": "Math & Enums",
        "description": "Multi-scale temperature converter supporting Celsius, Fahrenheit, and Kelvin with custom enum traits and precision rounding.",
        "concepts": ["Enums with Methods", "Traits (Display, From)", "Floating Point Precision", "Exhaustive Pattern Matching"],
        "code": r'''//! Project 002: Temperature Converter
//! Demonstrates enums with methods, traits, and unit conversions.

use std::fmt;

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum TemperatureScale {
    Celsius,
    Fahrenheit,
    Kelvin,
}

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Temperature {
    pub value: f64,
    pub scale: TemperatureScale,
}

impl Temperature {
    pub fn new(value: f64, scale: TemperatureScale) -> Self {
        Self { value, scale }
    }

    pub fn to_celsius(self) -> Self {
        let c = match self.scale {
            TemperatureScale::Celsius => self.value,
            TemperatureScale::Fahrenheit => (self.value - 32.0) * 5.0 / 9.0,
            TemperatureScale::Kelvin => self.value - 273.15,
        };
        Self::new(c, TemperatureScale::Celsius)
    }

    pub fn to_fahrenheit(self) -> Self {
        let f = match self.scale {
            TemperatureScale::Celsius => (self.value * 9.0 / 5.0) + 32.0,
            TemperatureScale::Fahrenheit => self.value,
            TemperatureScale::Kelvin => ((self.value - 273.15) * 9.0 / 5.0) + 32.0,
        };
        Self::new(f, TemperatureScale::Fahrenheit)
    }

    pub fn to_kelvin(self) -> Self {
        let k = match self.scale {
            TemperatureScale::Celsius => self.value + 273.15,
            TemperatureScale::Fahrenheit => ((self.value - 32.0) * 5.0 / 9.0) + 273.15,
            TemperatureScale::Kelvin => self.value,
        };
        Self::new(k, TemperatureScale::Kelvin)
    }
}

impl fmt::Display for Temperature {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let symbol = match self.scale {
            TemperatureScale::Celsius => "°C",
            TemperatureScale::Fahrenheit => "°F",
            TemperatureScale::Kelvin => "K",
        };
        write!(f, "{:.2}{}", self.value, symbol)
    }
}

fn main() {
    println!("=== 🦀 Project 002: Temperature Converter ===");
    let water_boiling = Temperature::new(100.0, TemperatureScale::Celsius);
    println!("Boiling point: {}", water_boiling);
    println!("In Fahrenheit: {}", water_boiling.to_fahrenheit());
    println!("In Kelvin:     {}", water_boiling.to_kelvin());

    let body_temp = Temperature::new(98.6, TemperatureScale::Fahrenheit);
    println!("\nHuman body temp: {}", body_temp);
    println!("In Celsius:     {}", body_temp.to_celsius());
    println!("In Kelvin:      {}", body_temp.to_kelvin());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_celsius_to_fahrenheit() {
        let c = Temperature::new(0.0, TemperatureScale::Celsius);
        let f = c.to_fahrenheit();
        assert!((f.value - 32.0).abs() < 1e-4);
    }

    #[test]
    fn test_round_trip() {
        let k = Temperature::new(300.0, TemperatureScale::Kelvin);
        let round_trip = k.to_celsius().to_fahrenheit().to_kelvin();
        assert!((round_trip.value - 300.0).abs() < 1e-3);
    }
}
'''
    },
    {
        "id": "003",
        "dir_name": "003_word_frequency_counter",
        "name": "word_frequency_counter",
        "title": "Word Frequency Counter",
        "level": "Simple",
        "category": "Text & Collections",
        "description": "Tokenizes text, strips punctuation, normalizes case, and counts word occurrences using HashMap and sorting.",
        "concepts": ["HashMap Entry API", "Iterators & Closures", "String Normalization", "Custom Sorting (Ord / PartialOrd)"],
        "code": r'''//! Project 003: Word Frequency Counter
//! Demonstrates HashMap, string slices, tokenization, and sorting by count.

use std::collections::HashMap;

pub struct WordCounter {
    counts: HashMap<String, usize>,
}

impl WordCounter {
    pub fn new() -> Self {
        Self { counts: HashMap::new() }
    }

    pub fn process_text(&mut self, text: &str) {
        for word in text.split_whitespace() {
            let cleaned: String = word
                .chars()
                .filter(|c| c.is_alphanumeric())
                .flat_map(|c| c.to_lowercase())
                .collect();

            if !cleaned.is_empty() {
                *self.counts.entry(cleaned).or_insert(0) += 1;
            }
        }
    }

    pub fn top_words(&self, n: usize) -> Vec<(String, usize)> {
        let mut pairs: Vec<(String, usize)> = self.counts
            .iter()
            .map(|(w, &c)| (w.clone(), c))
            .collect();
        pairs.sort_by(|a, b| b.1.cmp(&a.1).then_with(|| a.0.cmp(&b.0)));
        pairs.truncate(n);
        pairs
    }

    pub fn total_unique(&self) -> usize {
        self.counts.len()
    }
}

fn main() {
    println!("=== 🦀 Project 003: Word Frequency Counter ===");
    let passage = "To be, or not to be, that is the question: \
                   Whether 'tis nobler in the mind to suffer \
                   The slings and arrows of outrageous fortune, \
                   Or to take arms against a sea of troubles";

    let mut counter = WordCounter::new();
    counter.process_text(passage);

    println!("Total unique words: {}", counter.total_unique());
    println!("\nTop 5 frequent words:");
    for (word, count) in counter.top_words(5) {
        println!(" - {:<12}: {}", word, count);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_frequency_counting() {
        let mut counter = WordCounter::new();
        counter.process_text("Rust rust RUST, programming in Rust!");
        assert_eq!(counter.counts.get("rust"), Some(&4));
        assert_eq!(counter.counts.get("programming"), Some(&1));
        assert_eq!(counter.counts.get("in"), Some(&1));
    }
}
'''
    },
    {
        "id": "004",
        "dir_name": "004_cli_calculator",
        "name": "cli_calculator",
        "title": "CLI Calculator",
        "level": "Simple",
        "category": "Parsing & Math",
        "description": "Arithmetic calculator supporting +, -, *, /, parenthesis, and operator precedence using the Shunting-Yard algorithm.",
        "concepts": ["Lexing / Tokenization", "Shunting-Yard Algorithm", "Reverse Polish Notation (RPN)", "Error Handling (Result/Option)"],
        "code": r'''//! Project 004: CLI Calculator
//! Demonstrates tokenization, Shunting-yard algorithm, and RPN stack evaluation.

#[derive(Debug, PartialEq, Clone)]
pub enum Token {
    Number(f64),
    Plus,
    Minus,
    Multiply,
    Divide,
    LParen,
    RParen,
}

pub fn tokenize(expr: &str) -> Result<Vec<Token>, String> {
    let mut tokens = Vec::new();
    let mut chars = expr.chars().peekable();

    while let Some(&c) = chars.peek() {
        match c {
            ' ' | '\t' | '\n' => { chars.next(); }
            '+' => { tokens.push(Token::Plus); chars.next(); }
            '-' => { tokens.push(Token::Minus); chars.next(); }
            '*' => { tokens.push(Token::Multiply); chars.next(); }
            '/' => { tokens.push(Token::Divide); chars.next(); }
            '(' => { tokens.push(Token::LParen); chars.next(); }
            ')' => { tokens.push(Token::RParen); chars.next(); }
            '0'..='9' | '.' => {
                let mut num_str = String::new();
                while let Some(&ch) = chars.peek() {
                    if ch.is_digit(10) || ch == '.' {
                        num_str.push(ch);
                        chars.next();
                    } else {
                        break;
                    }
                }
                let val = num_str.parse::<f64>().map_err(|e| e.to_string())?;
                tokens.push(Token::Number(val));
            }
            other => return Err(format!("Unexpected character: {}", other)),
        }
    }
    Ok(tokens)
}

fn precedence(op: &Token) -> u8 {
    match op {
        Token::Plus | Token::Minus => 1,
        Token::Multiply | Token::Divide => 2,
        _ => 0,
    }
}

pub fn evaluate(expr: &str) -> Result<f64, String> {
    let tokens = tokenize(expr)?;
    let mut output: Vec<Token> = Vec::new();
    let mut ops: Vec<Token> = Vec::new();

    for token in tokens {
        match token {
            Token::Number(_) => output.push(token),
            Token::Plus | Token::Minus | Token::Multiply | Token::Divide => {
                while let Some(top) = ops.last() {
                    if precedence(top) >= precedence(&token) && *top != Token::LParen {
                        output.push(ops.pop().unwrap());
                    } else {
                        break;
                    }
                }
                ops.push(token);
            }
            Token::LParen => ops.push(token),
            Token::RParen => {
                let mut matched = false;
                while let Some(top) = ops.pop() {
                    if top == Token::LParen {
                        matched = true;
                        break;
                    }
                    output.push(top);
                }
                if !matched {
                    return Err("Mismatched parenthesis".to_string());
                }
            }
        }
    }

    while let Some(op) = ops.pop() {
        if op == Token::LParen || op == Token::RParen {
            return Err("Mismatched parenthesis".to_string());
        }
        output.push(op);
    }

    // Evaluate RPN
    let mut stack: Vec<f64> = Vec::new();
    for token in output {
        match token {
            Token::Number(n) => stack.push(n),
            Token::Plus => {
                let b = stack.pop().ok_or("Invalid expression")?;
                let a = stack.pop().ok_or("Invalid expression")?;
                stack.push(a + b);
            }
            Token::Minus => {
                let b = stack.pop().ok_or("Invalid expression")?;
                let a = stack.pop().ok_or("Invalid expression")?;
                stack.push(a - b);
            }
            Token::Multiply => {
                let b = stack.pop().ok_or("Invalid expression")?;
                let a = stack.pop().ok_or("Invalid expression")?;
                stack.push(a * b);
            }
            Token::Divide => {
                let b = stack.pop().ok_or("Invalid expression")?;
                let a = stack.pop().ok_or("Invalid expression")?;
                if b == 0.0 { return Err("Division by zero".to_string()); }
                stack.push(a / b);
            }
            _ => unreachable!(),
        }
    }

    stack.pop().ok_or("Empty expression".to_string())
}

fn main() {
    println!("=== 🦀 Project 004: CLI Calculator ===");
    let expressions = [
        "3 + 5 * 2",
        "(10 + 20) / (4 - 2)",
        "100 - 25 * 3 + 12 / 4",
    ];

    for expr in expressions {
        match evaluate(expr) {
            Ok(res) => println!("{} = {}", expr, res),
            Err(e) => println!("Error evaluating '{}': {}", expr, e),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_calc_precedence() {
        assert_eq!(evaluate("2 + 3 * 4").unwrap(), 14.0);
        assert_eq!(evaluate("(2 + 3) * 4").unwrap(), 20.0);
        assert_eq!(evaluate("10 / 2 - 3").unwrap(), 2.0);
    }
}
'''
    },
    {
        "id": "005",
        "dir_name": "005_todo_cli",
        "name": "todo_cli",
        "title": "To-Do List CLI Manager",
        "level": "Simple",
        "category": "Data Management & CRUD",
        "description": "In-memory task organizer with priority levels, status transitions, formatted listing, and filtering.",
        "concepts": ["Structs & Enums", "CRUD State Operations", "Display Trait Custom Formatting", "Vector Mutability"],
        "code": r'''//! Project 005: To-Do CLI Manager
//! Demonstrates state management, enum priorities, and filtered listings.

use std::fmt;

#[derive(Debug, PartialEq, Clone, Copy)]
pub enum Priority {
    Low,
    Medium,
    High,
}

#[derive(Debug, Clone)]
pub struct Task {
    pub id: usize,
    pub title: String,
    pub completed: bool,
    pub priority: Priority,
}

pub struct TodoList {
    tasks: Vec<Task>,
    next_id: usize,
}

impl TodoList {
    pub fn new() -> Self {
        Self { tasks: Vec::new(), next_id: 1 }
    }

    pub fn add(&mut self, title: &str, priority: Priority) -> usize {
        let id = self.next_id;
        self.next_id += 1;
        self.tasks.push(Task {
            id,
            title: title.to_string(),
            completed: false,
            priority,
        });
        id
    }

    pub fn complete(&mut self, id: usize) -> bool {
        if let Some(task) = self.tasks.iter_mut().find(|t| t.id == id) {
            task.completed = true;
            true
        } else {
            false
        }
    }

    pub fn remove(&mut self, id: usize) -> bool {
        let initial_len = self.tasks.len();
        self.tasks.retain(|t| t.id != id);
        self.tasks.len() < initial_len
    }

    pub fn filter_by_priority(&self, priority: Priority) -> Vec<&Task> {
        self.tasks.iter().filter(|t| t.priority == priority).collect()
    }
}

impl fmt::Display for TodoList {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        writeln!(f, "{:<4} {:<6} {:<8} {}", "ID", "STATUS", "PRIORITY", "TITLE")?;
        writeln!(f, "{}", "-".repeat(45))?;
        for task in &self.tasks {
            let status = if task.completed { "[x]" } else { "[ ]" };
            let prio = match task.priority {
                Priority::Low => "Low",
                Priority::Medium => "Medium",
                Priority::High => "High",
            };
            writeln!(f, "{:<4} {:<6} {:<8} {}", task.id, status, prio, task.title)?;
        }
        Ok(())
    }
}

fn main() {
    println!("=== 🦀 Project 005: To-Do CLI Manager ===");
    let mut todo = TodoList::new();
    let id1 = todo.add("Learn Rust ownership", Priority::High);
    let id2 = todo.add("Write unit tests", Priority::Medium);
    let _id3 = todo.add("Publish open source repo", Priority::Low);

    println!("Initial Task List:\n{}", todo);

    todo.complete(id1);
    println!("After Completing Task {}:\n{}", id1, todo);

    todo.remove(id2);
    println!("After Removing Task {}:\n{}", id2, todo);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_todo_crud() {
        let mut list = TodoList::new();
        let id = list.add("Write code", Priority::High);
        assert!(!list.tasks[0].completed);
        assert!(list.complete(id));
        assert!(list.tasks[0].completed);
        assert!(list.remove(id));
        assert_eq!(list.tasks.len(), 0);
    }
}
'''
    },
    {
        "id": "006",
        "dir_name": "006_palindrome_checker",
        "name": "palindrome_checker",
        "title": "Palindrome Checker",
        "level": "Simple",
        "category": "Strings & Algorithms",
        "description": "Unicode and whitespace-agnostic palindrome validator with bidirectional iterator comparison.",
        "concepts": ["String Iterators", "Double-Ended Iterators", "Unicode Char Filtering", "Complexity Analysis"],
        "code": r'''//! Project 006: Palindrome Checker
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
'''
    },
    {
        "id": "007",
        "dir_name": "007_fibonacci_generator",
        "name": "fibonacci_generator",
        "title": "Fibonacci Generator",
        "level": "Simple",
        "category": "Math & Iterators",
        "description": "Generates Fibonacci sequences via iterative, memoized, recursive, and custom infinite `Iterator` trait approaches.",
        "concepts": ["Iterator Trait Implementation", "Memoization with HashMap", "Stack vs Heap Recursion", "Infinite Streams (take)"],
        "code": r'''//! Project 007: Fibonacci Generator
//! Demonstrates implementing the Iterator trait, recursion, and memoization.

use std::collections::HashMap;

pub struct Fibonacci {
    curr: u128,
    next: u128,
}

impl Fibonacci {
    pub fn new() -> Self {
        Self { curr: 0, next: 1 }
    }
}

impl Iterator for Fibonacci {
    type Item = u128;

    fn next(&mut self) -> Option<Self::Item> {
        let current = self.curr;
        let new_next = self.curr.checked_add(self.next)?;
        self.curr = self.next;
        self.next = new_next;
        Some(current)
    }
}

pub fn fib_memo(n: u32, memo: &mut HashMap<u32, u128>) -> u128 {
    if n <= 1 {
        return n as u128;
    }
    if let Some(&val) = memo.get(&n) {
        return val;
    }
    let val = fib_memo(n - 1, memo) + fib_memo(n - 2, memo);
    memo.insert(n, val);
    val
}

fn main() {
    println!("=== 🦀 Project 007: Fibonacci Generator ===");
    println!("First 15 Fibonacci numbers using custom Iterator:");
    let fib = Fibonacci::new();
    let seq: Vec<u128> = fib.take(15).collect();
    println!("{:?}", seq);

    let mut memo = HashMap::new();
    let n = 30;
    println!("Fibonacci({}) using memoization: {}", n, fib_memo(n, &mut memo));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_fibonacci_iterator() {
        let fib = Fibonacci::new();
        let expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34];
        let actual: Vec<u128> = fib.take(10).collect();
        assert_eq!(actual, expected);
    }
}
'''
    },
    {
        "id": "008",
        "dir_name": "008_prime_sieve",
        "name": "prime_sieve",
        "title": "Prime Sieve & Factorizer",
        "level": "Simple",
        "category": "Algorithms & Math",
        "description": "Sieve of Eratosthenes prime generator and prime factorization engine with performance metrics.",
        "concepts": ["Boolean Bit Vectors", "Vector Indexing", "Prime Factorization", "Algorithmic Complexity"],
        "code": r'''//! Project 008: Prime Sieve & Factorizer
//! Demonstrates Sieve of Eratosthenes and prime factorization.

pub fn sieve_of_eratosthenes(limit: usize) -> Vec<usize> {
    if limit < 2 {
        return Vec::new();
    }
    let mut is_prime = vec![true; limit + 1];
    is_prime[0] = false;
    is_prime[1] = false;

    let p_limit = (limit as f64).sqrt() as usize;
    for p in 2..=p_limit {
        if is_prime[p] {
            let mut multiple = p * p;
            while multiple <= limit {
                is_prime[multiple] = false;
                multiple += p;
            }
        }
    }

    is_prime
        .iter()
        .enumerate()
        .filter_map(|(idx, &prime)| if prime { Some(idx) } else { None })
        .collect()
}

pub fn prime_factors(mut n: u64) -> Vec<u64> {
    let mut factors = Vec::new();
    while n % 2 == 0 {
        factors.push(2);
        n /= 2;
    }
    let mut d = 3;
    while d * d <= n {
        while n % d == 0 {
            factors.push(d);
            n /= d;
        }
        d += 2;
    }
    if n > 1 {
        factors.push(n);
    }
    factors
}

fn main() {
    println!("=== 🦀 Project 008: Prime Sieve & Factorizer ===");
    let primes_up_to_50 = sieve_of_eratosthenes(50);
    println!("Primes up to 50: {:?}", primes_up_to_50);

    let num = 840;
    println!("Prime factors of {}: {:?}", num, prime_factors(num));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sieve() {
        let primes = sieve_of_eratosthenes(30);
        assert_eq!(primes, vec![2, 3, 5, 7, 11, 13, 17, 19, 23, 29]);
    }

    #[test]
    fn test_factors() {
        assert_eq!(prime_factors(840), vec![2, 2, 2, 3, 5, 7]);
    }
}
'''
    },
    {
        "id": "009",
        "dir_name": "009_caesar_cipher",
        "name": "caesar_cipher",
        "title": "Caesar Cipher Tool",
        "level": "Simple",
        "category": "Cryptography & Strings",
        "description": "Symmetric shift cipher encryptor and decryptor supporting arbitrary positive and negative key shifts.",
        "concepts": ["Char Manipulation & Casting", "Modulo Arithmetic", "Symmetric Ciphers", "Boundary Handling"],
        "code": r'''//! Project 009: Caesar Cipher Tool
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
'''
    },
    {
        "id": "010",
        "dir_name": "010_matrix_operations",
        "name": "matrix_operations",
        "title": "2D Matrix Operations",
        "level": "Simple",
        "category": "Linear Algebra",
        "description": "Matrix data structure with addition, subtraction, scalar scaling, transposition, and dot-product multiplication.",
        "concepts": ["2D Vectors", "Operator Overloading", "Dimension Validation", "Linear Algebra"],
        "code": r'''//! Project 010: 2D Matrix Operations
//! Demonstrates matrix representations, validations, and matrix multiplication.

use std::fmt;

#[derive(Debug, Clone, PartialEq)]
pub struct Matrix {
    pub rows: usize,
    pub cols: usize,
    data: Vec<Vec<f64>>,
}

impl Matrix {
    pub fn new(data: Vec<Vec<f64>>) -> Result<Self, String> {
        let rows = data.len();
        if rows == 0 {
            return Err("Matrix must have at least one row".to_string());
        }
        let cols = data[0].len();
        if cols == 0 || !data.iter().all(|r| r.len() == cols) {
            return Err("All rows must have the same non-zero length".to_string());
        }
        Ok(Self { rows, cols, data })
    }

    pub fn transpose(&self) -> Self {
        let mut t = vec![vec![0.0; self.rows]; self.cols];
        for r in 0..self.rows {
            for c in 0..self.cols {
                t[c][r] = self.data[r][c];
            }
        }
        Self { rows: self.cols, cols: self.rows, data: t }
    }

    pub fn multiply(&self, other: &Self) -> Result<Self, String> {
        if self.cols != other.rows {
            return Err(format!("Dimension mismatch: {}x{} vs {}x{}", self.rows, self.cols, other.rows, other.cols));
        }
        let mut result = vec![vec![0.0; other.cols]; self.rows];
        for i in 0..self.rows {
            for j in 0..other.cols {
                let mut sum = 0.0;
                for k in 0..self.cols {
                    sum += self.data[i][k] * other.data[k][j];
                }
                result[i][j] = sum;
            }
        }
        Ok(Self { rows: self.rows, cols: other.cols, data: result })
    }
}

impl fmt::Display for Matrix {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        for row in &self.data {
            write!(f, "[ ")?;
            for val in row {
                write!(f, "{:6.2} ", val)?;
            }
            writeln!(f, "]")?;
        }
        Ok(())
    }
}

fn main() {
    println!("=== 🦀 Project 010: 2D Matrix Operations ===");
    let m1 = Matrix::new(vec![
        vec![1.0, 2.0],
        vec![3.0, 4.0],
    ]).unwrap();

    let m2 = Matrix::new(vec![
        vec![2.0, 0.0],
        vec![1.0, 2.0],
    ]).unwrap();

    println!("Matrix A:\n{}", m1);
    println!("Matrix B:\n{}", m2);
    let prod = m1.multiply(&m2).unwrap();
    println!("A x B:\n{}", prod);
    println!("Transpose of A:\n{}", m1.transpose());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_multiply() {
        let a = Matrix::new(vec![vec![1.0, 2.0], vec![3.0, 4.0]]).unwrap();
        let b = Matrix::new(vec![vec![2.0, 0.0], vec![1.0, 2.0]]).unwrap();
        let c = a.multiply(&b).unwrap();
        assert_eq!(c.data, vec![vec![4.0, 4.0], vec![10.0, 8.0]]);
    }
}
'''
    },
    {
        "id": "011",
        "dir_name": "011_unit_converter",
        "name": "unit_converter",
        "title": "Physical Unit Converter",
        "level": "Simple",
        "category": "Physics & Traits",
        "description": "Trait-based physical dimension unit converter for distance, mass, and volume conversions.",
        "concepts": ["Trait Bounds", "Associated Types", "Unit Standardization", "Floating Point Conversions"],
        "code": r'''//! Project 011: Physical Unit Converter
//! Demonstrates trait-based conversions and dimension unit modeling.

#[derive(Debug, PartialEq, Clone, Copy)]
pub enum LengthUnit {
    Meter,
    Kilometer,
    Mile,
    Foot,
    Inch,
}

impl LengthUnit {
    fn to_meters(self, val: f64) -> f64 {
        match self {
            LengthUnit::Meter => val,
            LengthUnit::Kilometer => val * 1000.0,
            LengthUnit::Mile => val * 1609.344,
            LengthUnit::Foot => val * 0.3048,
            LengthUnit::Inch => val * 0.0254,
        }
    }

    fn from_meters(self, meters: f64) -> f64 {
        match self {
            LengthUnit::Meter => meters,
            LengthUnit::Kilometer => meters / 1000.0,
            LengthUnit::Mile => meters / 1609.344,
            LengthUnit::Foot => meters / 0.3048,
            LengthUnit::Inch => meters / 0.0254,
        }
    }

    pub fn convert(from: Self, to: Self, value: f64) -> f64 {
        let meters = from.to_meters(value);
        to.from_meters(meters)
    }
}

fn main() {
    println!("=== 🦀 Project 011: Physical Unit Converter ===");
    let marathon_miles = 26.21875;
    let km = LengthUnit::convert(LengthUnit::Mile, LengthUnit::Kilometer, marathon_miles);
    let meters = LengthUnit::convert(LengthUnit::Mile, LengthUnit::Meter, marathon_miles);
    println!("{:.2} miles = {:.2} km = {:.0} meters", marathon_miles, km, meters);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_conversions() {
        let m = LengthUnit::convert(LengthUnit::Kilometer, LengthUnit::Meter, 1.0);
        assert!((m - 1000.0).abs() < 1e-4);
        let feet = LengthUnit::convert(LengthUnit::Meter, LengthUnit::Foot, 1.0);
        assert!((feet - 3.28084).abs() < 1e-3);
    }
}
'''
    },
    {
        "id": "012",
        "dir_name": "012_file_metadata_inspector",
        "name": "file_metadata_inspector",
        "title": "File Metadata Inspector",
        "level": "Simple",
        "category": "Filesystem & I/O",
        "description": "Inspects file size, permissions, file extension, and human-readable formatting of byte metrics.",
        "concepts": ["std::fs & std::path", "PathBuf and Path", "Human Byte Formatting", "Error Handling"],
        "code": r'''//! Project 012: File Metadata Inspector
//! Demonstrates filesystem inspection and human-readable byte calculations.

use std::path::Path;

pub fn format_bytes(bytes: u64) -> String {
    const KB: u64 = 1024;
    const MB: u64 = KB * 1024;
    const GB: u64 = MB * 1024;

    if bytes >= GB {
        format!("{:.2} GB", bytes as f64 / GB as f64)
    } else if bytes >= MB {
        format!("{:.2} MB", bytes as f64 / MB as f64)
    } else if bytes >= KB {
        format!("{:.2} KB", bytes as f64 / KB as f64)
    } else {
        format!("{} B", bytes)
    }
}

pub struct FileInfo {
    pub file_name: String,
    pub extension: String,
    pub simulated_size: u64,
}

impl FileInfo {
    pub fn inspect_path(p: &Path, simulated_size: u64) -> Self {
        Self {
            file_name: p.file_name().and_then(|n| n.to_str()).unwrap_or("unknown").to_string(),
            extension: p.extension().and_then(|e| e.to_str()).unwrap_or("none").to_string(),
            simulated_size,
        }
    }
}

fn main() {
    println!("=== 🦀 Project 012: File Metadata Inspector ===");
    let paths = [
        ("src/main.rs", 2450),
        ("assets/archive.tar.gz", 15482390),
        ("videos/presentation.mp4", 1854923847),
    ];

    for (p, size) in paths {
        let info = FileInfo::inspect_path(Path::new(p), size);
        println!("File: {:<25} Ext: {:<5} Size: {}", info.file_name, info.extension, format_bytes(info.simulated_size));
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_format_bytes() {
        assert_eq!(format_bytes(500), "500 B");
        assert_eq!(format_bytes(1024), "1.00 KB");
        assert_eq!(format_bytes(1048576), "1.00 MB");
    }
}
'''
    },
    {
        "id": "013",
        "dir_name": "013_password_generator",
        "name": "password_generator",
        "title": "Configurable Password Generator",
        "level": "Simple",
        "category": "Security & Strings",
        "description": "Generates secure randomized passwords with configurable entropy, character set inclusions, and strength ratings.",
        "concepts": ["Pseudo-Random Sampling", "Bitmasks & Config Enums", "Shannon Entropy Estimation", "String Generation"],
        "code": r'''//! Project 013: Configurable Password Generator
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
'''
    },
    {
        "id": "014",
        "dir_name": "014_stack_and_queue",
        "name": "stack_and_queue",
        "title": "Generic Stack & Queue",
        "level": "Simple",
        "category": "Data Structures",
        "description": "Generic implementations of LIFO Stack and FIFO Queue with peak, size, capacity, and iterator capabilities.",
        "concepts": ["Generics `<T>`", "LIFO vs FIFO Semantics", "VecDeque & Vec Backings", "Unit Testing"],
        "code": r'''//! Project 014: Generic Stack & Queue
//! Demonstrates generic data structures, LIFO and FIFO access patterns.

use std::collections::VecDeque;

#[derive(Debug, Default)]
pub struct Stack<T> {
    items: Vec<T>,
}

impl<T> Stack<T> {
    pub fn new() -> Self { Self { items: Vec::new() } }
    pub fn push(&mut self, item: T) { self.items.push(item); }
    pub fn pop(&mut self) -> Option<T> { self.items.pop() }
    pub fn peek(&self) -> Option<&T> { self.items.last() }
    pub fn is_empty(&self) -> bool { self.items.is_empty() }
    pub fn len(&self) -> usize { self.items.len() }
}

#[derive(Debug, Default)]
pub struct Queue<T> {
    items: VecDeque<T>,
}

impl<T> Queue<T> {
    pub fn new() -> Self { Self { items: VecDeque::new() } }
    pub fn enqueue(&mut self, item: T) { self.items.push_back(item); }
    pub fn dequeue(&mut self) -> Option<T> { self.items.pop_front() }
    pub fn peek(&self) -> Option<&T> { self.items.front() }
    pub fn is_empty(&self) -> bool { self.items.is_empty() }
    pub fn len(&self) -> usize { self.items.len() }
}

fn main() {
    println!("=== 🦀 Project 014: Generic Stack & Queue ===");
    let mut stack = Stack::new();
    stack.push(10);
    stack.push(20);
    stack.push(30);
    println!("Stack Pop: {:?}", stack.pop());

    let mut queue = Queue::new();
    queue.enqueue("Task 1");
    queue.enqueue("Task 2");
    println!("Queue Dequeue: {:?}", queue.dequeue());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_stack_lifo() {
        let mut s = Stack::new();
        s.push(1); s.push(2);
        assert_eq!(s.pop(), Some(2));
        assert_eq!(s.pop(), Some(1));
    }

    #[test]
    fn test_queue_fifo() {
        let mut q = Queue::new();
        q.enqueue(1); q.enqueue(2);
        assert_eq!(q.dequeue(), Some(1));
        assert_eq!(q.dequeue(), Some(2));
    }
}
'''
    },
    {
        "id": "015",
        "dir_name": "015_roman_numeral_converter",
        "name": "roman_numeral_converter",
        "title": "Roman Numeral Converter",
        "level": "Simple",
        "category": "Math & Strings",
        "description": "Bi-directional converter between standard integers (1-3999) and Roman numerals with subtractive notation.",
        "concepts": ["Pattern Matching", "Greedy Subtraction", "String Accumulation", "Validation & Parsing"],
        "code": r'''//! Project 015: Roman Numeral Converter
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
'''
    },
    {
        "id": "016",
        "dir_name": "016_json_field_extractor",
        "name": "json_field_extractor",
        "title": "Minimal JSON Field Extractor",
        "level": "Simple",
        "category": "Parsing & Text",
        "description": "Zero-dependency lightweight JSON string lexer and key-value extractor for flat objects.",
        "concepts": ["Handwritten Lexer", "String Slicing & Parsing", "HashMap Key-Value Storage", "Safe Option Handling"],
        "code": r'''//! Project 016: Minimal JSON Field Extractor
//! Demonstrates zero-dependency JSON string lexing and property extraction.

use std::collections::HashMap;

#[derive(Debug, PartialEq, Clone)]
pub enum JsonValue {
    String(String),
    Number(f64),
    Bool(bool),
    Null,
}

pub fn parse_flat_json(input: &str) -> Result<HashMap<String, JsonValue>, String> {
    let mut map = HashMap::new();
    let trimmed = input.trim();
    if !trimmed.starts_with('{') || !trimmed.ends_with('}') {
        return Err("Input must be enclosed in braces {}".to_string());
    }

    let inner = &trimmed[1..trimmed.len() - 1].trim();
    if inner.is_empty() {
        return Ok(map);
    }

    for pair in inner.split(',') {
        let parts: Vec<&str> = pair.splitn(2, ':').collect();
        if parts.len() != 2 {
            return Err(format!("Invalid key-value pair: {}", pair));
        }
        let key = parts[0].trim().trim_matches('"').to_string();
        let val_str = parts[1].trim();

        let val = if val_str.starts_with('"') && val_str.ends_with('"') {
            JsonValue::String(val_str[1..val_str.len() - 1].to_string())
        } else if val_str == "true" {
            JsonValue::Bool(true)
        } else if val_str == "false" {
            JsonValue::Bool(false)
        } else if val_str == "null" {
            JsonValue::Null
        } else if let Ok(num) = val_str.parse::<f64>() {
            JsonValue::Number(num)
        } else {
            return Err(format!("Unrecognized value format: {}", val_str));
        };

        map.insert(key, val);
    }

    Ok(map)
}

fn main() {
    println!("=== 🦀 Project 016: Minimal JSON Field Extractor ===");
    let raw = r#"{"name": "Rust", "version": 2021, "awesome": true, "legacy": null}"#;
    let parsed = parse_flat_json(raw).unwrap();
    for (k, v) in parsed {
        println!("{:<10} => {:?}", k, v);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_json_parse() {
        let json = r#"{"title": "Book", "pages": 320, "published": true}"#;
        let map = parse_flat_json(json).unwrap();
        assert_eq!(map.get("title"), Some(&JsonValue::String("Book".to_string())));
        assert_eq!(map.get("pages"), Some(&JsonValue::Number(320.0)));
        assert_eq!(map.get("published"), Some(&JsonValue::Bool(true)));
    }
}
'''
    },
    {
        "id": "017",
        "dir_name": "017_csv_parser",
        "name": "csv_parser",
        "title": "Robust CSV Table Parser",
        "level": "Simple",
        "category": "File Formats & Parsing",
        "description": "Parses CSV text adhering to RFC 4180 rules, correctly managing embedded commas, escape quotes, and line breaks.",
        "concepts": ["State Machine Parsing", "Slice Chunking", "RFC 4180 Specification", "Vector of Records"],
        "code": r'''//! Project 017: Robust CSV Table Parser
//! Demonstrates state-machine based CSV parsing handling escaped quotes and commas.

#[derive(Debug, PartialEq, Clone)]
pub struct CsvTable {
    pub headers: Vec<String>,
    pub rows: Vec<Vec<String>>,
}

pub fn parse_csv_line(line: &str) -> Vec<String> {
    let mut fields = Vec::new();
    let mut field = String::new();
    let mut in_quotes = false;
    let mut chars = line.chars().peekable();

    while let Some(c) = chars.next() {
        match c {
            '"' => {
                if in_quotes && chars.peek() == Some(&'"') {
                    field.push('"');
                    chars.next();
                } else {
                    in_quotes = !in_quotes;
                }
            }
            ',' if !in_quotes => {
                fields.push(field.trim().to_string());
                field = String::new();
            }
            _ => field.push(c),
        }
    }
    fields.push(field.trim().to_string());
    fields
}

pub fn parse_csv(content: &str) -> Option<CsvTable> {
    let mut lines = content.lines().filter(|l| !l.trim().is_empty());
    let header_line = lines.next()?;
    let headers = parse_csv_line(header_line);
    let mut rows = Vec::new();

    for line in lines {
        rows.push(parse_csv_line(line));
    }

    Some(CsvTable { headers, rows })
}

fn main() {
    println!("=== 🦀 Project 017: Robust CSV Table Parser ===");
    let sample = "id,name,role\n1,\"Doe, John\",Admin\n2,Jane Smith,Developer\n3,\"Special \"\"Alias\"\"\",User";
    let table = parse_csv(sample).unwrap();
    println!("Headers: {:?}", table.headers);
    for row in table.rows {
        println!("Row: {:?}", row);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_csv_quoting() {
        let line = r#"10,"Hello, World",42"#;
        let parsed = parse_csv_line(line);
        assert_eq!(parsed, vec!["10", "Hello, World", "42"]);
    }
}
'''
    },
    {
        "id": "018",
        "dir_name": "018_luhn_algorithm",
        "name": "luhn_algorithm",
        "title": "Luhn Algorithm Credit Card Validator",
        "level": "Simple",
        "category": "Algorithms & Validation",
        "description": "Calculates and verifies checksum digits according to the Luhn (Mod 10) formula used in payment cards.",
        "concepts": ["Iterator Reversal", "Char Digit Extraction", "Checksum Calculation", "Unit Testing"],
        "code": r'''//! Project 018: Luhn Algorithm Validator
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
'''
    },
    {
        "id": "019",
        "dir_name": "019_rock_paper_scissors",
        "name": "rock_paper_scissors",
        "title": "Rock-Paper-Scissors Simulator",
        "level": "Simple",
        "category": "Games & Enums",
        "description": "Rock, Paper, Scissors, Lizard, Spock game logic with round scoring and strategy evaluation.",
        "concepts": ["Enums with Comparisons", "Match Expressions", "Round Accounting", "Custom Display"],
        "code": r'''//! Project 019: Rock-Paper-Scissors Simulator
//! Demonstrates custom enum matching, outcomes, and scoring tally.

#[derive(Debug, PartialEq, Clone, Copy)]
pub enum Move {
    Rock,
    Paper,
    Scissors,
}

#[derive(Debug, PartialEq, Clone, Copy)]
pub enum Outcome {
    Win,
    Lose,
    Draw,
}

impl Move {
    pub fn play(self, opponent: Self) -> Outcome {
        match (self, opponent) {
            (Move::Rock, Move::Scissors)
            | (Move::Paper, Move::Rock)
            | (Move::Scissors, Move::Paper) => Outcome::Win,

            (Move::Rock, Move::Paper)
            | (Move::Paper, Move::Scissors)
            | (Move::Scissors, Move::Rock) => Outcome::Lose,

            _ => Outcome::Draw,
        }
    }
}

fn main() {
    println!("=== 🦀 Project 019: Rock-Paper-Scissors Simulator ===");
    let rounds = [
        (Move::Rock, Move::Scissors),
        (Move::Paper, Move::Paper),
        (Move::Scissors, Move::Rock),
    ];

    for (p1, p2) in rounds {
        let res = p1.play(p2);
        println!("{:?} vs {:?} -> {:?}", p1, p2, res);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_game_outcomes() {
        assert_eq!(Move::Rock.play(Move::Scissors), Outcome::Win);
        assert_eq!(Move::Scissors.play(Move::Rock), Outcome::Lose);
        assert_eq!(Move::Paper.play(Move::Paper), Outcome::Draw);
    }
}
'''
    },
    {
        "id": "020",
        "dir_name": "020_binary_search_tree",
        "name": "binary_search_tree",
        "title": "Binary Search Tree",
        "level": "Simple",
        "category": "Trees & Algorithms",
        "description": "Recursive Binary Search Tree with node insertion, contains lookup, depth measurement, and in-order traversal.",
        "concepts": ["Box<Option<Node>>", "Recursive Data Types", "In-Order Traversal", "Ord Trait Bounds"],
        "code": r'''//! Project 020: Binary Search Tree
//! Demonstrates recursive boxed node structures and tree traversals.

#[derive(Debug)]
pub struct TreeNode<T: Ord> {
    pub val: T,
    pub left: Option<Box<TreeNode<T>>>,
    pub right: Option<Box<TreeNode<T>>>,
}

#[derive(Debug, Default)]
pub struct BinarySearchTree<T: Ord> {
    root: Option<Box<TreeNode<T>>>,
}

impl<T: Ord + Copy> BinarySearchTree<T> {
    pub fn new() -> Self {
        Self { root: None }
    }

    pub fn insert(&mut self, val: T) {
        Self::insert_rec(&mut self.root, val);
    }

    fn insert_rec(node: &mut Option<Box<TreeNode<T>>>, val: T) {
        match node {
            None => {
                *node = Some(Box::new(TreeNode { val, left: None, right: None }));
            }
            Some(ref mut n) => {
                if val < n.val {
                    Self::insert_rec(&mut n.left, val);
                } else if val > n.val {
                    Self::insert_rec(&mut n.right, val);
                }
            }
        }
    }

    pub fn contains(&self, val: T) -> bool {
        let mut curr = &self.root;
        while let Some(n) = curr {
            if val == n.val {
                return true;
            } else if val < n.val {
                curr = &n.left;
            } else {
                curr = &n.right;
            }
        }
        false
    }

    pub fn in_order(&self) -> Vec<T> {
        let mut acc = Vec::new();
        Self::in_order_rec(&self.root, &mut acc);
        acc
    }

    fn in_order_rec(node: &Option<Box<TreeNode<T>>>, acc: &mut Vec<T>) {
        if let Some(n) = node {
            Self::in_order_rec(&n.left, acc);
            acc.push(n.val);
            Self::in_order_rec(&n.right, acc);
        }
    }
}

fn main() {
    println!("=== 🦀 Project 020: Binary Search Tree ===");
    let mut bst = BinarySearchTree::new();
    for v in [50, 30, 70, 20, 40, 60, 80] {
        bst.insert(v);
    }
    println!("In-order traversal: {:?}", bst.in_order());
    println!("Contains 40: {}", bst.contains(40));
    println!("Contains 99: {}", bst.contains(99));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bst() {
        let mut tree = BinarySearchTree::new();
        tree.insert(5);
        tree.insert(3);
        tree.insert(8);
        assert!(tree.contains(3));
        assert!(!tree.contains(10));
        assert_eq!(tree.in_order(), vec![3, 5, 8]);
    }
}
'''
    },
    {
        "id": "021",
        "dir_name": "021_run_length_encoding",
        "name": "run_length_encoding",
        "title": "Run-Length Encoding (RLE)",
        "level": "Simple",
        "category": "Compression & Strings",
        "description": "Lossless data compression algorithm encoding repeated consecutive values into (count, char) tokens.",
        "concepts": ["Char Peakable Iteration", "Compression Ratio Metric", "String Reassembly", "Lossless Roundtrips"],
        "code": r'''//! Project 021: Run-Length Encoding (RLE)
//! Demonstrates lossless stream compression and decompression.

pub fn encode_rle(input: &str) -> String {
    if input.is_empty() {
        return String::new();
    }
    let mut encoded = String::new();
    let mut chars = input.chars().peekable();

    while let Some(current) = chars.next() {
        let mut count = 1;
        while chars.peek() == Some(&current) {
            count += 1;
            chars.next();
        }
        encoded.push_str(&format!("{}{}", count, current));
    }
    encoded
}

pub fn decode_rle(encoded: &str) -> Result<String, &'static str> {
    let mut decoded = String::new();
    let mut count_str = String::new();

    for c in encoded.chars() {
        if c.is_digit(10) {
            count_str.push(c);
        } else {
            let count: usize = count_str.parse().map_err(|_| "Malformed RLE number")?;
            count_str.clear();
            for _ in 0..count {
                decoded.push(c);
            }
        }
    }
    Ok(decoded)
}

fn main() {
    println!("=== 🦀 Project 021: Run-Length Encoding ===");
    let original = "WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWB";
    let encoded = encode_rle(original);
    let decoded = decode_rle(&encoded).unwrap();

    println!("Original:  {} (len: {})", original, original.len());
    println!("Encoded:   {} (len: {})", encoded, encoded.len());
    println!("Decoded:   {}", decoded);
    assert_eq!(original, decoded);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_rle_roundtrip() {
        let s = "AAAAABBBCCDAA";
        let enc = encode_rle(s);
        assert_eq!(enc, "5A3B2C1D2A");
        assert_eq!(decode_rle(&enc).unwrap(), s);
    }
}
'''
    },
    {
        "id": "022",
        "dir_name": "022_sorting_algorithms",
        "name": "sorting_algorithms",
        "title": "Classic Sorting Suite",
        "level": "Simple",
        "category": "Algorithms",
        "description": "Collection of standard sorting algorithms: Bubble Sort, Selection Sort, Insertion Sort, Merge Sort, and Quick Sort.",
        "concepts": ["In-Place Mutation", "Divide and Conquer", "Generic Slices `&mut [T]`", "Ord Bounds"],
        "code": r'''//! Project 022: Classic Sorting Suite
//! Demonstrates Bubble, Selection, Insertion, Merge, and Quick Sort on generic slices.

pub fn bubble_sort<T: Ord>(arr: &mut [T]) {
    let n = arr.len();
    for i in 0..n {
        for j in 0..n.saturating_sub(i + 1) {
            if arr[j] > arr[j + 1] {
                arr.swap(j, j + 1);
            }
        }
    }
}

pub fn insertion_sort<T: Ord + Copy>(arr: &mut [T]) {
    for i in 1..arr.len() {
        let key = arr[i];
        let mut j = i;
        while j > 0 && arr[j - 1] > key {
            arr[j] = arr[j - 1];
            j -= 1;
        }
        arr[j] = key;
    }
}

pub fn quick_sort<T: Ord + Copy>(arr: &mut [T]) {
    if arr.len() <= 1 { return; }
    let pivot = arr[arr.len() / 2];
    let mut left = 0;
    let mut right = arr.len() - 1;

    while left <= right {
        while arr[left] < pivot { left += 1; }
        while arr[right] > pivot {
            if right == 0 { break; }
            right -= 1;
        }
        if left <= right {
            arr.swap(left, right);
            left += 1;
            if right > 0 { right -= 1; }
        }
    }

    if right > 0 { quick_sort(&mut arr[0..=right]); }
    if left < arr.len() { quick_sort(&mut arr[left..]); }
}

fn main() {
    println!("=== 🦀 Project 022: Classic Sorting Suite ===");
    let mut data1 = [64, 34, 25, 12, 22, 11, 90];
    bubble_sort(&mut data1);
    println!("Bubble sorted:    {:?}", data1);

    let mut data2 = [64, 34, 25, 12, 22, 11, 90];
    insertion_sort(&mut data2);
    println!("Insertion sorted: {:?}", data2);

    let mut data3 = [64, 34, 25, 12, 22, 11, 90];
    quick_sort(&mut data3);
    println!("Quick sorted:     {:?}", data3);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sorts() {
        let mut v = vec![5, 2, 8, 1, 9];
        quick_sort(&mut v);
        assert_eq!(v, vec![1, 2, 5, 8, 9]);
    }
}
'''
    },
    {
        "id": "023",
        "dir_name": "023_vector_statistics",
        "name": "vector_statistics",
        "title": "Vector Statistical Calculator",
        "level": "Simple",
        "category": "Math & Statistics",
        "description": "Calculates descriptive statistics: mean, median, mode, sample variance, standard deviation, and range.",
        "concepts": ["Statistical Aggregations", "Sorting & Quantiles", "HashMap Mode Tally", "Float Casts"],
        "code": r'''//! Project 023: Vector Statistical Calculator
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
'''
    },
    {
        "id": "024",
        "dir_name": "024_morse_code_translator",
        "name": "morse_code_translator",
        "title": "Morse Code Translator",
        "level": "Simple",
        "category": "Strings & Encodings",
        "description": "Bi-directional translator between text and International Morse Code with word-delimiter slash formatting.",
        "concepts": ["Lookup Table Mapping", "Splitting & Joining", "Bidirectional Dictionaries", "Char Mapping"],
        "code": r'''//! Project 024: Morse Code Translator
//! Demonstrates table lookups and bidirectional string translations.

const MORSE_TABLE: &[(char, &str)] = &[
    ('A', ".-"), ('B', "-..."), ('C', "-.-."), ('D', "-.."), ('E', "."),
    ('F', "..-."), ('G', "--."), ('H', "...."), ('I', ".."), ('J', ".---"),
    ('K', "-.-"), ('L', ".-.."), ('M', "--"), ('N', "-."), ('O', "---"),
    ('P', ".--."), ('Q', "--.-"), ('R', ".-."), ('S', "..."), ('T', "-"),
    ('U', "..-"), ('V', "...-"), ('W', ".--"), ('X', "-..-"), ('Y', "-.--"),
    ('Z', "--.."), ('0', "-----"), ('1', ".----"), ('2', "..---"), ('3', "...--"),
    ('4', "....-"), ('5', "....."), ('6', "-...."), ('7', "--..."), ('8', "---.."),
    ('9', "----."),
];

pub fn text_to_morse(text: &str) -> String {
    let mut words = Vec::new();
    for word in text.split_whitespace() {
        let mut letters = Vec::new();
        for ch in word.to_uppercase().chars() {
            if let Some(&(_, code)) = MORSE_TABLE.iter().find(|&&(c, _)| c == ch) {
                letters.push(code);
            }
        }
        words.push(letters.join(" "));
    }
    words.join(" / ")
}

pub fn morse_to_text(morse: &str) -> String {
    let mut words = Vec::new();
    for word_code in morse.split('/') {
        let mut letters = String::new();
        for code in word_code.split_whitespace() {
            if let Some(&(ch, _)) = MORSE_TABLE.iter().find(|&&(_, c)| c == code) {
                letters.push(ch);
            }
        }
        words.push(letters);
    }
    words.join(" ")
}

fn main() {
    println!("=== 🦀 Project 024: Morse Code Translator ===");
    let message = "SOS HELLO RUST";
    let morse = text_to_morse(message);
    let recovered = morse_to_text(&morse);

    println!("Plain: {}", message);
    println!("Morse: {}", morse);
    println!("Back:  {}", recovered);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_morse() {
        let enc = text_to_morse("SOS");
        assert_eq!(enc, "... --- ...");
        assert_eq!(morse_to_text("... --- ..."), "SOS");
    }
}
'''
    },
    {
        "id": "025",
        "dir_name": "025_ansi_color_formatter",
        "name": "ansi_color_formatter",
        "title": "ANSI Terminal Styler",
        "level": "Simple",
        "category": "CLI & Terminal",
        "description": "ANSI escape code wrapper providing colorful bold, underlined, and foreground/background styled terminal text.",
        "concepts": ["ANSI Escape Sequences", "Method Chaining / Builder Pattern", "Display Trait", "Terminal UX"],
        "code": r'''//! Project 025: ANSI Terminal Styler
//! Demonstrates ANSI escape sequences and method chaining builder styles.

#[derive(Debug, Clone, Copy)]
pub enum Color {
    Black = 30,
    Red = 31,
    Green = 32,
    Yellow = 33,
    Blue = 34,
    Magenta = 35,
    Cyan = 36,
    White = 37,
}

pub struct StyledText<'a> {
    text: &'a str,
    fg: Option<Color>,
    bold: bool,
    underline: bool,
}

impl<'a> StyledText<'a> {
    pub fn new(text: &'a str) -> Self {
        Self { text, fg: None, bold: false, underline: false }
    }

    pub fn color(mut self, color: Color) -> Self {
        self.fg = Some(color);
        self
    }

    pub fn bold(mut self) -> Self {
        self.bold = true;
        self
    }

    pub fn underline(mut self) -> Self {
        self.underline = true;
        self
    }

    pub fn render(&self) -> String {
        let mut codes = Vec::new();
        if self.bold { codes.push("1"); }
        if self.underline { codes.push("4"); }
        let fg_code;
        if let Some(c) = self.fg {
            fg_code = (c as u8).to_string();
            codes.push(&fg_code);
        }

        if codes.is_empty() {
            self.text.to_string()
        } else {
            format!("\x1b[{}m{}\x1b[0m", codes.join(";"), self.text)
        }
    }
}

fn main() {
    println!("=== 🦀 Project 025: ANSI Terminal Styler ===");
    println!("{}", StyledText::new("Success! Operation completed.").color(Color::Green).bold().render());
    println!("{}", StyledText::new("Warning: High memory usage.").color(Color::Yellow).render());
    println!("{}", StyledText::new("Error: Connection refused.").color(Color::Red).bold().underline().render());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ansi_render() {
        let styled = StyledText::new("Hello").color(Color::Red).bold().render();
        assert!(styled.contains("\x1b[1;31mHello\x1b[0m"));
    }
}
'''
    }
]
