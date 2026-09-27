use sha2::{Sha256, Digest};
use std::fs::File;
use std::io::{self, Read};

fn main() -> io::Result<()> {
    let file_path = "watermarked_img_8622055187516012161.png";

    let mut file = File::open(file_path)?;
    let mut hasher = Sha256::new();
    let mut buffer = Vec::new();

    file.read_to_end(&mut buffer)?;
    hasher.update(&buffer);

    let result = hasher.finalize();
    println!("Golden Kin Atelier Asset Hash (SHA-256):");
    for byte in result {
        print!("{:02x}", byte);
    }
    println!();

    Ok(())
}
