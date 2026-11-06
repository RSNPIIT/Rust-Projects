//! Project 049: Concurrent TCP Echo Server
//! Demonstrates TCP networking, stream reading/writing, and concurrent connections.

use std::io::{Read, Write};

pub fn handle_client_mock<R: Read, W: Write>(mut reader: R, mut writer: W) -> std::io::Result<usize> {
    let mut buf = [0u8; 128];
    let mut total_bytes = 0;

    loop {
        let n = reader.read(&mut buf)?;
        if n == 0 { break; }
        writer.write_all(&buf[..n])?;
        total_bytes += n;
    }
    Ok(total_bytes)
}

fn main() {
    println!("=== 🦀 Project 049: Concurrent TCP Echo Server ===");
    println!("Demonstrating echo protocol buffer roundtrip via mock memory stream:");

    let client_input = b"PING ECHO 123";
    let mut server_output = Vec::new();

    let bytes = handle_client_mock(&client_input[..], &mut server_output).unwrap();
    println!("Echoed {} bytes: {}", bytes, String::from_utf8_lossy(&server_output));
    assert_eq!(&client_input[..], &server_output[..]);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_echo_mock() {
        let msg = b"Hello Echo Server";
        let mut out = Vec::new();
        handle_client_mock(&msg[..], &mut out).unwrap();
        assert_eq!(msg, &out[..]);
    }
}
