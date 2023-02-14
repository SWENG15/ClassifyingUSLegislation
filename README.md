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
