//! Project 070: Augmented Interval Tree
//! Demonstrates interval trees for efficient geometric overlap queries.

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Interval {
    pub low: i32,
    pub high: i32,
}

impl Interval {
    pub fn overlaps(&self, other: &Self) -> bool {
        self.low <= other.high && other.low <= self.high
    }
}

pub struct IntervalNode {
    interval: Interval,
    max_high: i32,
    left: Option<Box<IntervalNode>>,
    right: Option<Box<IntervalNode>>,
}

pub struct IntervalTree {
    root: Option<Box<IntervalNode>>,
}

impl IntervalTree {
    pub fn new() -> Self { Self { root: None } }

    pub fn insert(&mut self, interval: Interval) {
        Self::insert_rec(&mut self.root, interval);
    }

    fn insert_rec(node: &mut Option<Box<IntervalNode>>, interval: Interval) {
        match node {
            None => {
                *node = Some(Box::new(IntervalNode {
                    interval,
                    max_high: interval.high,
                    left: None,
                    right: None,
                }));
            }
            Some(ref mut n) => {
                if interval.high > n.max_high {
                    n.max_high = interval.high;
                }
                if interval.low < n.interval.low {
                    Self::insert_rec(&mut n.left, interval);
                } else {
                    Self::insert_rec(&mut n.right, interval);
                }
            }
        }
    }

    pub fn find_overlap(&self, query: Interval) -> Option<Interval> {
        Self::find_overlap_rec(&self.root, query)
    }

    fn find_overlap_rec(node: &Option<Box<IntervalNode>>, query: Interval) -> Option<Interval> {
        let n = node.as_ref()?;
        if n.interval.overlaps(&query) {
            return Some(n.interval);
        }
        if let Some(ref left) = n.left {
            if left.max_high >= query.low {
                return Self::find_overlap_rec(&n.left, query);
            }
        }
        Self::find_overlap_rec(&n.right, query)
    }
}

fn main() {
    println!("=== 🦀 Project 070: Augmented Interval Tree ===");
    let mut tree = IntervalTree::new();
    for &(low, high) in &[(15, 20), (10, 30), (17, 19), (5, 20), (12, 15), (30, 40)] {
        tree.insert(Interval { low, high });
    }

    let query = Interval { low: 14, high: 16 };
    println!("Searching overlap for [{}-{}]:", query.low, query.high);
    if let Some(found) = tree.find_overlap(query) {
        println!("Found overlapping interval: [{}-{}]", found.low, found.high);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_overlap() {
        let mut t = IntervalTree::new();
        t.insert(Interval { low: 10, high: 20 });
        assert!(t.find_overlap(Interval { low: 15, high: 25 }).is_some());
        assert!(t.find_overlap(Interval { low: 25, high: 30 }).is_none());
    }
}
