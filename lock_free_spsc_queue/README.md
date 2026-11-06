# 🦀 Lock-Free SPSC Circular Queue (`074_lock_free_spsc_queue`)

**Difficulty:** 🔴 Advanced  
**Category:** Concurrency & Lock-Free  

---

## 📖 Overview

Single-Producer Single-Consumer lock-free ring buffer using atomic operations with acquire-release memory orderings.

---

## 🎯 Key Rust Concepts Demonstrated

- **AtomicUsize & AtomicPtr**
- **Acquire / Release Memory Orderings**
- **Lock-Free Ring Buffers**
- **Hardware Cache Line Padding**

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
074_lock_free_spsc_queue/
├── Cargo.toml      # Package manifest
├── README.md       # Project documentation
└── src/
    └── main.rs     # Implementation & unit tests
```
