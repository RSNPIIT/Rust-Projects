//! Project 080: Compiler Lexer & Parser
//! Demonstrates compiler front-end scanning, parsing, and AST construction.

#[derive(Debug, PartialEq, Clone)]
pub enum Token {
    Let,
    Ident(String),
    Assign,
    Int(i64),
    Semicolon,
}

pub fn lex(code: &str) -> Vec<Token> {
    let mut tokens = Vec::new();
    let mut chars = code.chars().peekable();

    while let Some(&c) = chars.peek() {
        match c {
            ' ' | '\t' | '\n' => { chars.next(); }
            '=' => { tokens.push(Token::Assign); chars.next(); }
            ';' => { tokens.push(Token::Semicolon); chars.next(); }
            'a'..='z' | 'A'..='Z' => {
                let mut s = String::new();
                while let Some(&ch) = chars.peek() {
                    if ch.is_alphanumeric() { s.push(ch); chars.next(); } else { break; }
                }
                if s == "let" { tokens.push(Token::Let); } else { tokens.push(Token::Ident(s)); }
            }
            '0'..='9' => {
                let mut n = 0i64;
                while let Some(&ch) = chars.peek() {
                    if let Some(d) = ch.to_digit(10) { n = n * 10 + d as i64; chars.next(); } else { break; }
                }
                tokens.push(Token::Int(n));
            }
            _ => { chars.next(); }
        }
    }
    tokens
}

#[derive(Debug, PartialEq)]
pub struct LetStatement {
    pub var_name: String,
    pub value: i64,
}

pub fn parse_let(tokens: &[Token]) -> Result<LetStatement, &'static str> {
    if tokens.len() < 5 { return Err("Insufficient tokens for let statement"); }
    if tokens[0] != Token::Let { return Err("Expected 'let'"); }
    let var_name = match &tokens[1] { Token::Ident(s) => s.clone(), _ => return Err("Expected identifier") };
    if tokens[2] != Token::Assign { return Err("Expected '='"); }
    let value = match tokens[3] { Token::Int(n) => n, _ => return Err("Expected integer literal") };
    if tokens[4] != Token::Semicolon { return Err("Expected ';'"); }
    Ok(LetStatement { var_name, value })
}

fn main() {
    println!("=== 🦀 Project 080: Compiler Lexer & Parser ===");
    let source = "let port = 8080;";
    let tokens = lex(source);
    println!("Tokens: {:?}", tokens);
    let ast = parse_let(&tokens).unwrap();
    println!("Parsed AST Statement: {:?}", ast);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_lexer_parser() {
        let t = lex("let x = 42;");
        let stmt = parse_let(&t).unwrap();
        assert_eq!(stmt.var_name, "x");
        assert_eq!(stmt.value, 42);
    }
}
