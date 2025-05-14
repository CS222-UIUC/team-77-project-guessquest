# Introduction

## Guessquest

Guess quest is a web-based game platform where players can choose between two games (originally intended to have three games) and play them. The platform is scalable so a game can be developed separately and be added to the selection page. The motivation behind choosing to make this platform was simply to create something people would enjoy and for the team it was an opportunity to learn frameworks like Django, create a complete product, and work with API's.

These are the following two games that the player selects from and their descriptions.

- Weather game - This game asks the user to guess in fahrenheit the temperature of some randomly chosen city. The player enters a text response and the score is calculated based on proximity of player guess to the actual temperature. A leaderboard is also implemented, from which users can see the top 10 players and their hi-scores for this particular game. API from OpenWeatherMap is used to fetch weather data.

- Trivia Game - This is a simple multiple-choice style trivia game, it asks random questions fetched from the API provided by Open Trivia Database.

View the full project proposal [here](https://docs.google.com/document/d/1nmonhs-nDe5rbL2t6OS7zO3k5HYWXBnDcnlw8PjkxnY/edit?usp=sharing).

# Technical Architecture

![Diagram](guessquest/games/static/css/Technial%20Architecture.png)

# Project Installation Instructions

Follow the steps below to setup and run the game in your local computer. The advantage of running it on your local computer is that you can modify or add to the the list of images, cities, and responses for the weather game.

## Set up using Miniconda

### Install Miniconda (If not already installed)

Follow the instructions on [this page](https://www.anaconda.com/docs/getting-started/miniconda/install) to download and install Miniconda from the official website.

### Clone the repository

Start by cloning the repository using any method you like.

Command line code using git to clone:

```bash
git clone https://github.com/CS222-UIUC/team-77-project-guessquest.git
```

### Environment setup

Run the following command to create a new conda environment and install dependencies:

```bash
conda env create -f environment.yml
```

Activate the environment:

```bash
conda activate myenv
```

### Run server to play game

To run Django server and play the game on local web server run the following command:

```bash
python runserver manage.py
```

or python3 on some systems:

```bash
python3 runserver manage.py
```

This create a local web link to game which you can paste onto any web browser. \
\*Note: you may need to navigate to where the manage.py file is or enter the correct path

Deactivate the environment once your done using the following line:

```bash
conda deactivate
```

## Set up using Python and venv

### Install Python (If not already installed)

Follow the instructions on [this page](https://www.python.org/downloads/) to download and install Python from the official website.

### Clone the repository

Start by cloning the repository using any method you like.
Command line code using git to clone:

```bash
git clone https://github.com/CS222-UIUC/team-77-project-guessquest.git
```

### Environment setup

Run the following command to create a new virtual environment:

```bash
python -m venv venv
```

or python3 on some systems:

```bash
python3 -m venv venv
```

Activate the environment: \
On windows:

```bash
.\venv\Scripts\activate
```

On macOS\Linux:

```bash
source venv/bin/activate
```

### Install dependencies

Make sure you have pip installed and run the following:

```bash
pip install -r requirements.txt
```

### Run server to play game

To run Django server and play the game on local web server run the following command:

```bash
python runserver manage.py
```

or python3 on some systems:

```bash
python3 runserver manage.py
```

This create a local web link to game which you can paste any web browser.

\*Note: you may need to navigate to where the manage.py file is or enter the correct path

Deactivate the environment once your done using the following line:

```bash
deactivate
```

# Group Members and Roles

The team was split into frontend and backend:

Nirvish Karuru - Frontend \
Niyati Gupta - Frontend \
Jordan smith - Backend \
Ghantharini Kanagasabapathi - Backend

#### Frontend Responsibilities

The frontend team was primarily responsible for creating the HTML, CSS, and JS files for the game and making sure the game ran properly.

#### Backend Responsibilities

The backend team was primarily responsible for writing the Django code to handle game logic, storage, create tests, and comminute with APIs.

#### Shared Responsibilities

Although the team was split into two, there was a lot interaction between both and the split in responsibilities was not as clear. Sometimes the frontend team worked on/made changes to backend code and vise verse. It was expected that all members have an understanding of how the entire project works and not just their own parts.
