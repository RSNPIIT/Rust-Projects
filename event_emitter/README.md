# 🦀 Type-Safe Event Dispatcher (`042_event_emitter`)

**Difficulty:** 🟡 Intermediate  
**Category:** Design Patterns  

---

## 📖 Overview

Decoupled observer event bus registering callbacks and dispatching typed payload notifications.

---

## 🎯 Key Rust Concepts Demonstrated

- **Closures as Trait Objects `Box<dyn Fn>`**
- **Observer Pattern**
- **Type Safety**
- **Handler Subscription**

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
042_event_emitter/
├── Cargo.toml      # Package manifest
├── README.md       # Project documentation
└── src/
    └── main.rs     # Implementation & unit tests
```
