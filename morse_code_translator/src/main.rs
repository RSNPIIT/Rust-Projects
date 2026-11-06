//! Project 024: Morse Code Translator
//! Demonstrates table lookups and bidirectional string translations.

const MORSE_TABLE: &[(char, &str)] = &[
    ('A', ".-"), ('B', "-..."), ('C', "-.-."), ('D', "-.."), ('E', "."),
    ('F', "..-."), ('G', "--."), ('H', "...."), ('I', ".."), ('J', ".---"),
    ('K', "-.-"), ('L', ".-.."), ('M', "--"), ('N', "-."), ('O', "---"),
    ('P', ".--."), ('Q', "--.-"), ('R', ".-."), ('S', "..."), ('T', "-"),
    ('U', "..-"), ('V', "...-"), ('W', ".--"), ('X', "-..-"), ('Y', "-.--"),
    ('Z', "--.."), ('0', "-----"), ('1', ".----"), ('2', "..---"), ('3', "...--"),
    ('4', "....-"), ('5', "....."), ('6', "-...."), ('7', "--..."), ('8', "---.."),
    ('9', "----."),
];

pub fn text_to_morse(text: &str) -> String {
    let mut words = Vec::new();
    for word in text.split_whitespace() {
        let mut letters = Vec::new();
        for ch in word.to_uppercase().chars() {
            if let Some(&(_, code)) = MORSE_TABLE.iter().find(|&&(c, _)| c == ch) {
                letters.push(code);
            }
        }
        words.push(letters.join(" "));
    }
    words.join(" / ")
}

pub fn morse_to_text(morse: &str) -> String {
    let mut words = Vec::new();
    for word_code in morse.split('/') {
        let mut letters = String::new();
        for code in word_code.split_whitespace() {
            if let Some(&(ch, _)) = MORSE_TABLE.iter().find(|&&(_, c)| c == code) {
                letters.push(ch);
            }
        }
        words.push(letters);
    }
    words.join(" ")
}

fn main() {
    println!("=== 🦀 Project 024: Morse Code Translator ===");
    let message = "SOS HELLO RUST";
    let morse = text_to_morse(message);
    let recovered = morse_to_text(&morse);

    println!("Plain: {}", message);
    println!("Morse: {}", morse);
    println!("Back:  {}", recovered);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_morse() {
        let enc = text_to_morse("SOS");
        assert_eq!(enc, "... --- ...");
        assert_eq!(morse_to_text("... --- ..."), "SOS");
    }
}
