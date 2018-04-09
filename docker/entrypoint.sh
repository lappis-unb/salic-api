#!/bin/bash

cmd="$@"

echo "SQL_DRIVER: $SQL_DRIVER"

if [ "$SQL_DRIVER" = "" ] || [ "$SQL_DRIVER" = "sqlite" ]; then
    inv db --force
fi

exec $cmd
