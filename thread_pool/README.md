# 🦀 Reusable Worker Thread Pool (`036_thread_pool`)

**Difficulty:** 🟡 Intermediate  
**Category:** Concurrency & Systems  

---

## 📖 Overview

Multi-threaded worker pool dispatching closures across OS threads using synchronized mpsc channels.

---

## 🎯 Key Rust Concepts Demonstrated

- **Arc<Mutex<Receiver<T>>>**
- **mpsc Channels**
- **Thread Spawning & JoinHandles**
- **Graceful Shutdown / Drop Trait**

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
036_thread_pool/
├── Cargo.toml      # Package manifest
├── README.md       # Project documentation
└── src/
    └── main.rs     # Implementation & unit tests
```
