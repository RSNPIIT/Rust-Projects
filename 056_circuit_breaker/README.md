# 🦀 Circuit Breaker State Machine (`056_circuit_breaker`)

**Difficulty:** 🟡 Intermediate  
**Category:** Distributed Systems  

---

## 📖 Overview

Resilience pattern state machine (Closed, Open, HalfOpen) tripping on fault thresholds and recovering after timeout.

---

## 🎯 Key Rust Concepts Demonstrated

- **Finite State Machine**
- **Fault Tolerance & Trip Limits**
- **std::time::Instant**
- **Resilience Patterns**

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
056_circuit_breaker/
├── Cargo.toml      # Package manifest
├── README.md       # Project documentation
└── src/
    └── main.rs     # Implementation & unit tests
```
