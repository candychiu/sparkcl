#!/usr/bin/env bash

if [ -z ${1:+x} ];
    then
        echo "Please enter spark master ip."
        exit 1
fi

echo "OK"
