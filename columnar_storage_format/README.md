# 🦀 Columnar Table Storage & RLE (`093_columnar_storage_format`)

**Difficulty:** 🔴 Advanced  
**Category:** Databases & Analytics  

---

## 📖 Overview

Column-oriented table representation (Apache Parquet style) with vectorized projections and run-length encoding.

---

## 🎯 Key Rust Concepts Demonstrated

- **Column-Oriented Data Layout**
- **Vectorized Batch Queries**
- **Run-Length Encoding (RLE)**
- **Cache Locality**

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
093_columnar_storage_format/
├── Cargo.toml      # Package manifest
├── README.md       # Project documentation
└── src/
    └── main.rs     # Implementation & unit tests
```
