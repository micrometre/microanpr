.PHONY: run
flask:
	flask --app flaskalpr run -h 0.0.0.0 --debug --reload

gunicorn:
	gunicorn -k gevent   -b 0.0.0.0:5000 'flaskalpr:create_app()'

wait:
	waitress-serve  --port=5000 --call 'flaskalpr:create_app'	

db_init:	
	flask --app flaskalpr init-db

default_user:	
	python3 flaskalpr/scripts/default_user.py 

clean: 
	rm flaskalpr/static/alprd1_images/*.jpg

start:
	docker compose up -d 

stop:
	docker compose down 

update:
	docker compose down 
	docker compose pull
	docker compose up -d --build

restart: 
	docker compose restart

remove:
	docker compose down -v
	docker compose rm -f

ffmpeg_serve:
	ffmpeg -i flaskalpr/static/uploaded-video/alprVideo1.mp4 -listen 1 -f mp4 -movflags frag_keyframe+empty_moov  http://127.0.0.1:5001

ffmpeg_comp:
	 ffmpeg -i alpr-video.mp4 -vcodec libx265 -crf 40 alpr-video-small.mp4



#gunicorn --bind 0.0.0.0 --timeout 600 --access-logfile '-' --error-logfile '-' 'flaskalpr:create_app'	 