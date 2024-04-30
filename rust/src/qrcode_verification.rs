mod qrcode_verification {

    pub fn contains_qr_code(matrix: &[[u8; 21]; 21]) -> bool {
        // Check for three position markers of a QR code in the matrix
        // Top-left corner
        let top_left =
            matrix[0][0] == 1 && matrix[0][6] == 1 && matrix[6][0] == 1 && matrix[6][6] == 1;
        // Top-right corner
        let top_right =
            matrix[0][20] == 1 && matrix[0][14] == 1 && matrix[6][20] == 1 && matrix[6][14] == 1;
        // Bottom-left corner
        let bottom_left =
            matrix[20][0] == 1 && matrix[20][6] == 1 && matrix[14][0] == 1 && matrix[14][6] == 1;

        let mut horizontal_timing = true;
        let mut vertical_timing = true;

        for i in 6..=14 {
            if i % 2 == 0 && (matrix[6][i] != 1 || matrix[i][6] != 1) {
                horizontal_timing = false;
                vertical_timing = false;
                break;
            } else if i % 2 != 0 && (matrix[6][i] != 0 || matrix[i][6] != 0) {
                horizontal_timing = false;
                vertical_timing = false;
                break;
            }
        }

        top_left && top_right && bottom_left && horizontal_timing && vertical_timing
    }
}
