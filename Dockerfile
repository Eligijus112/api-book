# Base Nginx image 
FROM nginx:stable-alpine

# Copying the HTML content of the book to the nginx directory for html serving
COPY /api-book/_build/html/ /usr/share/nginx/html