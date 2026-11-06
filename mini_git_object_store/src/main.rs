//! Project 075: Mini Git Content-Addressable Object Store
//! Demonstrates the core immutable DAG model of Git (blobs, trees, commits).

use std::collections::HashMap;

fn hash_content(data: &[u8]) -> String {
    let mut h: u64 = 14695981039346656037;
    for &b in data {
        h = (h ^ (b as u64)).wrapping_mul(1099511628211);
    }
    format!("{:016x}", h)
}

#[derive(Debug, PartialEq, Clone)]
pub enum GitObject {
    Blob(Vec<u8>),
    Commit { tree_hash: String, parent_hash: Option<String>, message: String },
}

pub struct GitObjectStore {
    objects: HashMap<String, GitObject>,
}

impl GitObjectStore {
    pub fn new() -> Self {
        Self { objects: HashMap::new() }
    }

    pub fn write_blob(&mut self, content: &[u8]) -> String {
        let hash = hash_content(content);
        self.objects.insert(hash.clone(), GitObject::Blob(content.to_vec()));
        hash
    }

    pub fn write_commit(&mut self, tree_hash: &str, parent: Option<&str>, message: &str) -> String {
        let payload = format!("{}:{:?}:{}", tree_hash, parent, message);
        let hash = hash_content(payload.as_bytes());
        self.objects.insert(hash.clone(), GitObject::Commit {
            tree_hash: tree_hash.to_string(),
            parent_hash: parent.map(|s| s.to_string()),
            message: message.to_string(),
        });
        hash
    }

    pub fn get(&self, hash: &str) -> Option<&GitObject> {
        self.objects.get(hash)
    }
}

fn main() {
    println!("=== 🦀 Project 075: Mini Git Object Store ===");
    let mut git = GitObjectStore::new();
    let blob_hash = git.write_blob(b"println!(\"Hello, Git!\");");
    println!("Created Blob SHA:   {}", blob_hash);

    let commit1 = git.write_commit(&blob_hash, None, "Initial commit");
    println!("Created Commit #1:  {}", commit1);

    let commit2 = git.write_commit(&blob_hash, Some(&commit1), "Second commit");
    println!("Created Commit #2:  {}", commit2);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_git_store() {
        let mut git = GitObjectStore::new();
        let h = git.write_blob(b"test");
        assert!(git.get(&h).is_some());
    }
}
