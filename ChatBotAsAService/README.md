# This is the chatbot as a service

You can create a new chatbot with a POST request and talk to a chatbot with a POST

# Installation
python 3.6 and venv are dependencies for this project as well as virtual env.

First clone the project and cd into the ChatBotAsAService directory

`$ git clone https://github.com/EricChristensen/Turing-Test-Game.git`

`$ cd Turing-Test-Game/ChatBotAsAService`

To create your virtual environment execute:

`$ python3 -m venv env`

from the command line.
To enter into the vritual environment execute:

`$ source env/bin/activate`

You should now see `(env)` before your prompt.
In the virtual environment execute:

`(env)$ pip3 install requirements.txt`

to install all of the dependencies for the project.

# Usage

## Start the service
To start the service run:

`(env)$ python3 service.py`

## Create a chatbot
With the service up and running, create a new chatbot execute a POST Request through your favorite REST client such as postman.

POST http://127.0.0.1:5000/create
Example request:
```
{
	"intents_file" : {
		"intents": [
    		{
				"patterns": [ "I hate you", "You suck", "You are bad"],
                "responses": [ "Dont be so mean, what are you afraid of?", "Wow, good one hotshot","Is that supposed to be funny?"],
                "tag": "attack"
            },
            {
                "patterns": ["Im not", "I would never", "I have never"],
                "responses": ["Dont be so defensive", "Why are you so defensive","Calm down cry baby"],
                "tag": "defense"
            }
        ]
	},
   "description" : "a game of arguing",
   "name" : "game_"
}
```
![create chatbot](https://github.com/EricChristensen/Turing-Test-Game/blob/master/ChatBotAsAService/imgs/chat_bot_create.png)

## Talk to a chat bot
With the service up and running, hit the `talk` POST endpoint specifying the name of the chatbot you want to talk to and the text that you want to say to the bot

POST http://127.0.0.1:5000/talk
```
{
	"human_chat": "hello how are you",
	"bot_name": "game_"
}
```
![talk to bot](https://github.com/EricChristensen/Turing-Test-Game/blob/master/ChatBotAsAService/imgs/chatbot_talk.png)

To exit from the virtual environment execute:

`(env)$ deactivate`
