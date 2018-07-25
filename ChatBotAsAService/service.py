from flask import Flask, jsonify, request
from chatbot import ChatBot
from bot_model import BotModel
import json
import os
import errno

app = Flask(__name__)

@app.route('/index', methods=['GET'])
def index():
    response = {
        "intro" : "welcome to the chatbot as a service. this end point should guide you through the other endpoints",
        "endpoints" : {
            "index" : "this endpoint. it is the informational endpoint",
            "talk" : "this lets you talk to a chat_bot. specify the name of the chatbot and the message you are sending to it",
            "create" : "this should create a new chatbot. specify the name of your chatbot and the intents json"
        }
    }
    return jsonify(response), 200

@app.route('/talk', methods=['POST'])
def talk():
    values = request.get_json()
    human_chat = values.get('human_chat')
    name = values.get('bot_name')

    if human_chat is None:
        return "Error: You need to talk to me", 400
    if name is None:
        return "Error: You need to tell me who i am", 400
    filepath = "./bots/" + name + "/" + name
    if not os.path.exists(os.path.dirname(filepath)):
        return "Error: The name of the bot you specified is not found", 404

    bot = ChatBot(name)
    bot_response = bot.response(human_chat)
    response = {
        'name' : name,
        'message': bot_response
    }
    return jsonify(response), 200

@app.route('/create', methods=['POST'])
def create():
    values = request.get_json()
    intents = values.get('intents_file')

    if intents is None:
        return "I cannot create a life form if I do not know this life form's intention you fool!", 400
    description = values.get('description')
    if description is None:
        return "Come on just describe the bot a little bit so that it will help others use it if they want", 400
    name = values.get('name')
    if name is None:
        return "We need a name for your bot you fool!", 400
    filepath = "./bots/" + name + "/" + name
    if not os.path.exists(os.path.dirname(filepath)):
        try:
            os.makedirs(os.path.dirname(filepath))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    with open(filepath + "intents.json", "w+") as outfile:
        json.dump(intents, outfile)
    botModel = BotModel(name)
    botModel.run()
    response = {
        "values" : values
    }
    return jsonify(response), 201

if __name__ == "__main__":
    app.run()
