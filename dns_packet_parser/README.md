# 🦀 Binary DNS Packet Parser (`065_dns_packet_parser`)

**Difficulty:** 🟡 Intermediate  
**Category:** Networking & Protocols  

---

## 📖 Overview

Decodes binary RFC 1035 DNS wire packets including 12-byte header flags, query questions, and resource records.

---

## 🎯 Key Rust Concepts Demonstrated

- **DNS Wire Format (RFC 1035)**
- **Bitwise Bitfield Flags**
- **Length-Prefixed Domain Labels**
- **Endian Integer Decoding**

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
065_dns_packet_parser/
├── Cargo.toml      # Package manifest
├── README.md       # Project documentation
└── src/
    └── main.rs     # Implementation & unit tests
```
