FROM nginx:alpine
RUN mkdir -p /app/staticfiles && \
    chown -R nginx:nginx /app/staticfiles && \
    chmod -R 755 /app/staticfiles

COPY nginx.conf /etc/nginx/conf.d/default.conf