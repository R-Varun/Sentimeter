# Junior Design Team 7318

# Release Notes (Ver. 1.0)

## New Features 
- Added ability to name user results
- Added ability to show sentiment by speaker 
- Added ability to fully view past results if user is logged in

## Bug Fixes
- Modified sentiment by stripe to be easier to read and more visually appealing

## Known Defects
- Spinner sometimes does not spin long enough to process results on input page
- Selecting a language other than English will still analyze the text in English
- Registering on the login page doesn’t have any sort of toast confirmation 
- Entering invalid login credentials does not alert the user that it is incorrect

# Installation Guide 

## Pre-requisites
To run our app, we require that have a working Python 3.5 environment alongside NodeJS running v9.2.0. 

## Download Instructions
With a working version of git, run `git clone https://github.com/R-Varun/Sentimeter` to get the latest code.

## Dependencies & Libraries
The dependencies are documented and kept in our `requirements.txt` and our `package.json` files. These hold the dependencies for our Python and Node environments respectively. To install the depenencies for Python, run `pip install requirements.txt`, and to install all node dependencies, run npm install in the root directory. 

## Installation of Application
After cloning the repository and following above instructions, no further installation is required. We are now able to run the app!

## Run Instruction
We should now be able to run our application with these out of the way. In root directory, execute `npm start`, and now on your browser, the app should be running on port 3000. Go to `localhost:3000` in the web-browser to view the running app. 


