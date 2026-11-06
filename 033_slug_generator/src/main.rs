//! Project 033: URL Slug Generator & Sanitizer
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
