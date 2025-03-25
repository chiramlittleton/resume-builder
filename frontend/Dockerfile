# Base image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy rest of the frontend code
COPY . .

# Expose development port
EXPOSE 3000

# Start Vite dev server
CMD ["npm", "run", "dev"]
