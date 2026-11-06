# 🦀 RFC 7230 HTTP/1.1 Parser (`039_http_parser`)

**Difficulty:** 🟡 Intermediate  
**Category:** Networking & Protocols  

---

## 📖 Overview

Zero-copy HTTP request and response parser parsing methods, status lines, headers, and body payloads.

---

## 🎯 Key Rust Concepts Demonstrated

- **HTTP/1.1 Specification**
- **Header Key-Value Slicing**
- **Chunked/Content-Length Transfer**
- **Stateful Wire Parsing**

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
039_http_parser/
├── Cargo.toml      # Package manifest
├── README.md       # Project documentation
└── src/
    └── main.rs     # Implementation & unit tests
```
