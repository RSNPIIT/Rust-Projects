//! Project 066: Semantic Versioning (SemVer) Parser
//! Demonstrates SemVer 2.0.0 parsing, comparison, and precedence ordering.

use std::cmp::Ordering;

#[derive(Debug, PartialEq, Eq, Clone)]
pub struct Version {
    pub major: u64,
    pub minor: u64,
    pub patch: u64,
    pub pre_release: Option<String>,
}

impl Version {
    pub fn parse(s: &str) -> Result<Self, &'static str> {
        let (version_core, pre) = match s.split_once('-') {
            Some((v, p)) => (v, Some(p.split('+').next().unwrap().to_string())),
            None => (s.split('+').next().unwrap(), None),
        };

        let parts: Vec<&str> = version_core.split('.').collect();
        if parts.len() != 3 {
            return Err("Version core must be major.minor.patch");
        }

        let major = parts[0].parse().map_err(|_| "Invalid major")?;
        let minor = parts[1].parse().map_err(|_| "Invalid minor")?;
        let patch = parts[2].parse().map_err(|_| "Invalid patch")?;

        Ok(Self { major, minor, patch, pre_release: pre })
    }
}

impl Ord for Version {
    fn cmp(&self, other: &Self) -> Ordering {
        self.major.cmp(&other.major)
            .then_with(|| self.minor.cmp(&other.minor))
            .then_with(|| self.patch.cmp(&other.patch))
            .then_with(|| {
                match (&self.pre_release, &other.pre_release) {
                    (None, None) => Ordering::Equal,
                    (Some(_), None) => Ordering::Less, // Pre-release has lower precedence
                    (None, Some(_)) => Ordering::Greater,
                    (Some(a), Some(b)) => a.cmp(b),
                }
            })
    }
}

impl PartialOrd for Version {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

fn main() {
    println!("=== 🦀 Project 066: SemVer Parser ===");
    let mut versions = [
        Version::parse("1.0.0").unwrap(),
        Version::parse("1.0.0-alpha").unwrap(),
        Version::parse("2.1.0").unwrap(),
        Version::parse("1.0.1").unwrap(),
    ];
    versions.sort();
    println!("Sorted SemVer versions:");
    for v in &versions {
        println!(" - {:?}", v);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_semver_precedence() {
        let v1 = Version::parse("1.0.0-alpha").unwrap();
        let v2 = Version::parse("1.0.0").unwrap();
        assert!(v1 < v2);
    }
}
