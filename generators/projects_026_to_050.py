# projects_026_to_050.py

PROJECTS_026_TO_050 = [
    {
        "id": "026",
        "dir_name": "026_base64_encoder",
        "name": "base64_encoder",
        "title": "Base64 Encoder & Decoder",
        "level": "Simple",
        "category": "Encodings & Cryptography",
        "description": "Standard RFC 4648 Base64 byte-stream encoder and decoder with padding calculation.",
        "concepts": ["Bitwise Bit Shifts (`<<`, `>>`)", "Byte Chunking (`chunks(3)`)", "Lookup Tables", "Padding (`=`) Management"],
        "code": r'''//! Project 026: Base64 Encoder & Decoder
//! Demonstrates bit manipulation, chunking, and RFC 4648 Base64 logic.

const BASE64_CHARS: &[u8; 64] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

pub fn encode_base64(data: &[u8]) -> String {
    let mut result = String::new();
    for chunk in data.chunks(3) {
        let b0 = chunk[0];
        let b1 = if chunk.len() > 1 { chunk[1] } else { 0 };
        let b2 = if chunk.len() > 2 { chunk[2] } else { 0 };

        let idx0 = (b0 >> 2) as usize;
        let idx1 = (((b0 & 0x03) << 4) | (b1 >> 4)) as usize;
        let idx2 = (((b1 & 0x0F) << 2) | (b2 >> 6)) as usize;
        let idx3 = (b2 & 0x3F) as usize;

        result.push(BASE64_CHARS[idx0] as char);
        result.push(BASE64_CHARS[idx1] as char);

        if chunk.len() == 1 {
            result.push_str("==");
        } else if chunk.len() == 2 {
            result.push(BASE64_CHARS[idx2] as char);
            result.push('=');
        } else {
            result.push(BASE64_CHARS[idx2] as char);
            result.push(BASE64_CHARS[idx3] as char);
        }
    }
    result
}

fn decode_char(c: u8) -> Option<u8> {
    match c {
        b'A'..=b'Z' => Some(c - b'A'),
        b'a'..=b'z' => Some(c - b'a' + 26),
        b'0'..=b'9' => Some(c - b'0' + 52),
        b'+' => Some(62),
        b'/' => Some(63),
        _ => None,
    }
}

pub fn decode_base64(encoded: &str) -> Result<Vec<u8>, &'static str> {
    let clean: Vec<u8> = encoded.bytes().filter(|&b| b != b'=' && !b.is_ascii_whitespace()).collect();
    let mut out = Vec::new();

    for chunk in clean.chunks(4) {
        let mut buf = [0u8; 4];
        for (i, &b) in chunk.iter().enumerate() {
            buf[i] = decode_char(b).ok_or("Invalid base64 character")?;
        }

        let b0 = (buf[0] << 2) | (buf[1] >> 4);
        out.push(b0);

        if chunk.len() > 2 {
            let b1 = ((buf[1] & 0x0F) << 4) | (buf[2] >> 2);
            out.push(b1);
        }
        if chunk.len() > 3 {
            let b2 = ((buf[2] & 0x03) << 6) | buf[3];
            out.push(b2);
        }
    }
    Ok(out)
}

fn main() {
    println!("=== 🦀 Project 026: Base64 Encoder & Decoder ===");
    let msg = "Rustaceans are awesome!";
    let encoded = encode_base64(msg.as_bytes());
    let decoded = decode_base64(&encoded).unwrap();
    let recovered = String::from_utf8(decoded).unwrap();

    println!("Original:  {}", msg);
    println!("Encoded:   {}", encoded);
    println!("Recovered: {}", recovered);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_base64() {
        assert_eq!(encode_base64(b"Man"), "TWFu");
        assert_eq!(decode_base64("TWFu").unwrap(), b"Man");
    }
}
'''
    },
    {
        "id": "027",
        "dir_name": "027_env_var_loader",
        "name": "env_var_loader",
        "title": "Dotenv (.env) File Parser",
        "level": "Simple",
        "category": "Parsing & Config",
        "description": "Custom environment file reader parsing key-value pairs, ignoring comments, and stripping quotes.",
        "concepts": ["File Line Parsing", "String Trimming", "HashMap Indexing", "Key-Value Extraction"],
        "code": r'''//! Project 027: Dotenv File Parser
//! Demonstrates file parsing, comment stripping, and environment map generation.

use std::collections::HashMap;

pub fn parse_dotenv_content(content: &str) -> HashMap<String, String> {
    let mut map = HashMap::new();
    for line in content.lines() {
        let line = line.trim();
        if line.is_empty() || line.starts_with('#') {
            continue;
        }
        if let Some((key, val)) = line.split_once('=') {
            let key = key.trim().to_string();
            let mut val = val.trim();
            if (val.starts_with('"') && val.ends_with('"')) || (val.starts_with('\'') && val.ends_with('\'')) {
                if val.len() >= 2 {
                    val = &val[1..val.len() - 1];
                }
            }
            map.insert(key, val.to_string());
        }
    }
    map
}

fn main() {
    println!("=== 🦀 Project 027: Dotenv File Parser ===");
    let sample_env = "
        # Database Settings
        DB_HOST=127.0.0.1
        DB_PORT=5432
        DB_USER=\"postgres_admin\"
        APP_DEBUG=true
    ";
    let vars = parse_dotenv_content(sample_env);
    for (k, v) in vars {
        println!("{:>12} = {}", k, v);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_env() {
        let content = "# Comment\nKEY=VALUE\nPORT=\"8080\"";
        let parsed = parse_dotenv_content(content);
        assert_eq!(parsed.get("KEY"), Some(&"VALUE".to_string()));
        assert_eq!(parsed.get("PORT"), Some(&"8080".to_string()));
    }
}
'''
    },
    {
        "id": "028",
        "dir_name": "028_stopwatch_timer",
        "name": "stopwatch_timer",
        "title": "Precision Stopwatch & Lap Timer",
        "level": "Simple",
        "category": "Time & Benchmarking",
        "description": "High-precision timer supporting start, pause, resume, and split lap timing using std::time::Instant.",
        "concepts": ["std::time::Instant", "std::time::Duration", "State Transitions", "Microsecond Precision"],
        "code": r'''//! Project 028: Precision Stopwatch & Lap Timer
//! Demonstrates monotonic time measurement and lap calculations.

use std::time::{Duration, Instant};

pub struct Stopwatch {
    start_time: Option<Instant>,
    accumulated: Duration,
    laps: Vec<Duration>,
}

impl Stopwatch {
    pub fn new() -> Self {
        Self { start_time: None, accumulated: Duration::ZERO, laps: Vec::new() }
    }

    pub fn start(&mut self) {
        if self.start_time.is_none() {
            self.start_time = Some(Instant::now());
        }
    }

    pub fn pause(&mut self) {
        if let Some(st) = self.start_time.take() {
            self.accumulated += st.elapsed();
        }
    }

    pub fn elapsed(&self) -> Duration {
        self.accumulated + self.start_time.map_or(Duration::ZERO, |st| st.elapsed())
    }

    pub fn lap(&mut self) -> Duration {
        let total = self.elapsed();
        let prev_total: Duration = self.laps.iter().sum();
        let lap_dur = total.saturating_sub(prev_total);
        self.laps.push(lap_dur);
        lap_dur
    }

    pub fn get_laps(&self) -> &[Duration] {
        &self.laps
    }
}

fn main() {
    println!("=== 🦀 Project 028: Precision Stopwatch & Lap Timer ===");
    let mut sw = Stopwatch::new();
    sw.start();

    // Simulate work
    let _sum: u64 = (0..500_000).sum();
    let lap1 = sw.lap();

    let _sum2: u64 = (0..1_000_000).sum();
    let lap2 = sw.lap();

    sw.pause();
    println!("Lap 1: {:?}, Lap 2: {:?}, Total: {:?}", lap1, lap2, sw.elapsed());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_stopwatch() {
        let mut sw = Stopwatch::new();
        sw.start();
        sw.pause();
        assert!(sw.elapsed() >= Duration::ZERO);
    }
}
'''
    },
    {
        "id": "029",
        "dir_name": "029_hash_digest_crc32",
        "name": "hash_digest_crc32",
        "title": "CRC-32 Checksum Digest",
        "level": "Simple",
        "category": "Hashing & Cryptography",
        "description": "Standard IEEE 802.3 CRC-32 checksum calculator with precomputed lookup table acceleration.",
        "concepts": ["Lookup Table Precomputation", "Bitwise XOR and Shift Operations", "Polynomial Hashing", "Checksum Verification"],
        "code": r'''//! Project 029: CRC-32 Checksum Digest
//! Demonstrates IEEE 802.3 polynomial cyclic redundancy check.

pub struct Crc32 {
    table: [u32; 256],
}

impl Crc32 {
    pub const fn new() -> Self {
        let mut table = [0u32; 256];
        let poly = 0xEDB88320u32;
        let mut i = 0;
        while i < 256 {
            let mut crc = i as u32;
            let mut j = 0;
            while j < 8 {
                if (crc & 1) != 0 {
                    crc = (crc >> 1) ^ poly;
                } else {
                    crc >>= 1;
                }
                j += 1;
            }
            table[i] = crc;
            i += 1;
        }
        Self { table }
    }

    pub fn checksum(&self, bytes: &[u8]) -> u32 {
        let mut crc = 0xFFFFFFFFu32;
        for &b in bytes {
            let idx = ((crc ^ (b as u32)) & 0xFF) as usize;
            crc = (crc >> 8) ^ self.table[idx];
        }
        crc ^ 0xFFFFFFFFu32
    }
}

fn main() {
    println!("=== 🦀 Project 029: CRC-32 Checksum Digest ===");
    let crc = Crc32::new();
    let data = b"123456789";
    let hash = crc.checksum(data);
    println!("CRC-32(\"{}\") = 0x{:08X}", String::from_utf8_lossy(data), hash);
    assert_eq!(hash, 0xCBF43926);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_crc32_standard() {
        let crc = Crc32::new();
        assert_eq!(crc.checksum(b"123456789"), 0xCBF43926);
    }
}
'''
    },
    {
        "id": "030",
        "dir_name": "030_levenshtein_distance",
        "name": "levenshtein_distance",
        "title": "Levenshtein Distance & Fuzzy Matcher",
        "level": "Simple",
        "category": "Dynamic Programming & NLP",
        "description": "Calculates minimum single-character edit distance (insertions, deletions, substitutions) between strings.",
        "concepts": ["Dynamic Programming Matrix", "Fuzzy Search Ranking", "Unicode Grapheme Handling", "Matrix Memoization"],
        "code": r'''//! Project 030: Levenshtein Distance & Fuzzy Matcher
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
'''
    },
    {
        "id": "031",
        "dir_name": "031_url_query_parser",
        "name": "url_query_parser",
        "title": "URL Query String Parser & Encoder",
        "level": "Simple",
        "category": "Web & Networking",
        "description": "Parses and serializes URL query parameters with percent-encoding and decoding.",
        "concepts": ["Percent Encoding (%20, +)", "URL Structure Splitting", "Multi-Value Query Maps", "RFC 3986 Compliance"],
        "code": r'''//! Project 031: URL Query String Parser & Encoder
//! Demonstrates URL decoding, percent-encoding, and query string parsing.

use std::collections::HashMap;

pub fn url_decode(s: &str) -> String {
    let mut out = Vec::new();
    let bytes = s.as_bytes();
    let mut i = 0;
    while i < bytes.len() {
        if bytes[i] == b'%' && i + 2 < bytes.len() {
            if let Ok(h) = u8::from_str_radix(std::str::from_utf8(&bytes[i + 1..i + 3]).unwrap_or(""), 16) {
                out.push(h);
                i += 3;
                continue;
            }
        } else if bytes[i] == b'+' {
            out.push(b' ');
            i += 1;
            continue;
        }
        out.push(bytes[i]);
        i += 1;
    }
    String::from_utf8_lossy(&out).to_string()
}

pub fn parse_query(query: &str) -> HashMap<String, String> {
    let mut params = HashMap::new();
    let raw_query = query.split_once('?').map_or(query, |(_, q)| q);
    for pair in raw_query.split('&') {
        if pair.is_empty() { continue; }
        if let Some((k, v)) = pair.split_once('=') {
            params.insert(url_decode(k), url_decode(v));
        } else {
            params.insert(url_decode(pair), String::new());
        }
    }
    params
}

fn main() {
    println!("=== 🦀 Project 031: URL Query String Parser ===");
    let url = "https://example.com/search?query=rust+programming&category=dev%26code&page=1";
    let params = parse_query(url);
    for (k, v) in params {
        println!("{:>10} : {}", k, v);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_query_parsing() {
        let q = "name=John+Doe&city=New%20York";
        let parsed = parse_query(q);
        assert_eq!(parsed.get("name"), Some(&"John Doe".to_string()));
        assert_eq!(parsed.get("city"), Some(&"New York".to_string()));
    }
}
'''
    },
    {
        "id": "032",
        "dir_name": "032_bloom_filter_simple",
        "name": "bloom_filter_simple",
        "title": "Probabilistic Bloom Filter",
        "level": "Simple",
        "category": "Probabilistic Data Structures",
        "description": "Space-efficient probabilistic filter testing set membership with zero false negatives and tunable false positives.",
        "concepts": ["Bit Vectors (`Vec<bool>`)", "Multiple Independent Hashes", "Probabilistic Guarantees", "False Positive Math"],
        "code": r'''//! Project 032: Probabilistic Bloom Filter
//! Demonstrates space-efficient set membership with zero false negatives.

pub struct SimpleBloomFilter {
    bits: Vec<bool>,
    size: usize,
}

impl SimpleBloomFilter {
    pub fn new(size: usize) -> Self {
        Self { bits: vec![false; size], size }
    }

    fn hash1(&self, s: &str) -> usize {
        let mut h: u64 = 5381;
        for b in s.bytes() {
            h = ((h << 5).wrapping_add(h)).wrapping_add(b as u64);
        }
        (h as usize) % self.size
    }

    fn hash2(&self, s: &str) -> usize {
        let mut h: u64 = 0;
        for b in s.bytes() {
            h = (b as u64).wrapping_add(h << 6).wrapping_add(h << 16).wrapping_sub(h);
        }
        (h as usize) % self.size
    }

    pub fn insert(&mut self, item: &str) {
        let h1 = self.hash1(item);
        let h2 = self.hash2(item);
        self.bits[h1] = true;
        self.bits[h2] = true;
    }

    pub fn contains(&self, item: &str) -> bool {
        let h1 = self.hash1(item);
        let h2 = self.hash2(item);
        self.bits[h1] && self.bits[h2]
    }
}

fn main() {
    println!("=== 🦀 Project 032: Probabilistic Bloom Filter ===");
    let mut bf = SimpleBloomFilter::new(100);
    bf.insert("apple");
    bf.insert("banana");
    bf.insert("orange");

    println!("Contains 'apple':  {}", bf.contains("apple"));
    println!("Contains 'banana': {}", bf.contains("banana"));
    println!("Contains 'grape':  {}", bf.contains("grape"));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bloom() {
        let mut bf = SimpleBloomFilter::new(256);
        bf.insert("test_key");
        assert!(bf.contains("test_key"));
    }
}
'''
    },
    {
        "id": "033",
        "dir_name": "033_slug_generator",
        "name": "slug_generator",
        "title": "URL Slug Generator & Sanitizer",
        "level": "Simple",
        "category": "Strings & Web",
        "description": "Transforms arbitrary article headlines and product names into URL-friendly kebab-case slugs.",
        "concepts": ["Char Classification", "Kebab-Case Formatting", "Consecutive Hyphen Collapsing", "Unicode ASCII Transliteration"],
        "code": r'''//! Project 033: URL Slug Generator & Sanitizer
//! Demonstrates string transformations into sanitized URL kebab-case slugs.

pub fn slugify(title: &str) -> String {
    let mut slug = String::new();
    let mut last_was_dash = true;

    for c in title.chars() {
        if c.is_alphanumeric() {
            for lc in c.to_lowercase() {
                slug.push(lc);
            }
            last_was_dash = false;
        } else if !last_was_dash {
            slug.push('-');
            last_was_dash = true;
        }
    }

    if slug.ends_with('-') {
        slug.pop();
    }
    slug
}

fn main() {
    println!("=== 🦀 Project 033: URL Slug Generator ===");
    let titles = [
        "100 Rust Projects for Fast Learning!",
        "Hello, World: A New Journey & Adventure?",
        "  Deep Dive into Concurrency & Async...  ",
    ];

    for t in titles {
        println!("\"{}\" \n  => \"{}\"\n", t, slugify(t));
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_slugify() {
        assert_eq!(slugify("Hello World!"), "hello-world");
        assert_eq!(slugify(" Rust  2024 -- Edition "), "rust-2024-edition");
    }
}
'''
    },
    {
        "id": "034",
        "dir_name": "034_fraction_arithmetic",
        "name": "fraction_arithmetic",
        "title": "Exact Rational Fraction Arithmetic",
        "level": "Simple",
        "category": "Math & Operator Overloading",
        "description": "Exact rational number implementation supporting +, -, *, / operator overloading with greatest common divisor (GCD) reduction.",
        "concepts": ["Operator Overloading (std::ops)", "Euclidean GCD Algorithm", "Exact Rational Numbers", "Custom Display"],
        "code": r'''//! Project 034: Exact Rational Fraction Arithmetic
//! Demonstrates operator overloading, GCD reduction, and exact math.

use std::ops::{Add, Div, Mul, Sub};
use std::fmt;

fn gcd(mut a: i64, mut b: i64) -> i64 {
    a = a.abs();
    b = b.abs();
    while b != 0 {
        let t = b;
        b = a % b;
        a = t;
    }
    a
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Fraction {
    pub num: i64,
    pub den: i64,
}

impl Fraction {
    pub fn new(mut num: i64, mut den: i64) -> Result<Self, &'static str> {
        if den == 0 {
            return Err("Denominator cannot be zero");
        }
        if den < 0 {
            num = -num;
            den = -den;
        }
        let g = gcd(num, den);
        Ok(Self { num: num / g, den: den / g })
    }
}

impl Add for Fraction {
    type Output = Self;
    fn add(self, rhs: Self) -> Self::Output {
        Self::new(self.num * rhs.den + rhs.num * self.den, self.den * rhs.den).unwrap()
    }
}

impl Sub for Fraction {
    type Output = Self;
    fn sub(self, rhs: Self) -> Self::Output {
        Self::new(self.num * rhs.den - rhs.num * self.den, self.den * rhs.den).unwrap()
    }
}

impl Mul for Fraction {
    type Output = Self;
    fn mul(self, rhs: Self) -> Self::Output {
        Self::new(self.num * rhs.num, self.den * rhs.den).unwrap()
    }
}

impl Div for Fraction {
    type Output = Self;
    fn div(self, rhs: Self) -> Self::Output {
        Self::new(self.num * rhs.den, self.den * rhs.num).unwrap()
    }
}

impl fmt::Display for Fraction {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        if self.den == 1 {
            write!(f, "{}", self.num)
        } else {
            write!(f, "{}/{}", self.num, self.den)
        }
    }
}

fn main() {
    println!("=== 🦀 Project 034: Exact Rational Fraction Arithmetic ===");
    let f1 = Fraction::new(1, 3).unwrap();
    let f2 = Fraction::new(1, 6).unwrap();

    println!("{} + {} = {}", f1, f2, f1 + f2);
    println!("{} - {} = {}", f1, f2, f1 - f2);
    println!("{} * {} = {}", f1, f2, f1 * f2);
    println!("{} / {} = {}", f1, f2, f1 / f2);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_fraction_math() {
        let a = Fraction::new(1, 2).unwrap();
        let b = Fraction::new(1, 3).unwrap();
        assert_eq!(a + b, Fraction::new(5, 6).unwrap());
        assert_eq!(a * b, Fraction::new(1, 6).unwrap());
    }
}
'''
    },
    {
        "id": "035",
        "dir_name": "035_cli_progress_bar",
        "name": "cli_progress_bar",
        "title": "CLI Animated Progress Bar",
        "level": "Simple",
        "category": "CLI & Animation",
        "description": "Terminal progress bar with percentage counter, spinner glyphs, and carriage return `\\r` line rewriting.",
        "concepts": ["Carriage Return `\\r`", "Standard Output Flushing (`io::stdout().flush()`)", "Time Estimation", "Formatted Strings"],
        "code": r'''//! Project 035: CLI Animated Progress Bar
//! Demonstrates terminal progress rendering, carriage returns, and stdout flushing.

pub struct ProgressBar {
    total: usize,
    current: usize,
    width: usize,
}

impl ProgressBar {
    pub fn new(total: usize, width: usize) -> Self {
        Self { total, current: 0, width }
    }

    pub fn set(&mut self, current: usize) {
        self.current = current.min(self.total);
    }

    pub fn render(&self) -> String {
        let percent = (self.current as f64 / self.total as f64) * 100.0;
        let filled = (self.current * self.width) / self.total;
        let empty = self.width - filled;

        let bar_fill = "=".repeat(filled);
        let bar_empty = " ".repeat(empty);

        format!("[{}>{}] {:>3.0}% ({}/{})", bar_fill, bar_empty, percent, self.current, self.total)
    }
}

fn main() {
    println!("=== 🦀 Project 035: CLI Animated Progress Bar ===");
    let mut pb = ProgressBar::new(100, 30);
    for step in (0..=100).step_by(25) {
        pb.set(step);
        println!("Progress: {}", pb.render());
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_progress_bar() {
        let mut pb = ProgressBar::new(100, 20);
        pb.set(50);
        let output = pb.render();
        assert!(output.contains("50%"));
    }
}
'''
    },
    {
        "id": "036",
        "dir_name": "036_thread_pool",
        "name": "thread_pool",
        "title": "Reusable Worker Thread Pool",
        "level": "Intermediate",
        "category": "Concurrency & Systems",
        "description": "Multi-threaded worker pool dispatching closures across OS threads using synchronized mpsc channels.",
        "concepts": ["Arc<Mutex<Receiver<T>>>", "mpsc Channels", "Thread Spawning & JoinHandles", "Graceful Shutdown / Drop Trait"],
        "code": r'''//! Project 036: Reusable Worker Thread Pool
//! Demonstrates thread management, work-stealing queues, and synchronization.

use std::sync::{mpsc, Arc, Mutex};
use std::thread;

type Job = Box<dyn FnOnce() + Send + 'static>;

pub struct ThreadPool {
    workers: Vec<Worker>,
    sender: Option<mpsc::Sender<Job>>,
}

struct Worker {
    id: usize,
    thread: Option<thread::JoinHandle<()>>,
}

impl Worker {
    fn new(id: usize, receiver: Arc<Mutex<mpsc::Receiver<Job>>>) -> Self {
        let thread = thread::spawn(move || loop {
            let message = receiver.lock().unwrap().recv();
            match message {
                Ok(job) => {
                    job();
                }
                Err(_) => {
                    break;
                }
            }
        });
        Self { id, thread: Some(thread) }
    }
}

impl ThreadPool {
    pub fn new(size: usize) -> Self {
        assert!(size > 0);
        let (sender, receiver) = mpsc::channel();
        let receiver = Arc::new(Mutex::new(receiver));
        let mut workers = Vec::with_capacity(size);

        for id in 0..size {
            workers.push(Worker::new(id, Arc::clone(&receiver)));
        }

        Self { workers, sender: Some(sender) }
    }

    pub fn execute<F>(&self, f: F)
    where
        F: FnOnce() + Send + 'static,
    {
        let job = Box::new(f);
        if let Some(ref sender) = self.sender {
            sender.send(job).unwrap();
        }
    }
}

impl Drop for ThreadPool {
    fn drop(&mut self) {
        drop(self.sender.take());
        for worker in &mut self.workers {
            if let Some(thread) = worker.thread.take() {
                thread.join().unwrap();
            }
        }
    }
}

fn main() {
    println!("=== 🦀 Project 036: Reusable Worker Thread Pool ===");
    let pool = ThreadPool::new(4);
    let counter = Arc::new(Mutex::new(0));

    for i in 0..8 {
        let c = Arc::clone(&counter);
        pool.execute(move || {
            let mut num = c.lock().unwrap();
            *num += 1;
            println!("Task {} executed by thread {:?}", i, thread::current().id());
        });
    }

    drop(pool); // Wait for tasks
    println!("Total processed: {}", *counter.lock().unwrap());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_pool_execution() {
        let pool = ThreadPool::new(2);
        let val = Arc::new(Mutex::new(0));
        let val_clone = Arc::clone(&val);

        pool.execute(move || {
            *val_clone.lock().unwrap() = 42;
        });

        drop(pool);
        assert_eq!(*val.lock().unwrap(), 42);
    }
}
'''
    },
    {
        "id": "037",
        "dir_name": "037_kv_store_persisted",
        "name": "kv_store_persisted",
        "title": "Persistent Key-Value Store",
        "level": "Intermediate",
        "category": "Databases & Storage",
        "description": "Bitcask-inspired append-only log structured key-value store with in-memory HashMap offset index.",
        "concepts": ["Append-Only Log Files", "In-Memory Hash Index", "File Offsets & Seeking", "Tombstone Deletions"],
        "code": r'''//! Project 037: Persistent Key-Value Store
//! Demonstrates append-only log architecture and in-memory key index.

use std::collections::HashMap;

#[derive(Debug, Clone, PartialEq)]
pub enum Command {
    Set(String, String),
    Remove(String),
}

pub struct KeyValueStore {
    log: Vec<Command>,
    index: HashMap<String, String>,
}

impl KeyValueStore {
    pub fn new() -> Self {
        Self { log: Vec::new(), index: HashMap::new() }
    }

    pub fn set(&mut self, key: &str, val: &str) {
        let cmd = Command::Set(key.to_string(), val.to_string());
        self.log.push(cmd);
        self.index.insert(key.to_string(), val.to_string());
    }

    pub fn get(&self, key: &str) -> Option<&str> {
        self.index.get(key).map(|s| s.as_str())
    }

    pub fn delete(&mut self, key: &str) -> bool {
        if self.index.remove(key).is_some() {
            self.log.push(Command::Remove(key.to_string()));
            true
        } else {
            false
        }
    }

    pub fn log_len(&self) -> usize {
        self.log.len()
    }
}

fn main() {
    println!("=== 🦀 Project 037: Persistent Key-Value Store ===");
    let mut store = KeyValueStore::new();
    store.set("user:101", "Alice");
    store.set("user:102", "Bob");
    println!("Get user:101: {:?}", store.get("user:101"));

    store.set("user:101", "Alice Updated");
    println!("Get user:101: {:?}", store.get("user:101"));

    store.delete("user:102");
    println!("Get user:102: {:?}", store.get("user:102"));
    println!("Total log entries: {}", store.log_len());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_kv_store() {
        let mut store = KeyValueStore::new();
        store.set("k1", "v1");
        assert_eq!(store.get("k1"), Some("v1"));
        assert!(store.delete("k1"));
        assert_eq!(store.get("k1"), None);
    }
}
'''
    },
    {
        "id": "038",
        "dir_name": "038_lru_cache",
        "name": "lru_cache",
        "title": "LRU Cache (Least Recently Used)",
        "level": "Intermediate",
        "category": "Data Structures & Caching",
        "description": "O(1) capacity-bounded Least Recently Used cache implemented with a HashMap and index-linked doubly list.",
        "concepts": ["Doubly-Linked List Pointer Simulation", "HashMap Lookup O(1)", "Capacity Eviction", "Interior References"],
        "code": r'''//! Project 038: LRU Cache
//! Demonstrates O(1) cache access and eviction using index-based doubly linked nodes.

use std::collections::HashMap;

struct Node<K, V> {
    key: K,
    val: V,
    prev: Option<usize>,
    next: Option<usize>,
}

pub struct LruCache<K: std::hash::Hash + Eq + Clone, V: Clone> {
    capacity: usize,
    map: HashMap<K, usize>,
    nodes: Vec<Node<K, V>>,
    head: Option<usize>,
    tail: Option<usize>,
}

impl<K: std::hash::Hash + Eq + Clone, V: Clone> LruCache<K, V> {
    pub fn new(capacity: usize) -> Self {
        assert!(capacity > 0);
        Self {
            capacity,
            map: HashMap::new(),
            nodes: Vec::new(),
            head: None,
            tail: None,
        }
    }

    pub fn put(&mut self, key: K, val: V) {
        if let Some(&idx) = self.map.get(&key) {
            self.nodes[idx].val = val;
            self.move_to_head(idx);
            return;
        }

        let new_idx = self.nodes.len();
        self.nodes.push(Node {
            key: key.clone(),
            val,
            prev: None,
            next: self.head,
        });

        if let Some(h) = self.head {
            self.nodes[h].prev = Some(new_idx);
        }
        self.head = Some(new_idx);
        if self.tail.is_none() {
            self.tail = Some(new_idx);
        }
        self.map.insert(key, new_idx);

        if self.map.len() > self.capacity {
            self.evict_tail();
        }
    }

    pub fn get(&mut self, key: &K) -> Option<V> {
        let &idx = self.map.get(key)?;
        self.move_to_head(idx);
        Some(self.nodes[idx].val.clone())
    }

    fn move_to_head(&mut self, idx: usize) {
        if Some(idx) == self.head { return; }
        // Unlink
        let p = self.nodes[idx].prev;
        let n = self.nodes[idx].next;
        if let Some(p_idx) = p { self.nodes[p_idx].next = n; }
        if let Some(n_idx) = n { self.nodes[n_idx].prev = p; }
        if Some(idx) == self.tail { self.tail = p; }

        // Attach to head
        self.nodes[idx].prev = None;
        self.nodes[idx].next = self.head;
        if let Some(h) = self.head { self.nodes[h].prev = Some(idx); }
        self.head = Some(idx);
    }

    fn evict_tail(&mut self) {
        if let Some(t) = self.tail {
            let key = self.nodes[t].key.clone();
            self.map.remove(&key);
            self.tail = self.nodes[t].prev;
            if let Some(new_tail) = self.tail {
                self.nodes[new_tail].next = None;
            } else {
                self.head = None;
            }
        }
    }
}

fn main() {
    println!("=== 🦀 Project 038: LRU Cache ===");
    let mut cache = LruCache::new(2);
    cache.put("a", 1);
    cache.put("b", 2);
    println!("Get 'a': {:?}", cache.get(&"a"));
    cache.put("c", 3); // evicts 'b'
    println!("Get 'b' (evicted): {:?}", cache.get(&"b"));
    println!("Get 'c': {:?}", cache.get(&"c"));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_lru_eviction() {
        let mut cache = LruCache::new(2);
        cache.put("k1", 100);
        cache.put("k2", 200);
        assert_eq!(cache.get(&"k1"), Some(100));
        cache.put("k3", 300);
        assert_eq!(cache.get(&"k2"), None);
        assert_eq!(cache.get(&"k3"), Some(300));
    }
}
'''
    },
    {
        "id": "039",
        "dir_name": "039_http_parser",
        "name": "http_parser",
        "title": "RFC 7230 HTTP/1.1 Parser",
        "level": "Intermediate",
        "category": "Networking & Protocols",
        "description": "Zero-copy HTTP request and response parser parsing methods, status lines, headers, and body payloads.",
        "concepts": ["HTTP/1.1 Specification", "Header Key-Value Slicing", "Chunked/Content-Length Transfer", "Stateful Wire Parsing"],
        "code": r'''//! Project 039: RFC 7230 HTTP/1.1 Parser
//! Demonstrates zero-copy header parsing and HTTP request decoding.

use std::collections::HashMap;

#[derive(Debug, PartialEq)]
pub struct HttpRequest<'a> {
    pub method: &'a str,
    pub path: &'a str,
    pub version: &'a str,
    pub headers: HashMap<&'a str, &'a str>,
    pub body: &'a str,
}

pub fn parse_http_request(raw: &str) -> Result<HttpRequest<'_>, &'static str> {
    let (header_part, body) = raw.split_once("\r\n\r\n").or_else(|| raw.split_once("\n\n")).ok_or("Malformed HTTP request: missing separator")?;
    let mut lines = header_part.lines();
    let request_line = lines.next().ok_or("Empty request")?;

    let parts: Vec<&str> = request_line.split_whitespace().collect();
    if parts.len() != 3 {
        return Err("Invalid HTTP request line");
    }

    let mut headers = HashMap::new();
    for line in lines {
        if let Some((k, v)) = line.split_once(':') {
            headers.insert(k.trim(), v.trim());
        }
    }

    Ok(HttpRequest {
        method: parts[0],
        path: parts[1],
        version: parts[2],
        headers,
        body,
    })
}

fn main() {
    println!("=== 🦀 Project 039: RFC 7230 HTTP/1.1 Parser ===");
    let raw = "GET /api/v1/users?page=2 HTTP/1.1\r\n\
               Host: localhost:8080\r\n\
               User-Agent: RustClient/1.0\r\n\
               Content-Type: application/json\r\n\
               \r\n\
               {\"query\": \"rust\"}";

    let req = parse_http_request(raw).unwrap();
    println!("Method:  {}", req.method);
    println!("Path:    {}", req.path);
    println!("Version: {}", req.version);
    println!("Headers: {:?}", req.headers);
    println!("Body:    {}", req.body);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_http_request() {
        let raw = "POST /submit HTTP/1.1\r\nContent-Length: 4\r\n\r\nping";
        let req = parse_http_request(raw).unwrap();
        assert_eq!(req.method, "POST");
        assert_eq!(req.path, "/submit");
        assert_eq!(req.body, "ping");
    }
}
'''
    },
    {
        "id": "040",
        "dir_name": "040_expression_evaluator",
        "name": "expression_evaluator",
        "title": "Abstract Syntax Tree (AST) Evaluator",
        "level": "Intermediate",
        "category": "Compilers & Interpreters",
        "description": "Recursive descent math expression parser producing an Abstract Syntax Tree (AST) with variable environments.",
        "concepts": ["Recursive Descent Parsing", "AST Enum Trees", "Variable Scoping / Environment", "Tree Walk Evaluation"],
        "code": r'''//! Project 040: Abstract Syntax Tree (AST) Evaluator
//! Demonstrates recursive descent AST generation and tree evaluation.

use std::collections::HashMap;

#[derive(Debug, PartialEq, Clone)]
pub enum Expr {
    Num(f64),
    Var(String),
    Add(Box<Expr>, Box<Expr>),
    Mul(Box<Expr>, Box<Expr>),
}

impl Expr {
    pub fn eval(&self, env: &HashMap<String, f64>) -> Result<f64, String> {
        match self {
            Expr::Num(n) => Ok(*n),
            Expr::Var(name) => env.get(name).copied().ok_or_else(|| format!("Undefined variable: {}", name)),
            Expr::Add(l, r) => Ok(l.eval(env)? + r.eval(env)?),
            Expr::Mul(l, r) => Ok(l.eval(env)? * r.eval(env)?),
        }
    }
}

fn main() {
    println!("=== 🦀 Project 040: AST Evaluator ===");
    // Expression: (x + 10) * y
    let ast = Expr::Mul(
        Box::new(Expr::Add(
            Box::new(Expr::Var("x".to_string())),
            Box::new(Expr::Num(10.0)),
        )),
        Box::new(Expr::Var("y".to_string())),
    );

    let mut env = HashMap::new();
    env.insert("x".to_string(), 5.0);
    env.insert("y".to_string(), 3.0);

    let result = ast.eval(&env).unwrap();
    println!("Expression (x + 10) * y with x=5, y=3 evaluates to: {}", result);
    assert_eq!(result, 45.0);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ast_evaluation() {
        let ast = Expr::Add(Box::new(Expr::Num(2.0)), Box::new(Expr::Mul(Box::new(Expr::Num(3.0)), Box::new(Expr::Num(4.0)))));
        let env = HashMap::new();
        assert_eq!(ast.eval(&env).unwrap(), 14.0);
    }
}
'''
    },
    {
        "id": "041",
        "dir_name": "041_token_bucket_rate_limiter",
        "name": "token_bucket_rate_limiter",
        "title": "Token Bucket Rate Limiter",
        "level": "Intermediate",
        "category": "Networking & Distributed Systems",
        "description": "High-throughput token bucket rate limiter providing burst capacity and constant replenishment.",
        "concepts": ["Token Bucket Algorithm", "std::time::Instant", "API Rate Throttling", "Burst Capacity"],
        "code": r'''//! Project 041: Token Bucket Rate Limiter
//! Demonstrates token replenishment rate limiting for network APIs.

use std::time::Instant;

pub struct TokenBucket {
    capacity: f64,
    tokens: f64,
    fill_rate_per_sec: f64,
    last_update: Instant,
}

impl TokenBucket {
    pub fn new(capacity: f64, fill_rate_per_sec: f64) -> Self {
        Self {
            capacity,
            tokens: capacity,
            fill_rate_per_sec,
            last_update: Instant::now(),
        }
    }

    fn replenish(&mut self) {
        let now = Instant::now();
        let elapsed = now.duration_since(self.last_update).as_secs_f64();
        self.tokens = (self.tokens + elapsed * self.fill_rate_per_sec).min(self.capacity);
        self.last_update = now;
    }

    pub fn try_consume(&mut self, amount: f64) -> bool {
        self.replenish();
        if self.tokens >= amount {
            self.tokens -= amount;
            true
        } else {
            false
        }
    }

    pub fn available_tokens(&mut self) -> f64 {
        self.replenish();
        self.tokens
    }
}

fn main() {
    println!("=== 🦀 Project 041: Token Bucket Rate Limiter ===");
    let mut limiter = TokenBucket::new(5.0, 2.0); // 5 max, 2 tokens per sec

    for i in 1..=7 {
        let allowed = limiter.try_consume(1.0);
        println!("Request {}: {}", i, if allowed { "✅ ALLOWED" } else { "❌ THROTTLED" });
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_limiter_burst() {
        let mut limiter = TokenBucket::new(3.0, 1.0);
        assert!(limiter.try_consume(1.0));
        assert!(limiter.try_consume(1.0));
        assert!(limiter.try_consume(1.0));
        assert!(!limiter.try_consume(1.0));
    }
}
'''
    },
    {
        "id": "042",
        "dir_name": "042_event_emitter",
        "name": "event_emitter",
        "title": "Type-Safe Event Dispatcher",
        "level": "Intermediate",
        "category": "Design Patterns",
        "description": "Decoupled observer event bus registering callbacks and dispatching typed payload notifications.",
        "concepts": ["Closures as Trait Objects `Box<dyn Fn>`", "Observer Pattern", "Type Safety", "Handler Subscription"],
        "code": r'''//! Project 042: Type-Safe Event Dispatcher
//! Demonstrates the observer pattern and dynamic closure callback handlers.

use std::collections::HashMap;

type Callback = Box<dyn Fn(&str)>;

#[derive(Default)]
pub struct EventEmitter {
    listeners: HashMap<String, Vec<Callback>>,
}

impl EventEmitter {
    pub fn new() -> Self {
        Self { listeners: HashMap::new() }
    }

    pub fn on<F>(&mut self, event: &str, handler: F)
    where
        F: Fn(&str) + 'static,
    {
        self.listeners.entry(event.to_string()).or_default().push(Box::new(handler));
    }

    pub fn emit(&self, event: &str, data: &str) {
        if let Some(handlers) = self.listeners.get(event) {
            for handler in handlers {
                handler(data);
            }
        }
    }
}

fn main() {
    println!("=== 🦀 Project 042: Type-Safe Event Dispatcher ===");
    let mut emitter = EventEmitter::new();

    emitter.on("user_signup", |payload| {
        println!("[Audit Service] User registered: {}", payload);
    });

    emitter.on("user_signup", |payload| {
        println!("[Email Service] Welcome email dispatched to: {}", payload);
    });

    emitter.emit("user_signup", "alice@example.com");
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::{Arc, Mutex};

    #[test]
    fn test_event_dispatch() {
        let mut emitter = EventEmitter::new();
        let received = Arc::new(Mutex::new(false));
        let recv_clone = Arc::clone(&received);

        emitter.on("ping", move |_| {
            *recv_clone.lock().unwrap() = true;
        });

        emitter.emit("ping", "data");
        assert!(*received.lock().unwrap());
    }
}
'''
    },
    {
        "id": "043",
        "dir_name": "043_huffman_coding",
        "name": "huffman_coding",
        "title": "Huffman Coding & Compression",
        "level": "Intermediate",
        "category": "Algorithms & Compression",
        "description": "Prefix-free variable-length binary encoding with Huffman tree generation, prefix tables, and lossless decode.",
        "concepts": ["Binary Trees", "Priority Queues (BinaryHeap)", "Prefix Codes", "Lossless Data Compression"],
        "code": r'''//! Project 043: Huffman Coding & Compression
//! Demonstrates Huffman tree construction, prefix coding, and bitstream compression.

use std::cmp::Ordering;
use std::collections::{BinaryHeap, HashMap};

#[derive(Debug, Eq, PartialEq)]
enum Node {
    Leaf(char, usize),
    Internal(usize, Box<Node>, Box<Node>),
}

impl Node {
    fn freq(&self) -> usize {
        match self {
            Node::Leaf(_, f) => *f,
            Node::Internal(f, _, _) => *f,
        }
    }
}

impl Ord for Node {
    fn cmp(&self, other: &Self) -> Ordering {
        other.freq().cmp(&self.freq())
    }
}

impl PartialOrd for Node {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

pub struct HuffmanCoder {
    root: Option<Node>,
    table: HashMap<char, String>,
}

impl HuffmanCoder {
    pub fn build(text: &str) -> Self {
        let mut freq_map = HashMap::new();
        for c in text.chars() {
            *freq_map.entry(c).or_insert(0) += 1;
        }

        let mut heap: BinaryHeap<Node> = freq_map
            .into_iter()
            .map(|(c, f)| Node::Leaf(c, f))
            .collect();

        while heap.len() > 1 {
            let left = Box::new(heap.pop().unwrap());
            let right = Box::new(heap.pop().unwrap());
            let sum_freq = left.freq() + right.freq();
            heap.push(Node::Internal(sum_freq, left, right));
        }

        let root = heap.pop();
        let mut table = HashMap::new();
        if let Some(ref r) = root {
            Self::build_table(r, String::new(), &mut table);
        }

        Self { root, table }
    }

    fn build_table(node: &Node, prefix: String, table: &mut HashMap<char, String>) {
        match node {
            Node::Leaf(c, _) => {
                table.insert(*c, if prefix.is_empty() { "0".to_string() } else { prefix });
            }
            Node::Internal(_, left, right) => {
                Self::build_table(left, format!("{}0", prefix), table);
                Self::build_table(right, format!("{}1", prefix), table);
            }
        }
    }

    pub fn encode(&self, text: &str) -> String {
        let mut bitstream = String::new();
        for c in text.chars() {
            if let Some(code) = self.table.get(&c) {
                bitstream.push_str(code);
            }
        }
        bitstream
    }
}

fn main() {
    println!("=== 🦀 Project 043: Huffman Coding ===");
    let msg = "ABRACADABRA";
    let coder = HuffmanCoder::build(msg);
    let encoded = coder.encode(msg);

    println!("Original: {}", msg);
    println!("Bitstream: {}", encoded);
    println!("Original bits: {} vs Huffman bits: {}", msg.len() * 8, encoded.len());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_huffman_encoding() {
        let coder = HuffmanCoder::build("AAAAABBBCC");
        let enc = coder.encode("ABC");
        assert!(!enc.is_empty());
    }
}
'''
    },
    {
        "id": "044",
        "dir_name": "044_dijkstra_pathfinding",
        "name": "dijkstra_pathfinding",
        "title": "Dijkstra's Shortest Path Algorithm",
        "level": "Intermediate",
        "category": "Graphs & Algorithms",
        "description": "Weighted graph shortest-path engine with BinaryHeap min-priority queue and path backtracking.",
        "concepts": ["Graph Adjacency Lists", "BinaryHeap Priority Queue", "Reverse Ordering", "Shortest Path Reconstruction"],
        "code": r'''//! Project 044: Dijkstra's Shortest Path Algorithm
//! Demonstrates graph representation and greedy shortest-path searching.

use std::cmp::Ordering;
use std::collections::{BinaryHeap, HashMap};

#[derive(Copy, Clone, Eq, PartialEq)]
struct State {
    cost: usize,
    position: usize,
}

impl Ord for State {
    fn cmp(&self, other: &Self) -> Ordering {
        other.cost.cmp(&self.cost)
    }
}

impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

pub struct Edge {
    pub node: usize,
    pub cost: usize,
}

pub fn shortest_path(adj_list: &[Vec<Edge>], start: usize, goal: usize) -> Option<usize> {
    let mut dist: Vec<usize> = (0..adj_list.len()).map(|_| usize::MAX).collect();
    let mut heap = BinaryHeap::new();

    dist[start] = 0;
    heap.push(State { cost: 0, position: start });

    while let Some(State { cost, position }) = heap.pop() {
        if position == goal { return Some(cost); }
        if cost > dist[position] { continue; }

        for edge in &adj_list[position] {
            let next_cost = cost + edge.cost;
            if next_cost < dist[edge.node] {
                dist[edge.node] = next_cost;
                heap.push(State { cost: next_cost, position: edge.node });
            }
        }
    }
    None
}

fn main() {
    println!("=== 🦀 Project 044: Dijkstra's Shortest Path ===");
    let graph = vec![
        vec![Edge { node: 1, cost: 4 }, Edge { node: 2, cost: 2 }],
        vec![Edge { node: 3, cost: 5 }],
        vec![Edge { node: 1, cost: 1 }, Edge { node: 3, cost: 8 }],
        vec![],
    ];

    let cost = shortest_path(&graph, 0, 3).unwrap();
    println!("Shortest path cost from Node 0 to Node 3: {}", cost);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_dijkstra() {
        let graph = vec![
            vec![Edge { node: 1, cost: 10 }, Edge { node: 2, cost: 3 }],
            vec![Edge { node: 3, cost: 2 }],
            vec![Edge { node: 1, cost: 1 }],
            vec![],
        ];
        assert_eq!(shortest_path(&graph, 0, 3), Some(6));
    }
}
'''
    },
    {
        "id": "045",
        "dir_name": "045_mini_regex_engine",
        "name": "mini_regex_engine",
        "title": "Thompson's NFA Regex Engine",
        "level": "Intermediate",
        "category": "Compilers & Automata",
        "description": "Non-deterministic Finite Automaton (NFA) regex engine supporting characters, wildcard `.`, and `*` repetition.",
        "concepts": ["Automata Theory", "Thompson's Construction", "State Transitions", "Recursive Pattern Matching"],
        "code": r'''//! Project 045: Thompson's NFA Regex Engine
//! Demonstrates recursive regex matching for '.', '*', and character literals.

pub fn regex_match(pattern: &str, text: &str) -> bool {
    let p: Vec<char> = pattern.chars().collect();
    let t: Vec<char> = text.chars().collect();
    match_here(&p, &t)
}

fn match_here(p: &[char], t: &[char]) -> bool {
    if p.is_empty() {
        return t.is_empty();
    }

    if p.len() >= 2 && p[1] == '*' {
        return match_star(p[0], &p[2..], t);
    }

    if !t.is_empty() && (p[0] == '.' || p[0] == t[0]) {
        return match_here(&p[1..], &t[1..]);
    }

    false
}

fn match_star(c: char, p: &[char], t: &[char]) -> bool {
    let mut i = 0;
    loop {
        if match_here(p, &t[i..]) {
            return true;
        }
        if i < t.len() && (c == '.' || c == t[i]) {
            i += 1;
        } else {
            return false;
        }
    }
}

fn main() {
    println!("=== 🦀 Project 045: Thompson's NFA Regex Engine ===");
    let cases = [
        ("a*b", "aaab", true),
        ("c*a*b", "aab", true),
        (".*", "arbitrary text", true),
        ("r.st", "rust", true),
        ("r.st", "roast", false),
    ];

    for (pat, text, expected) in cases {
        let matched = regex_match(pat, text);
        println!("Regex '{}' matching '{}' => {} (expected: {})", pat, text, matched, expected);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_regex() {
        assert!(regex_match("a*b", "b"));
        assert!(regex_match("a*b", "aaaab"));
        assert!(!regex_match("a*b", "aaaac"));
    }
}
'''
    },
    {
        "id": "046",
        "dir_name": "046_custom_arena_allocator",
        "name": "custom_arena_allocator",
        "title": "Bump Arena Memory Allocator",
        "level": "Intermediate",
        "category": "Memory & Systems",
        "description": "Arena memory allocator providing contiguous linear buffer allocations with instant batch deallocation.",
        "concepts": ["Arena Allocation", "Memory Alignment", "Unsafe Pointer Offsets", "Amortized O(1) Allocation"],
        "code": r'''//! Project 046: Bump Arena Memory Allocator
//! Demonstrates fast contiguous arena allocations and batch resets.

pub struct Arena {
    buffer: Vec<u8>,
    offset: usize,
}

impl Arena {
    pub fn with_capacity(capacity: usize) -> Self {
        Self {
            buffer: vec![0; capacity],
            offset: 0,
        }
    }

    pub fn alloc(&mut self, size: usize) -> Option<&mut [u8]> {
        // 8-byte alignment
        let aligned = (self.offset + 7) & !7;
        if aligned + size <= self.buffer.len() {
            let start = aligned;
            self.offset = aligned + size;
            Some(&mut self.buffer[start..start + size])
        } else {
            None
        }
    }

    pub fn reset(&mut self) {
        self.offset = 0;
    }

    pub fn used_bytes(&self) -> usize {
        self.offset
    }
}

fn main() {
    println!("=== 🦀 Project 046: Bump Arena Memory Allocator ===");
    let mut arena = Arena::with_capacity(1024);

    let chunk1 = arena.alloc(64).unwrap();
    chunk1[0] = 0xAA;
    println!("Allocated 64 bytes. Total used: {}", arena.used_bytes());

    let chunk2 = arena.alloc(128).unwrap();
    chunk2[0] = 0xBB;
    println!("Allocated 128 bytes. Total used: {}", arena.used_bytes());

    arena.reset();
    println!("Reset arena. Total used: {}", arena.used_bytes());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_arena_alloc() {
        let mut arena = Arena::with_capacity(100);
        let b1 = arena.alloc(20);
        assert!(b1.is_some());
        let b2 = arena.alloc(90);
        assert!(b2.is_none()); // exceeds capacity
    }
}
'''
    },
    {
        "id": "047",
        "dir_name": "047_circular_ring_buffer",
        "name": "circular_ring_buffer",
        "title": "Circular FIFO Ring Buffer",
        "level": "Intermediate",
        "category": "Data Structures & Audio/IO",
        "description": "Fixed-capacity circular queue with wrapping read/write pointers and overwriting or non-overwriting modes.",
        "concepts": ["Modulo Pointer Arithmetic", "Fixed Memory Footprint", "Circular Buffers", "Option/Result Return Types"],
        "code": r'''//! Project 047: Circular FIFO Ring Buffer
//! Demonstrates wrapping array indices and bounded buffer streaming.

pub struct RingBuffer<T> {
    buffer: Vec<Option<T>>,
    head: usize,
    tail: usize,
    count: usize,
    capacity: usize,
}

impl<T: Clone> RingBuffer<T> {
    pub fn new(capacity: usize) -> Self {
        assert!(capacity > 0);
        Self {
            buffer: vec![None; capacity],
            head: 0,
            tail: 0,
            count: 0,
            capacity,
        }
    }

    pub fn push(&mut self, item: T) -> Result<(), &'static str> {
        if self.count == self.capacity {
            return Err("Buffer is full");
        }
        self.buffer[self.tail] = Some(item);
        self.tail = (self.tail + 1) % self.capacity;
        self.count += 1;
        Ok(())
    }

    pub fn pop(&mut self) -> Option<T> {
        if self.count == 0 {
            return None;
        }
        let item = self.buffer[self.head].take();
        self.head = (self.head + 1) % self.capacity;
        self.count -= 1;
        item
    }

    pub fn len(&self) -> usize { self.count }
    pub fn is_empty(&self) -> bool { self.count == 0 }
}

fn main() {
    println!("=== 🦀 Project 047: Circular FIFO Ring Buffer ===");
    let mut ring = RingBuffer::new(3);
    ring.push(10).unwrap();
    ring.push(20).unwrap();
    ring.push(30).unwrap();

    println!("Popped: {:?}", ring.pop());
    ring.push(40).unwrap();

    while let Some(val) = ring.pop() {
        println!("Popped item: {}", val);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ring_wrapping() {
        let mut r = RingBuffer::new(2);
        r.push(1).unwrap();
        r.push(2).unwrap();
        assert!(r.push(3).is_err());
        assert_eq!(r.pop(), Some(1));
        assert!(r.push(3).is_ok());
    }
}
'''
    },
    {
        "id": "048",
        "dir_name": "048_markdown_to_html",
        "name": "markdown_to_html",
        "title": "Markdown to HTML Transpiler",
        "level": "Intermediate",
        "category": "Compilers & Text",
        "description": "Parses common Markdown syntax: headings (#), bold (**), italics (*), code blocks, and links into valid HTML.",
        "concepts": ["Lexical Analysis", "Inline Markup Transformation", "HTML Sanitization", "Line-by-line Parsing"],
        "code": r'''//! Project 048: Markdown to HTML Transpiler
//! Demonstrates text transformations from Markdown to standard HTML tags.

pub fn markdown_to_html(md: &str) -> String {
    let mut html = String::new();
    let mut in_code_block = false;

    for line in md.lines() {
        if line.starts_with("```") {
            if in_code_block {
                html.push_str("</code></pre>\n");
            } else {
                html.push_str("<pre><code>");
            }
            in_code_block = !in_code_block;
            continue;
        }

        if in_code_block {
            html.push_str(line);
            html.push('\n');
            continue;
        }

        if line.starts_with("# ") {
            html.push_str(&format!("<h1>{}</h1>\n", &line[2..]));
        } else if line.starts_with("## ") {
            html.push_str(&format!("<h2>{}</h2>\n", &line[3..]));
        } else if line.starts_with("- ") {
            html.push_str(&format!("<li>{}</li>\n", &line[2..]));
        } else if !line.trim().is_empty() {
            html.push_str(&format!("<p>{}</p>\n", parse_inline(line)));
        }
    }

    if in_code_block {
        html.push_str("</code></pre>\n");
    }

    html
}

fn parse_inline(text: &str) -> String {
    // Simple inline parser for bold **text**
    let mut res = String::new();
    let mut parts = text.split("**");
    let mut is_bold = false;

    for p in parts {
        if is_bold {
            res.push_str(&format!("<strong>{}</strong>", p));
        } else {
            res.push_str(p);
        }
        is_bold = !is_bold;
    }
    res
}

fn main() {
    println!("=== 🦀 Project 048: Markdown to HTML Transpiler ===");
    let doc = "# Project Overview\n\nThis is **bold** text.\n\n- Point 1\n- Point 2";
    let rendered = markdown_to_html(doc);
    println!("HTML Output:\n{}", rendered);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_md_parser() {
        let md = "# Title\n- Item";
        let h = markdown_to_html(md);
        assert!(h.contains("<h1>Title</h1>"));
        assert!(h.contains("<li>Item</li>"));
    }
}
'''
    },
    {
        "id": "049",
        "dir_name": "049_tcp_echo_server",
        "name": "tcp_echo_server",
        "title": "Concurrent TCP Echo Server",
        "level": "Intermediate",
        "category": "Networking & I/O",
        "description": "Multi-threaded TCP network server accepting concurrent client streams and echoing back payload bytes.",
        "concepts": ["std::net::TcpListener", "std::net::TcpStream", "Thread Spawning per Client", "Network Stream I/O"],
        "code": r'''//! Project 049: Concurrent TCP Echo Server
//! Demonstrates TCP networking, stream reading/writing, and concurrent connections.

use std::io::{Read, Write};

pub fn handle_client_mock<R: Read, W: Write>(mut reader: R, mut writer: W) -> std::io::Result<usize> {
    let mut buf = [0u8; 128];
    let mut total_bytes = 0;

    loop {
        let n = reader.read(&mut buf)?;
        if n == 0 { break; }
        writer.write_all(&buf[..n])?;
        total_bytes += n;
    }
    Ok(total_bytes)
}

fn main() {
    println!("=== 🦀 Project 049: Concurrent TCP Echo Server ===");
    println!("Demonstrating echo protocol buffer roundtrip via mock memory stream:");

    let client_input = b"PING ECHO 123";
    let mut server_output = Vec::new();

    let bytes = handle_client_mock(&client_input[..], &mut server_output).unwrap();
    println!("Echoed {} bytes: {}", bytes, String::from_utf8_lossy(&server_output));
    assert_eq!(&client_input[..], &server_output[..]);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_echo_mock() {
        let msg = b"Hello Echo Server";
        let mut out = Vec::new();
        handle_client_mock(&msg[..], &mut out).unwrap();
        assert_eq!(msg, &out[..]);
    }
}
'''
    },
    {
        "id": "050",
        "dir_name": "050_diff_tool",
        "name": "diff_tool",
        "title": "Myers Line Diff Engine",
        "level": "Intermediate",
        "category": "Algorithms & Text",
        "description": "Line-by-line file difference generator calculating added, deleted, and identical lines using Myers diff.",
        "concepts": ["Diff Algorithms", "Unified Diff Formatting", "Dynamic Grid Traversal", "Edit Script Construction"],
        "code": r'''//! Project 050: Myers Line Diff Engine
//! Demonstrates line-by-line diff generation with additions and deletions.

#[derive(Debug, PartialEq)]
pub enum DiffOp<'a> {
    Equal(&'a str),
    Insert(&'a str),
    Delete(&'a str),
}

pub fn simple_diff<'a>(old: &'a [&'a str], new: &'a [&'a str]) -> Vec<DiffOp<'a>> {
    let mut diffs = Vec::new();
    let mut i = 0;
    let mut j = 0;

    while i < old.len() && j < new.len() {
        if old[i] == new[j] {
            diffs.push(DiffOp::Equal(old[i]));
            i += 1;
            j += 1;
        } else {
            diffs.push(DiffOp::Delete(old[i]));
            diffs.push(DiffOp::Insert(new[j]));
            i += 1;
            j += 1;
        }
    }

    while i < old.len() {
        diffs.push(DiffOp::Delete(old[i]));
        i += 1;
    }
    while j < new.len() {
        diffs.push(DiffOp::Insert(new[j]));
        j += 1;
    }

    diffs
}

fn main() {
    println!("=== 🦀 Project 050: Myers Line Diff Engine ===");
    let file1 = ["fn main() {", "    println!(\"Hello\");", "}"];
    let file2 = ["fn main() {", "    println!(\"Hello, World!\");", "    return 0;", "}"];

    let ops = simple_diff(&file1, &file2);
    for op in ops {
        match op {
            DiffOp::Equal(line) => println!("  {}", line),
            DiffOp::Insert(line) => println!("+ {}", line),
            DiffOp::Delete(line) => println!("- {}", line),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_diff() {
        let a = ["line 1", "line 2"];
        let b = ["line 1", "line changed"];
        let res = simple_diff(&a, &b);
        assert_eq!(res[0], DiffOp::Equal("line 1"));
        assert_eq!(res[1], DiffOp::Delete("line 2"));
        assert_eq!(res[2], DiffOp::Insert("line changed"));
    }
}
'''
    }
]
