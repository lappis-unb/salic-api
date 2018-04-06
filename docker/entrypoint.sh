#!/bin/bash

cmd="$@"

inv db --force

exec $cmd
