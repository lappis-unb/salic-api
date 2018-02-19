#!/bin/bash

cmd="$@"

service nginx stop
service nginx start

$cmd