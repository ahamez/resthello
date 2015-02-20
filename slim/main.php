<?php
require 'vendor/autoload.php';

$app = new \Slim\Slim ();

$mongo = new MongoClient ("mongodb://127.0.0.1:27017");
$db = $mongo->paquito;

$app->get('/', function () use ($db) {
  $user = $db->users->findOne ([ "_id" => "saucisson" ]);
  $db->billing->update ([ "_id" => "saucisson" ], [ uniqid () => true ]);
  $project = $db->projects->findOne ([ "_id" => "cosyverif" ]);
  $db->results->update ([ "_id" => "cosyverif"], [ uniqid () => true ]);
  $locale = $db->locales->findOne ([ "_id" => "en" ]);
  echo "Hello, ahamez!";
});

$app->run();
