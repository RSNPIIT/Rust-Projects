//! Project 048: Markdown to HTML Transpiler
//! Demonstrates text transformations from Markdown to standard HTML tags.

pub fn markdown_to_html(md: &str) -> String {
    let mut html = String::new();
    let mut in_code_block = false;

    for line in md.lines() {
        if line.starts_with("```") {
            if in_code_block {
                html.push_str("</code></pre>\n");
            } else {
                html.push_str("<pre><code>");
            }
            in_code_block = !in_code_block;
            continue;
        }

        if in_code_block {
            html.push_str(line);
            html.push('\n');
            continue;
        }

        if line.starts_with("# ") {
            html.push_str(&format!("<h1>{}</h1>\n", &line[2..]));
        } else if line.starts_with("## ") {
            html.push_str(&format!("<h2>{}</h2>\n", &line[3..]));
        } else if line.starts_with("- ") {
            html.push_str(&format!("<li>{}</li>\n", &line[2..]));
        } else if !line.trim().is_empty() {
            html.push_str(&format!("<p>{}</p>\n", parse_inline(line)));
        }
    }

    if in_code_block {
        html.push_str("</code></pre>\n");
    }

    html
}

fn parse_inline(text: &str) -> String {
    // Simple inline parser for bold **text**
    let mut res = String::new();
    let mut parts = text.split("**");
    let mut is_bold = false;

    for p in parts {
        if is_bold {
            res.push_str(&format!("<strong>{}</strong>", p));
        } else {
            res.push_str(p);
        }
        is_bold = !is_bold;
    }
    res
}

fn main() {
    println!("=== 🦀 Project 048: Markdown to HTML Transpiler ===");
    let doc = "# Project Overview\n\nThis is **bold** text.\n\n- Point 1\n- Point 2";
    let rendered = markdown_to_html(doc);
    println!("HTML Output:\n{}", rendered);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_md_parser() {
        let md = "# Title\n- Item";
        let h = markdown_to_html(md);
        assert!(h.contains("<h1>Title</h1>"));
        assert!(h.contains("<li>Item</li>"));
    }
}
