<?php

$mongo = new MongoClient ("mongodb://127.0.0.1:27017");
$mongo->dropDB ($mongo->paquito);
$db = $mongo->paquito;

{
  $collection = $db->createCollection ("users");
  $saucisson = [
    "_id" => "saucisson",
    "projects" => [
      1 => "cosyverif",
      2 => "paquito"
    ]
  ];
  $collection->insert ($saucisson);
}
{
  $collection = $db->createCollection ("projects");
  $cosyverif = [
    "_id" => "cosyverif",
    "description" => "THE project"
  ];
  $collection->insert ($cosyverif);
  $paquito = [
    "_id" => "paquito",
    "description" => "A real shit"
  ];
  $collection->insert ($paquito);
}
{
  $collection = $db->createCollection ("billing");
  $saucisson = [
    "_id" => "saucisson",
    "usage"    => []
  ];
  $collection->insert ($saucisson);
}
{
  $collection = $db->createCollection ("results");
  $cosyverif = [
    "_id" => "cosyverif",
    "results" => []
  ];
  $collection->insert ($cosyverif);
  $paquito = [
    "_id" => "paquito",
    "results" => []
  ];
  $collection->insert ($paquito);
}
{
  $collection = $db->createCollection ("locales");
  $en = [
    "_id" => "en",
    "message" => "grouik"
  ];
  $collection->insert ($en);
}
