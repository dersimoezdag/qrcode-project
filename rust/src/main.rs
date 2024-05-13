use indicatif::{ProgressBar, ProgressStyle};
use std::fs;
use std::path::Path;
use std::{thread, time};

mod matrix_store;
mod qrcode_verification;

// Settings start
// activate testmode
const TESTMODE: bool = false;
// 0,1,2
const STEP_MODE: i64 = 0;
// times to iterate befor stop
const ITERATE_X_TIMES: i64 = 9999999999;
// Settings end

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

    let progress_bar = ProgressBar::new(10000);
    progress_bar.set_style(
        ProgressStyle::default_bar()
            .template("{spinner} [{elapsed_precise}] [{bar:40.cyan/black}] {percent}%")
            .unwrap(),
    );

    let delay = time::Duration::from_millis(25);

    for progress in 0..100 {
        thread::sleep(delay);
        // Code, der den Fortschritt simuliert
        progress_bar.set_position(progress);
    }

    progress_bar.finish();
}
