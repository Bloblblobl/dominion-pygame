# dominion-pygame

A [PyGame](https://www.pygame.org) / [PyGame GUI](https://github.com/MyreMylar/pygame_gui) client for the [Dominion](https://github.com/the-gigi/dominion) project 
based on the [Dominion card game](https://en.wikipedia.org/wiki/Dominion_%28card_game%29).

## Installation

## Pre-requisites

Install Python and pipenv

[Python](https://www.python.org/)
[pipenv](https://pipenv.pypa.io/en/latest/)

## MacOS Prerequisites

On the Mac you will also need:
`brew install sdl sdl_image sdl_mixer sdl_ttf portmidi`

## Installation

`pipenv install`

## Usage

There are two options to run the client. You can connect to a local server, 
or you can connect to a remote server.

### Connecting to a local server
To run against a local Dominion server you need a local server running.
See instructions for running a local Dominion server here:
https://github.com/the-gigi/dominion

Once the local server is running type:
```
DOMINION_PLAYER=<your name> pipenv run python main.py
``` 

You will play against Dominion AI players.

### Connecting to a remote server

You will need to get the IP address of the remote server from the person
running it. 

The next step is to set up a few environment variables. On Mac type in a terminal:

```
DOMINION_PLAYER='<your name>'
DOMINION_HOST='<IP address of the remote server>'
```

On Windows type in a PowerShell window:
```
$env:DOMINION_PLAYER=<your name>
$env:DOMINION_HOST=<IP address of the remote server>
```

Now, you finally launch dominion itself:

```
$ pipenv run python main.py
```

You will play against other players (human or AIs). If you 
(or any other human player) clicks the "Start Game" the server 
will start the game with the current human players and add AI 
players if necessary to reach 4 players. 

## Developer notes

Using [Fira Code](https://github.com/tonsky/FiraCode) font

BEWARE: PyGame on Windows can not render unicode characters above 0xFFFF

