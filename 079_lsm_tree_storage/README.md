# 🦀 Log-Structured Merge Tree (LSM) (`079_lsm_tree_storage`)

**Difficulty:** 🔴 Advanced  
**Category:** Databases & Storage  

---

## 📖 Overview

LSM-Tree storage architecture with in-memory MemTable (BTreeMap), write-ahead log (WAL), and SSTable compaction.

---

## 🎯 Key Rust Concepts Demonstrated

- **LSM Tree Architecture**
- **MemTable Flush**
- **SSTable Segments**
- **Compaction & De-duplication**

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
079_lsm_tree_storage/
├── Cargo.toml      # Package manifest
├── README.md       # Project documentation
└── src/
    └── main.rs     # Implementation & unit tests
```
