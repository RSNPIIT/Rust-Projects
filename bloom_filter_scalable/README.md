# 🦀 Scalable Partitioned Bloom Filter (`058_bloom_filter_scalable`)

**Difficulty:** 🟡 Intermediate  
**Category:** Probabilistic Data Structures  

---

## 📖 Overview

Multi-slice Bloom filter dynamically growing additional layers as capacity fills to maintain bounded error rate.

---

## 🎯 Key Rust Concepts Demonstrated

- **Layered Filters**
- **Geometric Growth**
- **Error Probability Bounding**
- **Hash Partitioning**

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
058_bloom_filter_scalable/
├── Cargo.toml      # Package manifest
├── README.md       # Project documentation
└── src/
    └── main.rs     # Implementation & unit tests
```
