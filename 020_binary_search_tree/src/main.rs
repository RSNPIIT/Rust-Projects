//! Project 020: Binary Search Tree
//! Demonstrates recursive boxed node structures and tree traversals.

#[derive(Debug)]
pub struct TreeNode<T: Ord> {
    pub val: T,
    pub left: Option<Box<TreeNode<T>>>,
    pub right: Option<Box<TreeNode<T>>>,
}

#[derive(Debug, Default)]
pub struct BinarySearchTree<T: Ord> {
    root: Option<Box<TreeNode<T>>>,
}

impl<T: Ord + Copy> BinarySearchTree<T> {
    pub fn new() -> Self {
        Self { root: None }
    }

    pub fn insert(&mut self, val: T) {
        Self::insert_rec(&mut self.root, val);
    }

    fn insert_rec(node: &mut Option<Box<TreeNode<T>>>, val: T) {
        match node {
            None => {
                *node = Some(Box::new(TreeNode { val, left: None, right: None }));
            }
            Some(ref mut n) => {
                if val < n.val {
                    Self::insert_rec(&mut n.left, val);
                } else if val > n.val {
                    Self::insert_rec(&mut n.right, val);
                }
            }
        }
    }

    pub fn contains(&self, val: T) -> bool {
        let mut curr = &self.root;
        while let Some(n) = curr {
            if val == n.val {
                return true;
            } else if val < n.val {
                curr = &n.left;
            } else {
                curr = &n.right;
            }
        }
        false
    }

    pub fn in_order(&self) -> Vec<T> {
        let mut acc = Vec::new();
        Self::in_order_rec(&self.root, &mut acc);
        acc
    }

    fn in_order_rec(node: &Option<Box<TreeNode<T>>>, acc: &mut Vec<T>) {
        if let Some(n) = node {
            Self::in_order_rec(&n.left, acc);
            acc.push(n.val);
            Self::in_order_rec(&n.right, acc);
        }
    }
}

fn main() {
    println!("=== 🦀 Project 020: Binary Search Tree ===");
    let mut bst = BinarySearchTree::new();
    for v in [50, 30, 70, 20, 40, 60, 80] {
        bst.insert(v);
    }
    println!("In-order traversal: {:?}", bst.in_order());
    println!("Contains 40: {}", bst.contains(40));
    println!("Contains 99: {}", bst.contains(99));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_bst() {
        let mut tree = BinarySearchTree::new();
        tree.insert(5);
        tree.insert(3);
        tree.insert(8);
        assert!(tree.contains(3));
        assert!(!tree.contains(10));
        assert_eq!(tree.in_order(), vec![3, 5, 8]);
    }
}
