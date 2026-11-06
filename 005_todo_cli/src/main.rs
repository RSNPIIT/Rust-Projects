//! Project 005: To-Do CLI Manager
//! Demonstrates state management, enum priorities, and filtered listings.

use std::fmt;

#[derive(Debug, PartialEq, Clone, Copy)]
pub enum Priority {
    Low,
    Medium,
    High,
}

#[derive(Debug, Clone)]
pub struct Task {
    pub id: usize,
    pub title: String,
    pub completed: bool,
    pub priority: Priority,
}

pub struct TodoList {
    tasks: Vec<Task>,
    next_id: usize,
}

impl TodoList {
    pub fn new() -> Self {
        Self { tasks: Vec::new(), next_id: 1 }
    }

    pub fn add(&mut self, title: &str, priority: Priority) -> usize {
        let id = self.next_id;
        self.next_id += 1;
        self.tasks.push(Task {
            id,
            title: title.to_string(),
            completed: false,
            priority,
        });
        id
    }

    pub fn complete(&mut self, id: usize) -> bool {
        if let Some(task) = self.tasks.iter_mut().find(|t| t.id == id) {
            task.completed = true;
            true
        } else {
            false
        }
    }

    pub fn remove(&mut self, id: usize) -> bool {
        let initial_len = self.tasks.len();
        self.tasks.retain(|t| t.id != id);
        self.tasks.len() < initial_len
    }

    pub fn filter_by_priority(&self, priority: Priority) -> Vec<&Task> {
        self.tasks.iter().filter(|t| t.priority == priority).collect()
    }
}

impl fmt::Display for TodoList {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        writeln!(f, "{:<4} {:<6} {:<8} {}", "ID", "STATUS", "PRIORITY", "TITLE")?;
        writeln!(f, "{}", "-".repeat(45))?;
        for task in &self.tasks {
            let status = if task.completed { "[x]" } else { "[ ]" };
            let prio = match task.priority {
                Priority::Low => "Low",
                Priority::Medium => "Medium",
                Priority::High => "High",
            };
            writeln!(f, "{:<4} {:<6} {:<8} {}", task.id, status, prio, task.title)?;
        }
        Ok(())
    }
}

fn main() {
    println!("=== 🦀 Project 005: To-Do CLI Manager ===");
    let mut todo = TodoList::new();
    let id1 = todo.add("Learn Rust ownership", Priority::High);
    let id2 = todo.add("Write unit tests", Priority::Medium);
    let _id3 = todo.add("Publish open source repo", Priority::Low);

    println!("Initial Task List:\n{}", todo);

    todo.complete(id1);
    println!("After Completing Task {}:\n{}", id1, todo);

    todo.remove(id2);
    println!("After Removing Task {}:\n{}", id2, todo);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_todo_crud() {
        let mut list = TodoList::new();
        let id = list.add("Write code", Priority::High);
        assert!(!list.tasks[0].completed);
        assert!(list.complete(id));
        assert!(list.tasks[0].completed);
        assert!(list.remove(id));
        assert_eq!(list.tasks.len(), 0);
    }
}
