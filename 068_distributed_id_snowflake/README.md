# 🦀 Twitter Snowflake Distributed ID Generator (`068_distributed_id_snowflake`)

**Difficulty:** 🟡 Intermediate  
**Category:** Distributed Systems  

---

## 📖 Overview

64-bit distributed chronological ID generator incorporating epoch timestamp, worker ID, datacenter ID, and sequence counter.

---

## 🎯 Key Rust Concepts Demonstrated

- **Bitwise Bit Packing**
- **Millisecond Epoch Offsets**
- **Sequence Increment & Overflow Wrapping**
- **Distributed Coordination**

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
068_distributed_id_snowflake/
├── Cargo.toml      # Package manifest
├── README.md       # Project documentation
└── src/
    └── main.rs     # Implementation & unit tests
```
