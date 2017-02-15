<?php
    $json = file_get_contents('php://input');
    $input = json_decode($json, TRUE);
    echo $json;
    echo $input;
?>
