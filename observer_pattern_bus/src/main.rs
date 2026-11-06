//! Project 062: Reactive Observer Event Bus
//! Demonstrates topic-based event subscriptions with detachable subscriber IDs.

use std::collections::HashMap;

pub type Subscriber = Box<dyn Fn(&str) + Send + Sync>;

pub struct EventBus {
    topics: HashMap<String, Vec<(usize, Subscriber)>>,
    next_id: usize,
}

impl EventBus {
    pub fn new() -> Self {
        Self { topics: HashMap::new(), next_id: 1 }
    }

    pub fn subscribe<F>(&mut self, topic: &str, handler: F) -> usize
    where
        F: Fn(&str) + Send + Sync + 'static,
    {
        let id = self.next_id;
        self.next_id += 1;
        self.topics.entry(topic.to_string()).or_default().push((id, Box::new(handler)));
        id
    }

    pub fn unsubscribe(&mut self, topic: &str, sub_id: usize) {
        if let Some(list) = self.topics.get_mut(topic) {
            list.retain(|(id, _)| *id != sub_id);
        }
    }

    pub fn publish(&self, topic: &str, message: &str) {
        if let Some(subscribers) = self.topics.get(topic) {
            for (_, handler) in subscribers {
                handler(message);
            }
        }
    }
}

fn main() {
    println!("=== 🦀 Project 062: Reactive Observer Event Bus ===");
    let mut bus = EventBus::new();
    let sub1 = bus.subscribe("alerts", |msg| println!("[Sub1] Alert: {}", msg));
    let _sub2 = bus.subscribe("alerts", |msg| println!("[Sub2] Alert: {}", msg));

    bus.publish("alerts", "Service degradation detected");
    bus.unsubscribe("alerts", sub1);
    println!("After Sub1 unsubscribe:");
    bus.publish("alerts", "Service fully restored");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_pubsub() {
        let mut bus = EventBus::new();
        let sub = bus.subscribe("test", |_| {});
        assert_eq!(bus.topics["test"].len(), 1);
        bus.unsubscribe("test", sub);
        assert_eq!(bus.topics["test"].len(), 0);
    }
}
