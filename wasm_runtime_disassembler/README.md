# 🦀 WebAssembly Binary Disassembler (`081_wasm_runtime_disassembler`)

**Difficulty:** 🔴 Advanced  
**Category:** Virtual Machines & Binary  

---

## 📖 Overview

WebAssembly (.wasm) binary reader validating magic number, version, section IDs, and decoding opcode streams.

---

## 🎯 Key Rust Concepts Demonstrated

- **Wasm Binary Specification**
- **Magic Number Verification `\0asm`**
- **Section ID Headers**
- **Bytecode Disassembly**

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
081_wasm_runtime_disassembler/
├── Cargo.toml      # Package manifest
├── README.md       # Project documentation
└── src/
    └── main.rs     # Implementation & unit tests
```
