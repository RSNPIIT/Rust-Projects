//! Project 034: Exact Rational Fraction Arithmetic
//! Demonstrates operator overloading, GCD reduction, and exact math.

use std::ops::{Add, Div, Mul, Sub};
use std::fmt;

fn gcd(mut a: i64, mut b: i64) -> i64 {
    a = a.abs();
    b = b.abs();
    while b != 0 {
        let t = b;
        b = a % b;
        a = t;
    }
    a
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Fraction {
    pub num: i64,
    pub den: i64,
}

impl Fraction {
    pub fn new(mut num: i64, mut den: i64) -> Result<Self, &'static str> {
        if den == 0 {
            return Err("Denominator cannot be zero");
        }
        if den < 0 {
            num = -num;
            den = -den;
        }
        let g = gcd(num, den);
        Ok(Self { num: num / g, den: den / g })
    }
}

impl Add for Fraction {
    type Output = Self;
    fn add(self, rhs: Self) -> Self::Output {
        Self::new(self.num * rhs.den + rhs.num * self.den, self.den * rhs.den).unwrap()
    }
}

impl Sub for Fraction {
    type Output = Self;
    fn sub(self, rhs: Self) -> Self::Output {
        Self::new(self.num * rhs.den - rhs.num * self.den, self.den * rhs.den).unwrap()
    }
}

impl Mul for Fraction {
    type Output = Self;
    fn mul(self, rhs: Self) -> Self::Output {
        Self::new(self.num * rhs.num, self.den * rhs.den).unwrap()
    }
}

impl Div for Fraction {
    type Output = Self;
    fn div(self, rhs: Self) -> Self::Output {
        Self::new(self.num * rhs.den, self.den * rhs.num).unwrap()
    }
}

impl fmt::Display for Fraction {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        if self.den == 1 {
            write!(f, "{}", self.num)
        } else {
            write!(f, "{}/{}", self.num, self.den)
        }
    }
}

fn main() {
    println!("=== 🦀 Project 034: Exact Rational Fraction Arithmetic ===");
    let f1 = Fraction::new(1, 3).unwrap();
    let f2 = Fraction::new(1, 6).unwrap();

    println!("{} + {} = {}", f1, f2, f1 + f2);
    println!("{} - {} = {}", f1, f2, f1 - f2);
    println!("{} * {} = {}", f1, f2, f1 * f2);
    println!("{} / {} = {}", f1, f2, f1 / f2);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_fraction_math() {
        let a = Fraction::new(1, 2).unwrap();
        let b = Fraction::new(1, 3).unwrap();
        assert_eq!(a + b, Fraction::new(5, 6).unwrap());
        assert_eq!(a * b, Fraction::new(1, 6).unwrap());
    }
}
