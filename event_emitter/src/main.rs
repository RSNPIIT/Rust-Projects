//! Project 042: Type-Safe Event Dispatcher
//! Demonstrates the observer pattern and dynamic closure callback handlers.

use std::collections::HashMap;

type Callback = Box<dyn Fn(&str)>;

#[derive(Default)]
pub struct EventEmitter {
    listeners: HashMap<String, Vec<Callback>>,
}

impl EventEmitter {
    pub fn new() -> Self {
        Self { listeners: HashMap::new() }
    }

    pub fn on<F>(&mut self, event: &str, handler: F)
    where
        F: Fn(&str) + 'static,
    {
        self.listeners.entry(event.to_string()).or_default().push(Box::new(handler));
    }

    pub fn emit(&self, event: &str, data: &str) {
        if let Some(handlers) = self.listeners.get(event) {
            for handler in handlers {
                handler(data);
            }
        }
    }
}

fn main() {
    println!("=== 🦀 Project 042: Type-Safe Event Dispatcher ===");
    let mut emitter = EventEmitter::new();

    emitter.on("user_signup", |payload| {
        println!("[Audit Service] User registered: {}", payload);
    });

    emitter.on("user_signup", |payload| {
        println!("[Email Service] Welcome email dispatched to: {}", payload);
    });

    emitter.emit("user_signup", "alice@example.com");
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::{Arc, Mutex};

    #[test]
    fn test_event_dispatch() {
        let mut emitter = EventEmitter::new();
        let received = Arc::new(Mutex::new(false));
        let recv_clone = Arc::clone(&received);

        emitter.on("ping", move |_| {
            *recv_clone.lock().unwrap() = true;
        });

        emitter.emit("ping", "data");
        assert!(*received.lock().unwrap());
    }
}
