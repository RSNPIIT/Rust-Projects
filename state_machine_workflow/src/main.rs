//! Project 061: Type-State Workflow State Machine
//! Demonstrates compile-time verified transitions with zero runtime cost.

use std::marker::PhantomData;

pub struct Draft;
pub struct UnderReview;
pub struct Published;

pub struct Document<State> {
    title: String,
    _state: PhantomData<State>,
}

impl Document<Draft> {
    pub fn new(title: &str) -> Self {
        Self { title: title.to_string(), _state: PhantomData }
    }

    pub fn submit_for_review(self) -> Document<UnderReview> {
        Document { title: self.title, _state: PhantomData }
    }
}

impl Document<UnderReview> {
    pub fn approve(self) -> Document<Published> {
        Document { title: self.title, _state: PhantomData }
    }

    pub fn reject(self) -> Document<Draft> {
        Document { title: self.title, _state: PhantomData }
    }
}

impl Document<Published> {
    pub fn read(&self) -> &str {
        &self.title
    }
}

fn main() {
    println!("=== 🦀 Project 061: Type-State Workflow State Machine ===");
    let draft = Document::new("Rust 2026 Roadmap");
    let in_review = draft.submit_for_review();
    let published = in_review.approve();

    println!("Published Document: {}", published.read());
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_typestate() {
        let doc = Document::new("RFC").submit_for_review().approve();
        assert_eq!(doc.read(), "RFC");
    }
}
