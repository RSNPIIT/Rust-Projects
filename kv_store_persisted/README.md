# 🦀 Persistent Key-Value Store (`037_kv_store_persisted`)

**Difficulty:** 🟡 Intermediate  
**Category:** Databases & Storage  

---

## 📖 Overview

Bitcask-inspired append-only log structured key-value store with in-memory HashMap offset index.

---

## 🎯 Key Rust Concepts Demonstrated

- **Append-Only Log Files**
- **In-Memory Hash Index**
- **File Offsets & Seeking**
- **Tombstone Deletions**

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
037_kv_store_persisted/
├── Cargo.toml      # Package manifest
├── README.md       # Project documentation
└── src/
    └── main.rs     # Implementation & unit tests
```
