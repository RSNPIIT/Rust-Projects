# 🦀 Distributed Two-Phase Commit (2PC) (`092_distributed_two_phase_commit`)

**Difficulty:** 🔴 Advanced  
**Category:** Distributed Systems & Transactions  

---

## 📖 Overview

Two-Phase Commit transaction coordinator and cohort participants supporting Prepare, Vote, Commit, and Abort rollback.

---

## 🎯 Key Rust Concepts Demonstrated

- **Atomic Distributed Transactions**
- **Coordinator & Cohort Roles**
- **Prepare & Commit Protocols**
- **Rollback Recovery**

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
092_distributed_two_phase_commit/
├── Cargo.toml      # Package manifest
├── README.md       # Project documentation
└── src/
    └── main.rs     # Implementation & unit tests
```
