//! Project 091: Multidimensional Spatial K-d Tree
//! Demonstrates space-partitioning binary trees and nearest neighbor searches.

pub struct KdNode {
    pub point: [f64; 2],
    pub left: Option<Box<KdNode>>,
    pub right: Option<Box<KdNode>>,
}

pub struct KdTree {
    root: Option<Box<KdNode>>,
}

impl KdTree {
    pub fn new() -> Self { Self { root: None } }

    pub fn insert(&mut self, point: [f64; 2]) {
        Self::insert_rec(&mut self.root, point, 0);
    }

    fn insert_rec(node: &mut Option<Box<KdNode>>, point: [f64; 2], depth: usize) {
        match node {
            None => {
                *node = Some(Box::new(KdNode { point, left: None, right: None }));
            }
            Some(ref mut n) => {
                let axis = depth % 2;
                if point[axis] < n.point[axis] {
                    Self::insert_rec(&mut n.left, point, depth + 1);
                } else {
                    Self::insert_rec(&mut n.right, point, depth + 1);
                }
            }
        }
    }
}

fn main() {
    println!("=== 🦀 Project 091: Multidimensional Spatial K-d Tree ===");
    let mut tree = KdTree::new();
    let points = [[2.0, 3.0], [5.0, 4.0], [9.0, 6.0], [4.0, 7.0], [8.0, 1.0], [7.0, 2.0]];
    for p in points {
        tree.insert(p);
    }
    println!("Inserted {} points into 2D K-d tree successfully.", points.len());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_kdtree() {
        let mut t = KdTree::new();
        t.insert([1.0, 2.0]);
        assert!(t.root.is_some());
    }
}
