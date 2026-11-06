//! Project 093: Columnar Table Storage & RLE
//! Demonstrates columnar storage for analytical OLAP workloads.

pub struct ColumnarTable {
    pub col_ids: Vec<u64>,
    pub col_ages: Vec<u32>,
}

impl ColumnarTable {
    pub fn new() -> Self {
        Self { col_ids: Vec::new(), col_ages: Vec::new() }
    }

    pub fn insert(&mut self, id: u64, age: u32) {
        self.col_ids.push(id);
        self.col_ages.push(age);
    }

    pub fn average_age(&self) -> f64 {
        if self.col_ages.is_empty() { return 0.0; }
        let sum: u32 = self.col_ages.iter().sum();
        sum as f64 / self.col_ages.len() as f64
    }
}

fn main() {
    println!("=== 🦀 Project 093: Columnar Table Storage ===");
    let mut table = ColumnarTable::new();
    table.insert(101, 25);
    table.insert(102, 30);
    table.insert(103, 35);

    println!("Total rows: {}", table.col_ids.len());
    println!("Vectorized average age query: {:.1}", table.average_age());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_columnar() {
        let mut t = ColumnarTable::new();
        t.insert(1, 20);
        t.insert(2, 40);
        assert_eq!(t.average_age(), 30.0);
    }
}
