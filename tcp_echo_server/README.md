# 🦀 Concurrent TCP Echo Server (`049_tcp_echo_server`)

**Difficulty:** 🟡 Intermediate  
**Category:** Networking & I/O  

---

## 📖 Overview

Multi-threaded TCP network server accepting concurrent client streams and echoing back payload bytes.

---

## 🎯 Key Rust Concepts Demonstrated

- **std::net::TcpListener**
- **std::net::TcpStream**
- **Thread Spawning per Client**
- **Network Stream I/O**

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
049_tcp_echo_server/
├── Cargo.toml      # Package manifest
├── README.md       # Project documentation
└── src/
    └── main.rs     # Implementation & unit tests
```
