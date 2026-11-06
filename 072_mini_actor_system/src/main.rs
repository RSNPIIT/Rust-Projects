//! Project 072: Mini Actor Model Concurrency System
//! Demonstrates the actor model, isolated state, and message passing concurrency.

use std::sync::mpsc::{channel, Sender};
use std::thread;

pub enum CounterMessage {
    Increment(u64),
    Get(Sender<u64>),
    Stop,
}

pub struct CounterActor {
    sender: Sender<CounterMessage>,
    handle: thread::JoinHandle<()>,
}

impl CounterActor {
    pub fn start() -> Self {
        let (tx, rx) = channel::<CounterMessage>();
        let handle = thread::spawn(move || {
            let mut state: u64 = 0;
            while let Ok(msg) = rx.recv() {
                match msg {
                    CounterMessage::Increment(n) => state += n,
                    CounterMessage::Get(reply_to) => { let _ = reply_to.send(state); },
                    CounterMessage::Stop => break,
                }
            }
        });
        Self { sender: tx, handle }
    }

    pub fn send(&self, msg: CounterMessage) {
        let _ = self.sender.send(msg);
    }

    pub fn get_value(&self) -> u64 {
        let (tx, rx) = channel();
        self.send(CounterMessage::Get(tx));
        rx.recv().unwrap()
    }

    pub fn stop(self) {
        self.send(CounterMessage::Stop);
        self.handle.join().unwrap();
    }
}

fn main() {
    println!("=== 🦀 Project 072: Mini Actor Model ===");
    let actor = CounterActor::start();
    actor.send(CounterMessage::Increment(10));
    actor.send(CounterMessage::Increment(32));

    println!("Current Actor Counter State: {}", actor.get_value());
    actor.stop();
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_actor() {
        let actor = CounterActor::start();
        actor.send(CounterMessage::Increment(5));
        assert_eq!(actor.get_value(), 5);
        actor.stop();
    }
}
