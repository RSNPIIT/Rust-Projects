//! Project 044: Dijkstra's Shortest Path Algorithm
//! Demonstrates graph representation and greedy shortest-path searching.

use std::cmp::Ordering;
use std::collections::{BinaryHeap, HashMap};

#[derive(Copy, Clone, Eq, PartialEq)]
struct State {
    cost: usize,
    position: usize,
}

impl Ord for State {
    fn cmp(&self, other: &Self) -> Ordering {
        other.cost.cmp(&self.cost)
    }
}

impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

pub struct Edge {
    pub node: usize,
    pub cost: usize,
}

pub fn shortest_path(adj_list: &[Vec<Edge>], start: usize, goal: usize) -> Option<usize> {
    let mut dist: Vec<usize> = (0..adj_list.len()).map(|_| usize::MAX).collect();
    let mut heap = BinaryHeap::new();

    dist[start] = 0;
    heap.push(State { cost: 0, position: start });

    while let Some(State { cost, position }) = heap.pop() {
        if position == goal { return Some(cost); }
        if cost > dist[position] { continue; }

        for edge in &adj_list[position] {
            let next_cost = cost + edge.cost;
            if next_cost < dist[edge.node] {
                dist[edge.node] = next_cost;
                heap.push(State { cost: next_cost, position: edge.node });
            }
        }
    }
    None
}

fn main() {
    println!("=== 🦀 Project 044: Dijkstra's Shortest Path ===");
    let graph = vec![
        vec![Edge { node: 1, cost: 4 }, Edge { node: 2, cost: 2 }],
        vec![Edge { node: 3, cost: 5 }],
        vec![Edge { node: 1, cost: 1 }, Edge { node: 3, cost: 8 }],
        vec![],
    ];

    let cost = shortest_path(&graph, 0, 3).unwrap();
    println!("Shortest path cost from Node 0 to Node 3: {}", cost);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_dijkstra() {
        let graph = vec![
            vec![Edge { node: 1, cost: 10 }, Edge { node: 2, cost: 3 }],
            vec![Edge { node: 3, cost: 2 }],
            vec![Edge { node: 1, cost: 1 }],
            vec![],
        ];
        assert_eq!(shortest_path(&graph, 0, 3), Some(6));
    }
}
