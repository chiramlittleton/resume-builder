# Base image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy only package.json + lock first (for better Docker caching)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the frontend code, including vite.config.ts
COPY . .

# Expose the port your Vite dev server will run on
EXPOSE 5173

# Run Vite in dev mode, listening on all interfaces
CMD ["npm", "run", "dev"]
