//! Project 035: CLI Animated Progress Bar
//! Demonstrates terminal progress rendering, carriage returns, and stdout flushing.

pub struct ProgressBar {
    total: usize,
    current: usize,
    width: usize,
}

impl ProgressBar {
    pub fn new(total: usize, width: usize) -> Self {
        Self { total, current: 0, width }
    }

    pub fn set(&mut self, current: usize) {
        self.current = current.min(self.total);
    }

    pub fn render(&self) -> String {
        let percent = (self.current as f64 / self.total as f64) * 100.0;
        let filled = (self.current * self.width) / self.total;
        let empty = self.width - filled;

        let bar_fill = "=".repeat(filled);
        let bar_empty = " ".repeat(empty);

        format!("[{}>{}] {:>3.0}% ({}/{})", bar_fill, bar_empty, percent, self.current, self.total)
    }
}

fn main() {
    println!("=== 🦀 Project 035: CLI Animated Progress Bar ===");
    let mut pb = ProgressBar::new(100, 30);
    for step in (0..=100).step_by(25) {
        pb.set(step);
        println!("Progress: {}", pb.render());
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_progress_bar() {
        let mut pb = ProgressBar::new(100, 20);
        pb.set(50);
        let output = pb.render();
        assert!(output.contains("50%"));
    }
}
