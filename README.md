# ClassifyingUSLegislation
University project to design ML classification for US State Legislation.

# About
This is the base template for the US State Legislation website for SWENG. 


# Run the Website
The website is implemented using Pyscript.
It is run using Visual Studio Code.
1. Install pyscript extension, along with the Live Server extension. Live Server allows you to run pyscript directly in your browser.
2. Go to Settings in Visual Studio Code, then search for “Format on save”, and uncheck the box "Editor: Format On Save". This prevents certain python syntax errors.
3. Save the file and click the "Go Live" in the bottom right of the Visual Studio Code screen. The website should start up in your browser.

# Testing and Linting

## Testing
Please make sure to write sufficient unit tests for your Python code (get in contact if you're not sure what this means!). Your tests should be in a file whose name ends in test - for example the tests for `main.py` are in `main-test.py`. To run tests locally to confirm they work, make sure you have pytest installed by running
```
pip install pytest
```

Then you can run the tests in your file by running
```
pytest filename-test.py
```
So, for main you would run `pytest main-test.py`.

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
 
# Using Docker
A Dockerfile has been added to this project for the purposes of deployment.

To build the current version, 
```
docker build -t web-app .
```

Then, to run that
```
docker run -p 5500:5500 web-app
```

Then, you should be able to access the website at 127.0.0.1:5500.
