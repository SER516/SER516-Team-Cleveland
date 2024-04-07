# SER516-Team-Cleveland
<div>
    <img width="20" src="https://user-images.githubusercontent.com/25181517/183423507-c056a6f9-1ba8-4312-a350-19bcbc5a8697.png" alt="Python" title="Python"/>
    <img width="20" src="https://user-images.githubusercontent.com/25181517/183897015-94a058a6-b86e-4e42-a37f-bf92061753e5.png" alt="React" title="React"/>
    <img width="20" src="https://user-images.githubusercontent.com/25181517/117207330-263ba280-adf4-11eb-9b97-0ac5b40bc3be.png" alt="Docker" title="Docker"/>
    <img width="20" src="https://user-images.githubusercontent.com/25181517/121401671-49102800-c959-11eb-9f6f-74d49a5e1774.png" alt="npm" title="npm"/>
    <img width="20" src="https://user-images.githubusercontent.com/25181517/184146221-671413cb-b1ae-47db-a232-b37c99281516.png" alt="SonarQube" title="SonarQube"/>
    <img width="20" src="https://user-images.githubusercontent.com/25181517/184117132-9e89a93b-65fb-47c3-91e7-7d0f99e7c066.png" alt="pytest" title="pytest"/>
</div>

## Taiga API Integration

This project is a Python script for interacting with the Taiga API to perform various task and calculating metrics.

## Running the Application

- ### Running the Application using Docker

  To run the application this way, you need to install docker on your system first. Docker is an application that
  uses containerization technology to package software and its dependencies into standardized units called containers. 
  You can download docker to your system from- https://docs.docker.com/get-docker/.

  To run the application using docker, go to the folder - SER516-Team-Cleaveland (The base folder of the project),
  and run the command- 

   ``` bash
   cd SER516-Team-Cleveland
   docker-compose up --build -d
   ```
  It should run a multi-container application, which contains the front-end and the back-end applications. 
  Visit http://localhost:3000 to start the application. 

- ### Alternate method- Running the applications locally without Docker

  - #### 1. Prerequisites

    Before running the script, make sure you have the following installed:

    - Python 3 (Note: Python version>=3.11 for `date.fromisoformat()` to work properly)
    - Required Python packages (Go to `taigaProject` folder and install using `pip install -r requirements.txt`)
    - Taiga account with API access
    - Taiga project slug
    - Clone the repository
    ```bash
       git clone https://github.com/ser516asu/SER516-Team-Cleveland.git
       cd SER516-Team-Cleveland/taigaProject
    ```

  - #### 2. Running the Backend Application

    Go to `taigaProject` folder
    ``` bash
    cd taigaProject
    ```
    Run the command to download required dependencies
    ``` bash
    pip install -r requirements.txt
    ```
    Go to the source folder of the backend application(`cd taigaProject/src` or `cd src` depending on the current folder) and run the command- 
    ``` bash
    uvicorn main:app 
    ```
    Or
    ``` bash
    python3.11 -m uvicorn main:app
    ```

    To run on different port:
    ``` bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8001
    ```

    You can hit the API using `http://127.0.0.1:8000/[requiredApiPath]` or `http://localhost:8000/[requiredApiPath]`
    while providing the necessary payload. 

    Visit http://localhost:8000/docs to look at the possible APIs which can be hit from Postman.

    Use the command 
    ``` bash
    uvicorn main:app --reload
    ```
    to run the application in developer mode, it reloads everytime there's a change in a file. 

    ##### 2.1. Writing/Running unit test

    We're using pytest to write the unit test for the backend application. 
    The dependency is added to the requirements.txt file, please do a pip install before trying to run the tests. 
    In the test folder, create the python file in the format "test_{test-file-name}", since pytest only identifies the 
    files named in this format.

    To run the tests, go to the root folder, and run the command 
    ```
    pytest
    ```
    in the terminal to run the tests and get the results.

    - #### 3. To run the frontend
    Download node.js from https://nodejs.org/en/download

    On Mac, you can download either from above website or using homebrew.
    ``` bash
    brew search node
    ```
    ``` bash
    brew install node
    ```

    ##### 3.1. Check Node and npm version

    Command to check the Node version to confirm successful installation
    ``` bash
    node -v
    ```
    Command to check the npm version
    ``` bash
    npm -v
    ```

    ##### 3.2. Run the project
    1. Go to `react-ui` folder
    2. Install the packages using command:
    ``` bash
    npm install
    ```
    4. After successful install, start the project:
    ``` bash
    npm start
    ```
    4. Go to http://localhost:3000 to view in browser

  - ## Run microserices
    1. Lead-time: Go to lead-time folder and run it on port 8001
    ``` bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8001
    ```

    2. Dev-focus: Go to dev-focus folder and run it on port 8003
    ``` bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8003
    ```

## Using the application
  
- ### Getting Taiga Project Slug

To interact with the Taiga API using the provided Python script, you will need the project slug of your Taiga project. Follow these steps to find the project slug:

1. **Login to Taiga**: Open your web browser and log in to your Taiga account.

2. **Select the Project**: Navigate to the project for which you want to obtain the project slug.

3. **Project URL**: Look at the URL in your browser's address bar while you are inside the project. The project slug is the part of the URL that comes after the last slash     ("/"). For example:


- ### Fetch Metrics from Application
1. Enter username and password of taiga account to login
2. Project page will be displayed
3. Enter project slug eg: ser516asu-ser516-team-cleveland
4. Select type of metric from dropdown.
5. Submit to get the metric displaoyed on the same screen
