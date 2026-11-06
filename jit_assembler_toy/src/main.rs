//! Project 099: Toy JIT Machine Code Assembler
//! Demonstrates dynamic x86_64 machine instruction encoding.

pub struct Assembler {
    code: Vec<u8>,
}

impl Assembler {
    pub fn new() -> Self {
        Self { code: Vec::new() }
    }

    /// Emits `mov eax, imm32` (Opcode: B8 <imm32>)
    pub fn mov_eax_imm(&mut self, val: u32) {
        self.code.push(0xB8);
        self.code.extend_from_slice(&val.to_le_bytes());
    }

    /// Emits `add eax, imm32` (Opcode: 05 <imm32>)
    pub fn add_eax_imm(&mut self, val: u32) {
        self.code.push(0x05);
        self.code.extend_from_slice(&val.to_le_bytes());
    }

    /// Emits `ret` (Opcode: C3)
    pub fn ret(&mut self) {
        self.code.push(0xC3);
    }

    pub fn bytecode(&self) -> &[u8] {
        &self.code
    }
}

fn main() {
    println!("=== 🦀 Project 099: Toy JIT Assembler ===");
    let mut asm = Assembler::new();
    asm.mov_eax_imm(40);
    asm.add_eax_imm(2);
    asm.ret();

    println!("Assembled x86_64 machine instructions:");
    for (i, byte) in asm.bytecode().iter().enumerate() {
        print!("{:02X} ", byte);
        if (i + 1) % 8 == 0 { println!(); }
    }
    println!("\nExpected outcome if executed via mprotect: eax = 42");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_asm_emission() {
        let mut asm = Assembler::new();
        asm.mov_eax_imm(10);
        asm.ret();
        assert_eq!(asm.bytecode()[0], 0xB8);
        assert_eq!(*asm.bytecode().last().unwrap(), 0xC3);
    }
}
