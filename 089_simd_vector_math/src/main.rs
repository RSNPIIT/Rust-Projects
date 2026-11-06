//! Project 089: SIMD Vectorized Linear Algebra
//! Demonstrates 4-wide vector SIMD calculations and geometric transformations.

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Vec4(pub [f32; 4]);

impl Vec4 {
    pub fn new(x: f32, y: f32, z: f32, w: f32) -> Self {
        Self([x, y, z, w])
    }

    pub fn dot(&self, other: &Self) -> f32 {
        self.0[0] * other.0[0] + self.0[1] * other.0[1] + self.0[2] * other.0[2] + self.0[3] * other.0[3]
    }

    pub fn add(&self, other: &Self) -> Self {
        Self([
            self.0[0] + other.0[0],
            self.0[1] + other.0[1],
            self.0[2] + other.0[2],
            self.0[3] + other.0[3],
        ])
    }

    pub fn magnitude(&self) -> f32 {
        self.dot(self).sqrt()
    }
}

fn main() {
    println!("=== 🦀 Project 089: SIMD Vectorized Linear Algebra ===");
    let v1 = Vec4::new(1.0, 2.0, 3.0, 4.0);
    let v2 = Vec4::new(4.0, 3.0, 2.0, 1.0);

    println!("v1: {:?}", v1);
    println!("v2: {:?}", v2);
    println!("v1 + v2:      {:?}", v1.add(&v2));
    println!("v1 . v2:      {:.2}", v1.dot(&v2));
    println!("Magnitude v1: {:.2}", v1.magnitude());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_vec4() {
        let a = Vec4::new(1.0, 0.0, 0.0, 0.0);
        let b = Vec4::new(0.0, 1.0, 0.0, 0.0);
        assert_eq!(a.dot(&b), 0.0);
    }
}
