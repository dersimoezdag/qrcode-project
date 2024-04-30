use std::fs;
use std::path::Path;

mod matrix_store;
mod qrcode_verification;

fn main() {
    println!("QR-Code Project started");

    let path = "./res";
    if !Path::new(path).exists() {
        match fs::create_dir_all(path) {
            Ok(_) => {}
            Err(err) => {
                panic!("Fehler beim Erstellen des Verzeichnisses: {:?}", err);
            }
        }
    } else {
        println!("Ordner 'res' existiert bereits.")
    }
}
