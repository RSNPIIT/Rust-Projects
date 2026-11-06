# 🦀 Robust CSV Table Parser (`017_csv_parser`)

**Difficulty:** 🟢 Simple  
**Category:** File Formats & Parsing  

---

## 📖 Overview

Parses CSV text adhering to RFC 4180 rules, correctly managing embedded commas, escape quotes, and line breaks.

---

## 🎯 Key Rust Concepts Demonstrated

- **State Machine Parsing**
- **Slice Chunking**
- **RFC 4180 Specification**
- **Vector of Records**

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
017_csv_parser/
├── Cargo.toml      # Package manifest
├── README.md       # Project documentation
└── src/
    └── main.rs     # Implementation & unit tests
```
