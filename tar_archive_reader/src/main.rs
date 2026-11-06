//! Project 064: POSIX UStar Tar Archive Reader
//! Demonstrates 512-byte block decoding and octal header parsing.

pub struct TarHeader {
    pub name: String,
    pub size: usize,
    pub mode: u32,
}

pub fn parse_tar_header(block: &[u8; 512]) -> Option<TarHeader> {
    if block.iter().all(|&b| b == 0) {
        return None; // End of archive marker
    }

    let name = String::from_utf8_lossy(&block[0..100]).trim_matches('\0').to_string();
    let size_str = String::from_utf8_lossy(&block[124..136]).trim_matches('\0').trim().to_string();
    let size = usize::from_str_radix(&size_str, 8).unwrap_or(0);
    let mode_str = String::from_utf8_lossy(&block[100..108]).trim_matches('\0').trim().to_string();
    let mode = u32::from_str_radix(&mode_str, 8).unwrap_or(0);

    Some(TarHeader { name, size, mode })
}

fn main() {
    println!("=== 🦀 Project 064: POSIX UStar Tar Archive Reader ===");
    let mut mock_block = [0u8; 512];
    mock_block[0..8].copy_from_slice(b"test.txt");
    mock_block[100..107].copy_from_slice(b"0000644");
    mock_block[124..135].copy_from_slice(b"00000000100");

    let header = parse_tar_header(&mock_block).unwrap();
    println!("File Name: {}", header.name);
    println!("File Size: {} bytes", header.size);
    println!("Mode:      0o{:o}", header.mode);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tar_header() {
        let mut blk = [0u8; 512];
        blk[0..4].copy_from_slice(b"file");
        blk[124..135].copy_from_slice(b"00000000010"); // 8 in octal
        let h = parse_tar_header(&blk).unwrap();
        assert_eq!(h.name, "file");
        assert_eq!(h.size, 8);
    }
}
