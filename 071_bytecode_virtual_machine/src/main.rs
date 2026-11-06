//! Project 071: Stack-Based Bytecode Virtual Machine
//! Demonstrates VM opcode decoding, call stacks, and execution loop.

#[derive(Debug, Clone, Copy)]
pub enum Opcode {
    Push(i64),
    Add,
    Sub,
    Mul,
    Halt,
}

pub struct VirtualMachine {
    stack: Vec<i64>,
}

impl VirtualMachine {
    pub fn new() -> Self {
        Self { stack: Vec::new() }
    }

    pub fn execute(&mut self, bytecode: &[Opcode]) -> Result<i64, &'static str> {
        let mut ip = 0;
        while ip < bytecode.len() {
            match bytecode[ip] {
                Opcode::Push(v) => self.stack.push(v),
                Opcode::Add => {
                    let b = self.stack.pop().ok_or("Stack underflow")?;
                    let a = self.stack.pop().ok_or("Stack underflow")?;
                    self.stack.push(a + b);
                }
                Opcode::Sub => {
                    let b = self.stack.pop().ok_or("Stack underflow")?;
                    let a = self.stack.pop().ok_or("Stack underflow")?;
                    self.stack.push(a - b);
                }
                Opcode::Mul => {
                    let b = self.stack.pop().ok_or("Stack underflow")?;
                    let a = self.stack.pop().ok_or("Stack underflow")?;
                    self.stack.push(a * b);
                }
                Opcode::Halt => break,
            }
            ip += 1;
        }
        self.stack.pop().ok_or("Empty stack at termination")
    }
}

fn main() {
    println!("=== 🦀 Project 071: Stack-Based Bytecode VM ===");
    // Program: (10 + 20) * 3
    let program = vec![
        Opcode::Push(10),
        Opcode::Push(20),
        Opcode::Add,
        Opcode::Push(3),
        Opcode::Mul,
        Opcode::Halt,
    ];

    let mut vm = VirtualMachine::new();
    let res = vm.execute(&program).unwrap();
    println!("Bytecode execution result: {}", res);
    assert_eq!(res, 90);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_vm() {
        let mut vm = VirtualMachine::new();
        let code = [Opcode::Push(5), Opcode::Push(7), Opcode::Add, Opcode::Halt];
        assert_eq!(vm.execute(&code).unwrap(), 12);
    }
}
