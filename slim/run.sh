#! /bin/bash

curl -sS https://getcomposer.org/installer | php
./composer.phar update
php init.php
php -S localhost:8080 -t . main.php
