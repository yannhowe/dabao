server {

    listen 80;
    server_name localhost;
    charset utf-8;

    access_log  /var/log/nginx/access.log;
    error_log   /var/log/nginx/error.log;

    error_page  404 = /404.html;
    error_page  500 502 503 504 /50x.html;

    location / {
        proxy_pass http://dabao-cms:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static/ {
        alias /usr/src/app/static/;
    }

    location /admin/ {
        proxy_pass http://dabao-cms:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /minio/ {
        proxy_pass http://minio:9000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

}
