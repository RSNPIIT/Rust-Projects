//! Project 025: ANSI Terminal Styler
//! Demonstrates ANSI escape sequences and method chaining builder styles.

#[derive(Debug, Clone, Copy)]
pub enum Color {
    Black = 30,
    Red = 31,
    Green = 32,
    Yellow = 33,
    Blue = 34,
    Magenta = 35,
    Cyan = 36,
    White = 37,
}

pub struct StyledText<'a> {
    text: &'a str,
    fg: Option<Color>,
    bold: bool,
    underline: bool,
}

impl<'a> StyledText<'a> {
    pub fn new(text: &'a str) -> Self {
        Self { text, fg: None, bold: false, underline: false }
    }

    pub fn color(mut self, color: Color) -> Self {
        self.fg = Some(color);
        self
    }

    pub fn bold(mut self) -> Self {
        self.bold = true;
        self
    }

    pub fn underline(mut self) -> Self {
        self.underline = true;
        self
    }

    pub fn render(&self) -> String {
        let mut codes = Vec::new();
        if self.bold { codes.push("1"); }
        if self.underline { codes.push("4"); }
        let fg_code;
        if let Some(c) = self.fg {
            fg_code = (c as u8).to_string();
            codes.push(&fg_code);
        }

        if codes.is_empty() {
            self.text.to_string()
        } else {
            format!("\x1b[{}m{}\x1b[0m", codes.join(";"), self.text)
        }
    }
}

fn main() {
    println!("=== 🦀 Project 025: ANSI Terminal Styler ===");
    println!("{}", StyledText::new("Success! Operation completed.").color(Color::Green).bold().render());
    println!("{}", StyledText::new("Warning: High memory usage.").color(Color::Yellow).render());
    println!("{}", StyledText::new("Error: Connection refused.").color(Color::Red).bold().underline().render());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ansi_render() {
        let styled = StyledText::new("Hello").color(Color::Red).bold().render();
        assert!(styled.contains("\x1b[1;31mHello\x1b[0m"));
    }
}
