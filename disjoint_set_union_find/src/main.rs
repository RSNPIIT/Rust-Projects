//! Project 094: Disjoint-Set Union-Find
//! Demonstrates near O(1) amortized set merging and cycle detection.

pub struct UnionFind {
    parent: Vec<usize>,
    rank: Vec<usize>,
}

impl UnionFind {
    pub fn new(size: usize) -> Self {
        Self {
            parent: (0..size).collect(),
            rank: vec![0; size],
        }
    }

    pub fn find(&mut self, mut i: usize) -> usize {
        let mut root = i;
        while root != self.parent[root] {
            root = self.parent[root];
        }
        // Path compression
        while i != root {
            let next = self.parent[i];
            self.parent[i] = root;
            i = next;
        }
        root
    }

    pub fn union(&mut self, i: usize, j: usize) -> bool {
        let root_i = self.find(i);
        let root_j = self.find(j);
        if root_i == root_j {
            return false; // Already in same set (cycle)
        }

        if self.rank[root_i] < self.rank[root_j] {
            self.parent[root_i] = root_j;
        } else if self.rank[root_i] > self.rank[root_j] {
            self.parent[root_j] = root_i;
        } else {
            self.parent[root_j] = root_i;
            self.rank[root_i] += 1;
        }
        true
    }
}

fn main() {
    println!("=== 🦀 Project 094: Disjoint-Set Union-Find ===");
    let mut uf = UnionFind::new(5);
    uf.union(0, 1);
    uf.union(1, 2);

    println!("0 connected to 2? {}", uf.find(0) == uf.find(2));
    println!("0 connected to 3? {}", uf.find(0) == uf.find(3));
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_dsu() {
        let mut uf = UnionFind::new(4);
        assert!(uf.union(0, 1));
        assert!(!uf.union(0, 1)); // duplicate
    }
}
