//! Project 081: WebAssembly Binary Disassembler
//! Demonstrates parsing Wasm binary headers and section headers.

pub const WASM_MAGIC: [u8; 4] = [0x00, 0x61, 0x73, 0x6D]; // "\0asm"
pub const WASM_VERSION: [u8; 4] = [0x01, 0x00, 0x00, 0x00];

#[derive(Debug, PartialEq)]
pub struct WasmModuleHeader {
    pub valid_magic: bool,
    pub version: u32,
}

pub fn parse_wasm_header(bytes: &[u8]) -> Result<WasmModuleHeader, &'static str> {
    if bytes.len() < 8 {
        return Err("File too small to be a Wasm module");
    }
    let magic = &bytes[0..4];
    let version_bytes = [bytes[4], bytes[5], bytes[6], bytes[7]];
    let version = u32::from_le_bytes(version_bytes);

    Ok(WasmModuleHeader {
        valid_magic: magic == WASM_MAGIC,
        version,
    })
}

fn main() {
    println!("=== 🦀 Project 081: WebAssembly Disassembler ===");
    let mock_wasm: [u8; 8] = [0x00, 0x61, 0x73, 0x6D, 0x01, 0x00, 0x00, 0x00];
    let header = parse_wasm_header(&mock_wasm).unwrap();
    println!("Valid Magic? {}", header.valid_magic);
    println!("Wasm Version: {}", header.version);
    assert!(header.valid_magic);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_wasm_magic() {
        let h = parse_wasm_header(&[0x00, 0x61, 0x73, 0x6D, 1, 0, 0, 0]).unwrap();
        assert!(h.valid_magic);
        assert_eq!(h.version, 1);
    }
}
