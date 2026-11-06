//! Project 067: CLI Argument Parser from Scratch
//! Demonstrates zero-dependency CLI option and flag extraction.

use std::collections::{HashMap, HashSet};

#[derive(Default, Debug)]
pub struct CliArgs {
    pub flags: HashSet<String>,
    pub options: HashMap<String, String>,
    pub positionals: Vec<String>,
}

pub fn parse_args(args: &[String]) -> CliArgs {
    let mut parsed = CliArgs::default();
    let mut i = 0;

    while i < args.len() {
        let arg = &args[i];
        if arg.starts_with("--") {
            let opt = &arg[2..];
            if let Some((k, v)) = opt.split_once('=') {
                parsed.options.insert(k.to_string(), v.to_string());
            } else if i + 1 < args.len() && !args[i + 1].starts_with('-') {
                parsed.options.insert(opt.to_string(), args[i + 1].clone());
                i += 1;
            } else {
                parsed.flags.insert(opt.to_string());
            }
        } else if arg.starts_with('-') && arg.len() > 1 {
            for c in arg[1..].chars() {
                parsed.flags.insert(c.to_string());
            }
        } else {
            parsed.positionals.push(arg.clone());
        }
        i += 1;
    }
    parsed
}

fn main() {
    println!("=== 🦀 Project 067: CLI Argument Parser ===");
    let mock_args: Vec<String> = vec![
        "--verbose".into(),
        "-rf".into(),
        "--port".into(),
        "8080".into(),
        "input.txt".into(),
        "output.txt".into(),
    ];

    let cli = parse_args(&mock_args);
    println!("Flags:       {:?}", cli.flags);
    println!("Options:     {:?}", cli.options);
    println!("Positionals: {:?}", cli.positionals);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_cli_parsing() {
        let args = vec!["--host".into(), "localhost".into(), "-v".into()];
        let p = parse_args(&args);
        assert!(p.flags.contains("v"));
        assert_eq!(p.options.get("host"), Some(&"localhost".to_string()));
    }
}
