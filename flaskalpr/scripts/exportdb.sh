#!/bin/bash
docker exec  redis redis-cli HGETALL alpr_plate_to_img > /home/dell/repos/flaskalpr/flaskalpr/data/export.csv