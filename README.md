# SER516-Team-Cleveland

# Taiga API Integration

This project is a Python script for interacting with the Taiga API to perform various task and calculating metrics.

## Prerequisites

Before running the script, make sure you have the following installed:

- Python 3
- Required Python packages (install using `pip install -r requirements.txt`)
- Taiga account with API access
- Taiga project slug

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/ser516asu/SER516-Team-Cleveland.git
   cd SER516-Team-Cleveland/taigaProject
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
   
3. Run the script:

   ```bash
   python3 app.py
   ```

## Getting Taiga Project Slug

To interact with the Taiga API using the provided Python script, you will need the project slug of your Taiga project. Follow these steps to find the project slug:

1. **Login to Taiga**: Open your web browser and log in to your Taiga account.

2. **Select the Project**: Navigate to the project for which you want to obtain the project slug.

3. **Project URL**: Look at the URL in your browser's address bar while you are inside the project. The project slug is the part of the URL that comes after the last slash ("/"). For example:


## Running the Backend Application

After running the command 
``` bash
   pip install -r requirements.txt
   ```
Go to the taigaProject folder (`cd taigaProject`) and run the command- 
``` bash
uvicorn main:app 
```

You can hit the API using `http:127.0.0.1/[requiredApiPath]`
while providing the necessary payload. 

Use the command 
``` bash
uvicorn main:app --reload
```
to run the application in developer mode, it reloads everytime 
there's a change in a file. 
## Download Node.js

Download node.js from https://nodejs.org/en/download

On Mac, you can download either from above website or using homebrew.

### `brew search node`


### `brew install node`

## Check Node and npm version

Command to check the Node version to confirm successful installation

### `node -v`

Command to check the npm version

### `npm -v`

### Run the project
1. Go to react-ui folder
2. Install the packages using command:
## `npm install`
3. After successful install, start the project:
## `npm start`
4. Go to http://localhost:3000 to view in browser

## Other Available Scripts

In the project directory, you can run:

### `npm start`


Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.
