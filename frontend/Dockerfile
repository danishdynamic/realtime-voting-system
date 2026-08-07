# Use an official lightweight Node image
FROM node:20-alpine

# Set the working directory inside the container
WORKDIR /app

# Copy package files first to optimize Docker layer caching
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of your frontend source code
COPY . .

# Expose the standard React port (3000 for CRA, 5173 for Vite)
EXPOSE 3000

# Start the development server with hot-reloading
CMD ["npm", "start"]