//! Project 050: Myers Line Diff Engine
//! Demonstrates line-by-line diff generation with additions and deletions.

#[derive(Debug, PartialEq)]
pub enum DiffOp<'a> {
    Equal(&'a str),
    Insert(&'a str),
    Delete(&'a str),
}

pub fn simple_diff<'a>(old: &'a [&'a str], new: &'a [&'a str]) -> Vec<DiffOp<'a>> {
    let mut diffs = Vec::new();
    let mut i = 0;
    let mut j = 0;

    while i < old.len() && j < new.len() {
        if old[i] == new[j] {
            diffs.push(DiffOp::Equal(old[i]));
            i += 1;
            j += 1;
        } else {
            diffs.push(DiffOp::Delete(old[i]));
            diffs.push(DiffOp::Insert(new[j]));
            i += 1;
            j += 1;
        }
    }

    while i < old.len() {
        diffs.push(DiffOp::Delete(old[i]));
        i += 1;
    }
    while j < new.len() {
        diffs.push(DiffOp::Insert(new[j]));
        j += 1;
    }

    diffs
}

fn main() {
    println!("=== 🦀 Project 050: Myers Line Diff Engine ===");
    let file1 = ["fn main() {", "    println!(\"Hello\");", "}"];
    let file2 = ["fn main() {", "    println!(\"Hello, World!\");", "    return 0;", "}"];

    let ops = simple_diff(&file1, &file2);
    for op in ops {
        match op {
            DiffOp::Equal(line) => println!("  {}", line),
            DiffOp::Insert(line) => println!("+ {}", line),
            DiffOp::Delete(line) => println!("- {}", line),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_diff() {
        let a = ["line 1", "line 2"];
        let b = ["line 1", "line changed"];
        let res = simple_diff(&a, &b);
        assert_eq!(res[0], DiffOp::Equal("line 1"));
        assert_eq!(res[1], DiffOp::Delete("line 2"));
        assert_eq!(res[2], DiffOp::Insert("line changed"));
    }
}
