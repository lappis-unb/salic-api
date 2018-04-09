#!/bin/bash

cmd="$@"

if [ "$SQL_DRIVER" = "" ] || [ "$SQL_DRIVER" = "sqlite" ]; then
    inv db --force
fi

exec $cmd
