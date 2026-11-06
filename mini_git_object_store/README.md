# 🦀 Mini Git Content-Addressable Object Store (`075_mini_git_object_store`)

**Difficulty:** 🔴 Advanced  
**Category:** Version Control & Storage  

---

## 📖 Overview

Content-addressable storage implementation mimicking Git: blob, tree, and commit objects addressed by cryptographic hashes.

---

## 🎯 Key Rust Concepts Demonstrated

- **Content-Addressable Storage**
- **Git Object Model (blob, tree, commit)**
- **SHA Object Hashing**
- **Immutable Object DAG**

---

## 🚀 How to Run

Navigate into this project directory and use `cargo`:

```bash
# Run the project
cargo run

# Run with quiet cargo output
cargo run -q

# Run unit tests
cargo test
```

---

## 📂 Project Structure

```text
075_mini_git_object_store/
├── Cargo.toml      # Package manifest
├── README.md       # Project documentation
└── src/
    └── main.rs     # Implementation & unit tests
```
