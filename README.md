# ClassifyingUSLegislation
University project to design ML classification for US State Legislation.

# About
This is the base template for the US State Legislation website for SWENG. 

# Run the Website

## GIT LFS
This project uses large datasets that exceed the 100MB limit on github. To run the project you will need to have have GIT LFS installed on your machine. Steps for installing this can be found on git-lfs.com.

## Run the Website Uncontainerised
The website is implemented using Pyscript.
You can run it using Visual Studio Code, although you will need to install the dependencies in requirements/web-app.txt. If you do not want to do this, then read the next section.
1. Install pyscript extension, along with the Live Server extension. Live Server allows you to run pyscript directly in your browser.
2. Go to Settings in Visual Studio Code, then search for “Format on save”, and uncheck the box "Editor: Format On Save". This prevents certain python syntax errors.
3. Save the file and click the "Go Live" in the bottom right of the Visual Studio Code screen. The website should start up in your browser.

## Run the Website Containerised
If you do not want to install dependencies to run this project, you can run it using Docker instead.
To build the current version, 
```
docker build -t web-app .
```

Then, to run that
```
docker run -p 5500:5500 web-app
```

Then, you should be able to access the website at 127.0.0.1:5500.


## Run Releases
### Release 3
This release contains an expanded prototype, with checking for the probability of a bill passing. To run this, run the following with Docker Desktop open:

```
docker run --name=web-app-container -p 5500:5500 clairegregg/classifying-us-legislation:v2
```

### Release 2
This release contains a fully functioning prototype. To run this, run the following with Docker Desktop open:

```
docker run --name=web-app-container -p 5500:5500 clairegregg/classifying-us-legislation:v1
```

### Release 1
This release just has a basic front end, and no ML classification model linked. To run this, run the following with Docker Desktop open:

```
docker run --name=web-app-container -p 5500:5500 clairegregg/classifying-us-legislation:v0-alpha
```



# Testing and Linting

## Testing
Please make sure to write sufficient unit tests for your Python code (get in contact if you're not sure what this means!). Your tests should be in a file whose name ends in test - for example the tests for `main.py` are in `main_test.py`. To run tests locally to confirm they work, make sure you have pytest installed by running
```
pip install pytest
```

Then you can run the tests in your file by running
```
pytest filename-test.py
```
So, for main you would run `pytest main_test.py`.

## Linting
We also have linting enabled on this repo, to ensure high quality and standardised code. To check if your code is okay before committing, you can run pylint!
First, confirm you have it installed by running
```
pip install pylint
```

Then, you can lint a file you have written by running
```
py -m pylint filename.py
```

 (You might just be able to run `pylint filename`, but that hasn't worked for me!)

 This will tell you any issues with your code, which you should fix before committing.

## To install ETL pipeline dependencies run:
```
pip install -r requirements/pulling-data.txt
```
Also create an env.py file with the line: 
```
API_KEY = "YOUR_LEGISCAN_API_KEY"
```
