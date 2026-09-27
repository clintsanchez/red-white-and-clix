# Website form endpoint -> GoHighLevel. Build context is the repository root.
FROM node:20-alpine
WORKDIR /app
COPY deploy/railway/forms/server.mjs /app/server.mjs
USER node
EXPOSE 8080
CMD ["node", "/app/server.mjs"]
