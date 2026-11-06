# 🦀 Shared Memory IPC Ring Buffer (`085_memory_mapped_ring_buffer`)

**Difficulty:** 🔴 Advanced  
**Category:** Systems & IPC  

---

## 📖 Overview

Simulated shared-memory circular queue for inter-process communication (IPC) with atomic synchronization.

---

## 🎯 Key Rust Concepts Demonstrated

- **Shared-Memory Layout**
- **Atomic Read/Write Head Offsets**
- **Inter-Process Communication (IPC)**
- **Zero-Copy Data Transfer**

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
085_memory_mapped_ring_buffer/
├── Cargo.toml      # Package manifest
├── README.md       # Project documentation
└── src/
    └── main.rs     # Implementation & unit tests
```
