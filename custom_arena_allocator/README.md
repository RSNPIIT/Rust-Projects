# 🦀 Bump Arena Memory Allocator (`046_custom_arena_allocator`)

**Difficulty:** 🟡 Intermediate  
**Category:** Memory & Systems  

---

## 📖 Overview

Arena memory allocator providing contiguous linear buffer allocations with instant batch deallocation.

---

## 🎯 Key Rust Concepts Demonstrated

- **Arena Allocation**
- **Memory Alignment**
- **Unsafe Pointer Offsets**
- **Amortized O(1) Allocation**

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
046_custom_arena_allocator/
├── Cargo.toml      # Package manifest
├── README.md       # Project documentation
└── src/
    └── main.rs     # Implementation & unit tests
```
