<?php

use League\Fractal\Manager;
use League\Fractal\Resource\Collection;

require __DIR__.'/vendor/autoload.php';

$path = __DIR__.'/sitegraph.json';

function readTheFile($path) {
    $handle = fopen($path, "r");

    while(!feof($handle)) {
        $line = trim(fgets($handle));
        if ($line) {
            $json = json_decode($line);
            yield $json;
        }
    }

    fclose($handle);
}


// Create a top level instance somewhere
$fractal  = new Manager();
$iterator = readTheFile($path);

$resource = new Collection($iterator, function($page) {
    var_dump($page);
    exit;
});


$fractal->createData($resource)->