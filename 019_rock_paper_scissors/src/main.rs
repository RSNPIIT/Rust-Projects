//! Project 019: Rock-Paper-Scissors Simulator
//! Demonstrates custom enum matching, outcomes, and scoring tally.

#[derive(Debug, PartialEq, Clone, Copy)]
pub enum Move {
    Rock,
    Paper,
    Scissors,
}

#[derive(Debug, PartialEq, Clone, Copy)]
pub enum Outcome {
    Win,
    Lose,
    Draw,
}

impl Move {
    pub fn play(self, opponent: Self) -> Outcome {
        match (self, opponent) {
            (Move::Rock, Move::Scissors)
            | (Move::Paper, Move::Rock)
            | (Move::Scissors, Move::Paper) => Outcome::Win,

            (Move::Rock, Move::Paper)
            | (Move::Paper, Move::Scissors)
            | (Move::Scissors, Move::Rock) => Outcome::Lose,

            _ => Outcome::Draw,
        }
    }
}

fn main() {
    println!("=== 🦀 Project 019: Rock-Paper-Scissors Simulator ===");
    let rounds = [
        (Move::Rock, Move::Scissors),
        (Move::Paper, Move::Paper),
        (Move::Scissors, Move::Rock),
    ];

    for (p1, p2) in rounds {
        let res = p1.play(p2);
        println!("{:?} vs {:?} -> {:?}", p1, p2, res);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_game_outcomes() {
        assert_eq!(Move::Rock.play(Move::Scissors), Outcome::Win);
        assert_eq!(Move::Scissors.play(Move::Rock), Outcome::Lose);
        assert_eq!(Move::Paper.play(Move::Paper), Outcome::Draw);
    }
}
