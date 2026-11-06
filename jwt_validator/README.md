# 🦀 JWT (JSON Web Token) Structure Validator (`055_jwt_validator`)

**Difficulty:** 🟡 Intermediate  
**Category:** Web & Security  

---

## 📖 Overview

Parses and unpacks JWT tokens into Header, Payload, and Signature segments with Base64Url decoding.

---

## 🎯 Key Rust Concepts Demonstrated

- **Base64Url Specification**
- **JSON Web Token RFC 7519**
- **Payload Field Extraction**
- **Signature Verification Logic**

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
055_jwt_validator/
├── Cargo.toml      # Package manifest
├── README.md       # Project documentation
└── src/
    └── main.rs     # Implementation & unit tests
```
