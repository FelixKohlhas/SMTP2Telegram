FROM node:16-alpine

WORKDIR /app

RUN npm install -g ehlo

EXPOSE 10025

# Use an entrypoint script to allow dynamic args
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
