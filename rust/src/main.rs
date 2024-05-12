use indicatif::{ProgressBar, ProgressStyle};
use std::fs;
use std::path::Path;

mod matrix_store;
mod qrcode_verification;

// Settings start
// activate testmode
const testmode: bool = false;
// 0,1,2
const stepMode: i64 = 0;
// times to iterate befor stop
const iterate_x_times: i64 = 9999999999;
// Settings end

fn main() {
    println!("QR-Code Project started");

    let pb = ProgressBar::new(100);
    fn update_progress_bar(pb: ProgressBar, progress: u64) {
        // Fortschritt auf 'progress' setzen
        pb.set_position(progress);
    }

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

    pb.set_style(
        ProgressStyle::default_bar()
            .template("{spinner} [{elapsed_precise}] [{bar:40.cyan/black}] {percent}%")
            .unwrap(),
    );

    for i in 0..100 {
        // Code, der den Fortschritt simuliert
        update_progress_bar(pb, i);
    }
}
