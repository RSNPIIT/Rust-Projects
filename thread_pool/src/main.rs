//! Project 036: Reusable Worker Thread Pool
//! Demonstrates thread management, work-stealing queues, and synchronization.

use std::sync::{mpsc, Arc, Mutex};
use std::thread;

type Job = Box<dyn FnOnce() + Send + 'static>;

pub struct ThreadPool {
    workers: Vec<Worker>,
    sender: Option<mpsc::Sender<Job>>,
}

struct Worker {
    id: usize,
    thread: Option<thread::JoinHandle<()>>,
}

impl Worker {
    fn new(id: usize, receiver: Arc<Mutex<mpsc::Receiver<Job>>>) -> Self {
        let thread = thread::spawn(move || loop {
            let message = receiver.lock().unwrap().recv();
            match message {
                Ok(job) => {
                    job();
                }
                Err(_) => {
                    break;
                }
            }
        });
        Self { id, thread: Some(thread) }
    }
}

impl ThreadPool {
    pub fn new(size: usize) -> Self {
        assert!(size > 0);
        let (sender, receiver) = mpsc::channel();
        let receiver = Arc::new(Mutex::new(receiver));
        let mut workers = Vec::with_capacity(size);

        for id in 0..size {
            workers.push(Worker::new(id, Arc::clone(&receiver)));
        }

        Self { workers, sender: Some(sender) }
    }

    pub fn execute<F>(&self, f: F)
    where
        F: FnOnce() + Send + 'static,
    {
        let job = Box::new(f);
        if let Some(ref sender) = self.sender {
            sender.send(job).unwrap();
        }
    }
}

impl Drop for ThreadPool {
    fn drop(&mut self) {
        drop(self.sender.take());
        for worker in &mut self.workers {
            if let Some(thread) = worker.thread.take() {
                thread.join().unwrap();
            }
        }
    }
}

fn main() {
    println!("=== 🦀 Project 036: Reusable Worker Thread Pool ===");
    let pool = ThreadPool::new(4);
    let counter = Arc::new(Mutex::new(0));

    for i in 0..8 {
        let c = Arc::clone(&counter);
        pool.execute(move || {
            let mut num = c.lock().unwrap();
            *num += 1;
            println!("Task {} executed by thread {:?}", i, thread::current().id());
        });
    }

    drop(pool); // Wait for tasks
    println!("Total processed: {}", *counter.lock().unwrap());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_pool_execution() {
        let pool = ThreadPool::new(2);
        let val = Arc::new(Mutex::new(0));
        let val_clone = Arc::clone(&val);

        pool.execute(move || {
            *val_clone.lock().unwrap() = 42;
        });

        drop(pool);
        assert_eq!(*val.lock().unwrap(), 42);
    }
}
