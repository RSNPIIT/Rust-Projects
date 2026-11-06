# 🦀 POSIX UStar Tar Archive Reader (`064_tar_archive_reader`)

**Difficulty:** 🟡 Intermediate  
**Category:** File Formats & Systems  

---

## 📖 Overview

Parses standard 512-byte POSIX UStar tar headers extracting filename, size, octal permissions, and content.

---

## 🎯 Key Rust Concepts Demonstrated

- **Tar 512-Byte Record Blocks**
- **Octal String to Integer Parsing**
- **Binary Header Layout**
- **Stream Chunking**

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
064_tar_archive_reader/
├── Cargo.toml      # Package manifest
├── README.md       # Project documentation
└── src/
    └── main.rs     # Implementation & unit tests
```
