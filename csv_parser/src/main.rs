//! Project 017: Robust CSV Table Parser
//! Demonstrates state-machine based CSV parsing handling escaped quotes and commas.

#[derive(Debug, PartialEq, Clone)]
pub struct CsvTable {
    pub headers: Vec<String>,
    pub rows: Vec<Vec<String>>,
}

pub fn parse_csv_line(line: &str) -> Vec<String> {
    let mut fields = Vec::new();
    let mut field = String::new();
    let mut in_quotes = false;
    let mut chars = line.chars().peekable();

    while let Some(c) = chars.next() {
        match c {
            '"' => {
                if in_quotes && chars.peek() == Some(&'"') {
                    field.push('"');
                    chars.next();
                } else {
                    in_quotes = !in_quotes;
                }
            }
            ',' if !in_quotes => {
                fields.push(field.trim().to_string());
                field = String::new();
            }
            _ => field.push(c),
        }
    }
    fields.push(field.trim().to_string());
    fields
}

pub fn parse_csv(content: &str) -> Option<CsvTable> {
    let mut lines = content.lines().filter(|l| !l.trim().is_empty());
    let header_line = lines.next()?;
    let headers = parse_csv_line(header_line);
    let mut rows = Vec::new();

    for line in lines {
        rows.push(parse_csv_line(line));
    }

    Some(CsvTable { headers, rows })
}

fn main() {
    println!("=== 🦀 Project 017: Robust CSV Table Parser ===");
    let sample = "id,name,role\n1,\"Doe, John\",Admin\n2,Jane Smith,Developer\n3,\"Special \"\"Alias\"\"\",User";
    let table = parse_csv(sample).unwrap();
    println!("Headers: {:?}", table.headers);
    for row in table.rows {
        println!("Row: {:?}", row);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_csv_quoting() {
        let line = r#"10,"Hello, World",42"#;
        let parsed = parse_csv_line(line);
        assert_eq!(parsed, vec!["10", "Hello, World", "42"]);
    }
}
