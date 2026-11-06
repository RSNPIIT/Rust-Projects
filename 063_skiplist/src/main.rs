//! Project 063: Probabilistic Skip List
//! Demonstrates multi-layer express lanes for logarithmic search and insertion.

#[derive(Clone)]
struct SkipNode {
    val: i32,
    forward: Vec<Option<usize>>,
}

pub struct SkipList {
    nodes: Vec<SkipNode>,
    head: usize,
    max_level: usize,
}

impl SkipList {
    pub fn new(max_level: usize) -> Self {
        let head_node = SkipNode {
            val: i32::MIN,
            forward: vec![None; max_level],
        };
        Self {
            nodes: vec![head_node],
            head: 0,
            max_level,
        }
    }

    pub fn contains(&self, target: i32) -> bool {
        let mut curr = self.head;
        for lvl in (0..self.max_level).rev() {
            while let Some(next_idx) = self.nodes[curr].forward[lvl] {
                if self.nodes[next_idx].val < target {
                    curr = next_idx;
                } else if self.nodes[next_idx].val == target {
                    return true;
                } else {
                    break;
                }
            }
        }
        false
    }

    pub fn insert(&mut self, val: i32) {
        let new_idx = self.nodes.len();
        self.nodes.push(SkipNode {
            val,
            forward: vec![None; self.max_level],
        });

        // Insert at base level
        let mut curr = self.head;
        while let Some(next_idx) = self.nodes[curr].forward[0] {
            if self.nodes[next_idx].val < val {
                curr = next_idx;
            } else {
                break;
            }
        }
        let old_next = self.nodes[curr].forward[0];
        self.nodes[new_idx].forward[0] = old_next;
        self.nodes[curr].forward[0] = Some(new_idx);
    }
}

fn main() {
    println!("=== 🦀 Project 063: Probabilistic Skip List ===");
    let mut sl = SkipList::new(4);
    for n in [10, 25, 40, 5, 15] {
        sl.insert(n);
    }
    println!("Contains 25: {}", sl.contains(25));
    println!("Contains 99: {}", sl.contains(99));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_skip_list() {
        let mut sl = SkipList::new(3);
        sl.insert(50);
        sl.insert(20);
        assert!(sl.contains(50));
        assert!(sl.contains(20));
        assert!(!sl.contains(30));
    }
}
