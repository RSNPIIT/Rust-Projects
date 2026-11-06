//! Project 004: CLI Calculator
//! Demonstrates tokenization, Shunting-yard algorithm, and RPN stack evaluation.

#[derive(Debug, PartialEq, Clone)]
pub enum Token {
    Number(f64),
    Plus,
    Minus,
    Multiply,
    Divide,
    LParen,
    RParen,
}

pub fn tokenize(expr: &str) -> Result<Vec<Token>, String> {
    let mut tokens = Vec::new();
    let mut chars = expr.chars().peekable();

    while let Some(&c) = chars.peek() {
        match c {
            ' ' | '\t' | '\n' => { chars.next(); }
            '+' => { tokens.push(Token::Plus); chars.next(); }
            '-' => { tokens.push(Token::Minus); chars.next(); }
            '*' => { tokens.push(Token::Multiply); chars.next(); }
            '/' => { tokens.push(Token::Divide); chars.next(); }
            '(' => { tokens.push(Token::LParen); chars.next(); }
            ')' => { tokens.push(Token::RParen); chars.next(); }
            '0'..='9' | '.' => {
                let mut num_str = String::new();
                while let Some(&ch) = chars.peek() {
                    if ch.is_digit(10) || ch == '.' {
                        num_str.push(ch);
                        chars.next();
                    } else {
                        break;
                    }
                }
                let val = num_str.parse::<f64>().map_err(|e| e.to_string())?;
                tokens.push(Token::Number(val));
            }
            other => return Err(format!("Unexpected character: {}", other)),
        }
    }
    Ok(tokens)
}

fn precedence(op: &Token) -> u8 {
    match op {
        Token::Plus | Token::Minus => 1,
        Token::Multiply | Token::Divide => 2,
        _ => 0,
    }
}

pub fn evaluate(expr: &str) -> Result<f64, String> {
    let tokens = tokenize(expr)?;
    let mut output: Vec<Token> = Vec::new();
    let mut ops: Vec<Token> = Vec::new();

    for token in tokens {
        match token {
            Token::Number(_) => output.push(token),
            Token::Plus | Token::Minus | Token::Multiply | Token::Divide => {
                while let Some(top) = ops.last() {
                    if precedence(top) >= precedence(&token) && *top != Token::LParen {
                        output.push(ops.pop().unwrap());
                    } else {
                        break;
                    }
                }
                ops.push(token);
            }
            Token::LParen => ops.push(token),
            Token::RParen => {
                let mut matched = false;
                while let Some(top) = ops.pop() {
                    if top == Token::LParen {
                        matched = true;
                        break;
                    }
                    output.push(top);
                }
                if !matched {
                    return Err("Mismatched parenthesis".to_string());
                }
            }
        }
    }

    while let Some(op) = ops.pop() {
        if op == Token::LParen || op == Token::RParen {
            return Err("Mismatched parenthesis".to_string());
        }
        output.push(op);
    }

    // Evaluate RPN
    let mut stack: Vec<f64> = Vec::new();
    for token in output {
        match token {
            Token::Number(n) => stack.push(n),
            Token::Plus => {
                let b = stack.pop().ok_or("Invalid expression")?;
                let a = stack.pop().ok_or("Invalid expression")?;
                stack.push(a + b);
            }
            Token::Minus => {
                let b = stack.pop().ok_or("Invalid expression")?;
                let a = stack.pop().ok_or("Invalid expression")?;
                stack.push(a - b);
            }
            Token::Multiply => {
                let b = stack.pop().ok_or("Invalid expression")?;
                let a = stack.pop().ok_or("Invalid expression")?;
                stack.push(a * b);
            }
            Token::Divide => {
                let b = stack.pop().ok_or("Invalid expression")?;
                let a = stack.pop().ok_or("Invalid expression")?;
                if b == 0.0 { return Err("Division by zero".to_string()); }
                stack.push(a / b);
            }
            _ => unreachable!(),
        }
    }

    stack.pop().ok_or("Empty expression".to_string())
}

fn main() {
    println!("=== 🦀 Project 004: CLI Calculator ===");
    let expressions = [
        "3 + 5 * 2",
        "(10 + 20) / (4 - 2)",
        "100 - 25 * 3 + 12 / 4",
    ];

    for expr in expressions {
        match evaluate(expr) {
            Ok(res) => println!("{} = {}", expr, res),
            Err(e) => println!("Error evaluating '{}': {}", expr, e),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_calc_precedence() {
        assert_eq!(evaluate("2 + 3 * 4").unwrap(), 14.0);
        assert_eq!(evaluate("(2 + 3) * 4").unwrap(), 20.0);
        assert_eq!(evaluate("10 / 2 - 3").unwrap(), 2.0);
    }
}
