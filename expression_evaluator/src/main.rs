//! Project 040: Abstract Syntax Tree (AST) Evaluator
//! Demonstrates recursive descent AST generation and tree evaluation.

use std::collections::HashMap;

#[derive(Debug, PartialEq, Clone)]
pub enum Expr {
    Num(f64),
    Var(String),
    Add(Box<Expr>, Box<Expr>),
    Mul(Box<Expr>, Box<Expr>),
}

impl Expr {
    pub fn eval(&self, env: &HashMap<String, f64>) -> Result<f64, String> {
        match self {
            Expr::Num(n) => Ok(*n),
            Expr::Var(name) => env.get(name).copied().ok_or_else(|| format!("Undefined variable: {}", name)),
            Expr::Add(l, r) => Ok(l.eval(env)? + r.eval(env)?),
            Expr::Mul(l, r) => Ok(l.eval(env)? * r.eval(env)?),
        }
    }
}

fn main() {
    println!("=== 🦀 Project 040: AST Evaluator ===");
    // Expression: (x + 10) * y
    let ast = Expr::Mul(
        Box::new(Expr::Add(
            Box::new(Expr::Var("x".to_string())),
            Box::new(Expr::Num(10.0)),
        )),
        Box::new(Expr::Var("y".to_string())),
    );

    let mut env = HashMap::new();
    env.insert("x".to_string(), 5.0);
    env.insert("y".to_string(), 3.0);

    let result = ast.eval(&env).unwrap();
    println!("Expression (x + 10) * y with x=5, y=3 evaluates to: {}", result);
    assert_eq!(result, 45.0);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ast_evaluation() {
        let ast = Expr::Add(Box::new(Expr::Num(2.0)), Box::new(Expr::Mul(Box::new(Expr::Num(3.0)), Box::new(Expr::Num(4.0)))));
        let env = HashMap::new();
        assert_eq!(ast.eval(&env).unwrap(), 14.0);
    }
}
