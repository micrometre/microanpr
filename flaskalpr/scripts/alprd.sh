#!/bin/bash
dir=flaskalpr/static/alprd_images
inotifywait  -m "$dir" -e close_write --format '%w%f' |
    while IFS=' ' read -r fname
    do
        #curl -X POST -H 'Content-Type: application/json' -d '{"$fname"}' http://localhost:5000/alprd1/alprd
        echo $fname

    done