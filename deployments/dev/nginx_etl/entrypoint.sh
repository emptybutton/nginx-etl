#!/bin/bash

source ${UV_PROJECT_ENVIRONMENT}/bin/activate

touch /run/nginx/fake.log
chown nobody:nogroup /run/nginx/fake.log

nginx-etl dev db init
$@
