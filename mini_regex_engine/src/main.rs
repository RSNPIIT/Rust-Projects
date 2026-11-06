//! Project 045: Thompson's NFA Regex Engine
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
