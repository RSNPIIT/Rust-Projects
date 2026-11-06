//! Project 059: Generic Binary Min-Heap
//! Demonstrates sift-up/down array heap algorithms and priority queue operations.

pub struct MinHeap<T: Ord> {
    data: Vec<T>,
}

impl<T: Ord> MinHeap<T> {
    pub fn new() -> Self {
        Self { data: Vec::new() }
    }

    pub fn push(&mut self, item: T) {
        self.data.push(item);
        self.sift_up(self.data.len() - 1);
    }

    pub fn pop(&mut self) -> Option<T> {
        if self.data.is_empty() { return None; }
        let last = self.data.len() - 1;
        self.data.swap(0, last);
        let min_val = self.data.pop();
        if !self.data.is_empty() {
            self.sift_down(0);
        }
        min_val
    }

    fn sift_up(&mut self, mut idx: usize) {
        while idx > 0 {
            let parent = (idx - 1) / 2;
            if self.data[idx] < self.data[parent] {
                self.data.swap(idx, parent);
                idx = parent;
            } else {
                break;
            }
        }
    }

    fn sift_down(&mut self, mut idx: usize) {
        let len = self.data.len();
        loop {
            let left = 2 * idx + 1;
            let right = 2 * idx + 2;
            let mut smallest = idx;

            if left < len && self.data[left] < self.data[smallest] {
                smallest = left;
            }
            if right < len && self.data[right] < self.data[smallest] {
                smallest = right;
            }
            if smallest != idx {
                self.data.swap(idx, smallest);
                idx = smallest;
            } else {
                break;
            }
        }
    }

    pub fn len(&self) -> usize { self.data.len() }
}

fn main() {
    println!("=== 🦀 Project 059: Generic Binary Min-Heap ===");
    let mut heap = MinHeap::new();
    for v in [45, 12, 89, 5, 23, 67] {
        heap.push(v);
    }

    print!("Popping in ascending order: ");
    while let Some(v) = heap.pop() {
        print!("{} ", v);
    }
    println!();
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_min_heap() {
        let mut h = MinHeap::new();
        h.push(10);
        h.push(5);
        h.push(20);
        assert_eq!(h.pop(), Some(5));
        assert_eq!(h.pop(), Some(10));
        assert_eq!(h.pop(), Some(20));
    }
}
