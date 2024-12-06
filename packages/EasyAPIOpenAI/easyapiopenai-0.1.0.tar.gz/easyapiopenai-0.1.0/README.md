# OpenAI-API-requests
Python classes which allow using OpenAI API easily. Based fully on web requests.

The classes are well documented within the code file. 

Currently there are classes:

ChatGPTAgent - allows you to create instance (object) of ChatGPT, saves conversation history and supports tweaking all parameters like model, system prompt, temperature etc. Use GetResponse to send a new message to the chatbot, ChangeSystemMessage to change system message without affecting conversation history, and use ClearHistory to reset message history.

ImgChatGPTAgent - same as ChatGPTAgent, but introduces additional method GetResponseWithImg, which allows you to send a message containing a image file. Please mind that as of now only ChatGPT 4o and 4o-mini support processing images.

DallEAgent - Allows to generate an image with DALL-E AI image generator. Use GetImage to get the image as PIL Image variable, or use GetImageURL to get link to generated image.

# Usage

To use it in your Python project, download my code into same folder and write: 

from APIWojOpenAI import * 

Of course that depends on how you name the file.

Class ChatGPTAgent should work well on embedded MicroPython systems, such as Raspberry Pi Pico. In that case remove other classes from the file and replace all import statements with import urequests as requests .

I may make it a pip package someday.

# Example code

from APIWojOpenAI import * #assuming you have my code in the same directory saved to file APIWojOpenAI.py

API_KEY = 'KEY' #OpenAI API key, always remember about securing it propely.

bot = ChatGPTAgent(API_KEY, model="gpt-3.5-turbo", max_tokens=1000, role="Your name is Bob")

message = "Hello, who are you?" #Sample message

answer = bot.GetResponse(message) #Get answer

print(answer)

message = "Remember that my favourite animal is a lizard." #Second sample message

answer = bot.GetResponse(message) #Get next answer, continuing conversation

print(answer)

message = "What is my favourite animal?" #Third sample message, to prove it remembers

answer = bot.GetResponse(message) #Get next answer, continuing conversation

print(answer)

[Output]:

Hi there! My name is Bob. How can I assist you today?

Got it! Your favorite animal is a lizard. Would you like to talk about lizards or anything else related to them?

Your favorite animal is a lizard.

# Known errors and things to mind

Incorrect API key, nonexistent AI model or other impossible parameter will result in 404 error.

ImgChatGPTAgent may not remember the image for longer than one or two next questions.

If chat history is longer than 100 messages, the AI might stop working. It depends on the AI model, for sure. I noticed that for GPT-3.5-turbo.
