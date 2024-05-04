.PHONY: run
flask:
	flask --app flaskalpr run -h 0.0.0.0 --debug --reload
flask_db_init:
	flask --app flaskalpr init-db
wait:
	waitress-serve  --call 'flaskalpr:create_app'	

clean: 
	rm -rf flaskalpr/static/alprd1_images/
	mkdir flaskalpr/static/alprd1_images

start:
	docker-compose up -d 

stop:
	docker-compose down 

update:
	docker-compose down 
	docker-compose pull
	docker-compose up -d --build

restart:
	docker-compose restart

remove:
	docker-compose down -v
	docker-compose rm -f

ffmpeg_mp4:
	ffmpeg -i flaskalpr/static/uploaded-video/alprVideo.mp4 -listen 1 -f mp4 -movflags frag_keyframe+empty_moov  http://127.0.0.1:5001

#	redis
#SCAN 0 count 100 match *19*

