# Use an official Node.js runtime as the base image
FROM node:14-alpine

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json from the react-ui directory to the working directory
COPY ./package*.json ./

# Install npm dependencies
RUN npm install

# Copy the rest of the application code from the react-ui directory to the working directory
COPY . ./

# Expose the port on which the React app will run (default is 3000)
EXPOSE 3000

# Set the command to run the React app when the container starts
CMD ["npm", "start"]
