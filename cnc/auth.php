<?php
// change 'password' to your desired password.
// it would also be smarted to store this as a physical
// hash rather than having the raw text hased upon
// execution. totally up to you
$stored_hashed_password = hash('sha256', 'password');

// if captured...
if (isset($_POST['password'])) {
    // get password from form input
    $entered_password = $_POST['password'];

    // hash user password via SHA-256
    $entered_hashed_password = hash('sha256', $entered_password);

    // hash comparison to for integrity
    if ($entered_hashed_password === $stored_hashed_password) {
        // if hashes match, redirect to ddos panel
        header("Location: index.html");
        exit();
    } else {
        // return error if password is incorrect
        echo "Invalid password. Please try again.";
    }
} else {
    // verbose prompt to enter password
    echo "Password is required.";
}
?>
