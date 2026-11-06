//! Project 010: 2D Matrix Operations
//! Demonstrates matrix representations, validations, and matrix multiplication.

use std::fmt;

#[derive(Debug, Clone, PartialEq)]
pub struct Matrix {
    pub rows: usize,
    pub cols: usize,
    data: Vec<Vec<f64>>,
}

impl Matrix {
    pub fn new(data: Vec<Vec<f64>>) -> Result<Self, String> {
        let rows = data.len();
        if rows == 0 {
            return Err("Matrix must have at least one row".to_string());
        }
        let cols = data[0].len();
        if cols == 0 || !data.iter().all(|r| r.len() == cols) {
            return Err("All rows must have the same non-zero length".to_string());
        }
        Ok(Self { rows, cols, data })
    }

    pub fn transpose(&self) -> Self {
        let mut t = vec![vec![0.0; self.rows]; self.cols];
        for r in 0..self.rows {
            for c in 0..self.cols {
                t[c][r] = self.data[r][c];
            }
        }
        Self { rows: self.cols, cols: self.rows, data: t }
    }

    pub fn multiply(&self, other: &Self) -> Result<Self, String> {
        if self.cols != other.rows {
            return Err(format!("Dimension mismatch: {}x{} vs {}x{}", self.rows, self.cols, other.rows, other.cols));
        }
        let mut result = vec![vec![0.0; other.cols]; self.rows];
        for i in 0..self.rows {
            for j in 0..other.cols {
                let mut sum = 0.0;
                for k in 0..self.cols {
                    sum += self.data[i][k] * other.data[k][j];
                }
                result[i][j] = sum;
            }
        }
        Ok(Self { rows: self.rows, cols: other.cols, data: result })
    }
}

impl fmt::Display for Matrix {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        for row in &self.data {
            write!(f, "[ ")?;
            for val in row {
                write!(f, "{:6.2} ", val)?;
            }
            writeln!(f, "]")?;
        }
        Ok(())
    }
}

fn main() {
    println!("=== 🦀 Project 010: 2D Matrix Operations ===");
    let m1 = Matrix::new(vec![
        vec![1.0, 2.0],
        vec![3.0, 4.0],
    ]).unwrap();

    let m2 = Matrix::new(vec![
        vec![2.0, 0.0],
        vec![1.0, 2.0],
    ]).unwrap();

    println!("Matrix A:\n{}", m1);
    println!("Matrix B:\n{}", m2);
    let prod = m1.multiply(&m2).unwrap();
    println!("A x B:\n{}", prod);
    println!("Transpose of A:\n{}", m1.transpose());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_multiply() {
        let a = Matrix::new(vec![vec![1.0, 2.0], vec![3.0, 4.0]]).unwrap();
        let b = Matrix::new(vec![vec![2.0, 0.0], vec![1.0, 2.0]]).unwrap();
        let c = a.multiply(&b).unwrap();
        assert_eq!(c.data, vec![vec![4.0, 4.0], vec![10.0, 8.0]]);
    }
}
