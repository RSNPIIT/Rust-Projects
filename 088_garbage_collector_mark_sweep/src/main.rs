//! Project 088: Tracing Mark-and-Sweep Garbage Collector
//! Demonstrates managed heap allocation, root tracing, and memory reclamation.

struct GcObject {
    marked: bool,
    references: Vec<usize>,
}

pub struct GcHeap {
    objects: Vec<Option<GcObject>>,
}

impl GcHeap {
    pub fn new() -> Self {
        Self { objects: Vec::new() }
    }

    pub fn allocate(&mut self) -> usize {
        let id = self.objects.len();
        self.objects.push(Some(GcObject { marked: false, references: Vec::new() }));
        id
    }

    pub fn add_reference(&mut self, from: usize, to: usize) {
        if let Some(Some(ref mut obj)) = self.objects.get_mut(from) {
            obj.references.push(to);
        }
    }

    pub fn collect(&mut self, roots: &[usize]) -> usize {
        // Mark
        for &root in roots {
            self.mark(root);
        }

        // Sweep
        let mut reclaimed = 0;
        for obj in self.objects.iter_mut() {
            if let Some(ref mut o) = obj {
                if !o.marked {
                    *obj = None;
                    reclaimed += 1;
                } else {
                    o.marked = false; // Reset mark
                }
            }
        }
        reclaimed
    }

    fn mark(&mut self, id: usize) {
        if let Some(Some(ref mut obj)) = self.objects.get_mut(id) {
            if !obj.marked {
                obj.marked = true;
                let refs = obj.references.clone();
                for child in refs {
                    self.mark(child);
                }
            }
        }
    }
}

fn main() {
    println!("=== 🦀 Project 088: Mark-and-Sweep Garbage Collector ===");
    let mut heap = GcHeap::new();
    let root = heap.allocate();
    let child1 = heap.allocate();
    let garbage = heap.allocate();

    heap.add_reference(root, child1);
    println!("Heap objects: {}", heap.objects.len());

    let freed = heap.collect(&[root]);
    println!("Reclaimed unreachable objects: {}", freed);
    assert_eq!(freed, 1);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_gc() {
        let mut heap = GcHeap::new();
        let r = heap.allocate();
        let _g = heap.allocate();
        let freed = heap.collect(&[r]);
        assert_eq!(freed, 1);
    }
}
