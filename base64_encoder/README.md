# 🦀 Base64 Encoder & Decoder (`026_base64_encoder`)

**Difficulty:** 🟢 Simple  
**Category:** Encodings & Cryptography  

---

## 📖 Overview

Standard RFC 4648 Base64 byte-stream encoder and decoder with padding calculation.

---

## 🎯 Key Rust Concepts Demonstrated

- **Bitwise Bit Shifts (`<<`, `>>`)**
- **Byte Chunking (`chunks(3)`)**
- **Lookup Tables**
- **Padding (`=`) Management**

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
026_base64_encoder/
├── Cargo.toml      # Package manifest
├── README.md       # Project documentation
└── src/
    └── main.rs     # Implementation & unit tests
```
