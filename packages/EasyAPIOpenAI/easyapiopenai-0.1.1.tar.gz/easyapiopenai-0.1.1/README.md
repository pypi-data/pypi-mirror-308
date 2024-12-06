# OpenAI-API-requests

Python classes that allow for easy interaction with the OpenAI API, based fully on web requests.

The classes are well documented within the code file.

## Currently Available Classes

### ChatGPTAgent
- Allows you to create an instance (object) of ChatGPT.
- Saves conversation history and supports tweaking all parameters like model, system prompt, temperature, etc.
- **Methods:**
  - `GetResponse`: Send a new message to the chatbot.
  - `ChangeSystemMessage`: Change the system message without affecting conversation history.
  - `ClearHistory`: Reset message history.

### ImgChatGPTAgent
- Similar to `ChatGPTAgent`, but introduces an additional method:
  - `GetResponseWithImg`: Send a message containing an image file.
- **Note:** As of now, only ChatGPT 4o and 4o-mini support processing images.

### DallEAgent
- Allows you to generate an image with the DALL-E AI image generator.
- **Methods:**
  - `GetImage`: Get the image as a PIL Image variable.
  - `GetImageURL`: Get a link to the generated image.

## Usage

You can download the package using PIP:

```bash
pip install EasyAPIOpenAI
```

Then, use it as follows:

```python
import easyapiopenai as oai

agent = oai.ChatGPTAgent("api-key", 'gpt-3.5-turbo')
```

Alternatively, if you prefer not to use PIP or are working with MicroPython, download the source code into the same folder and write:

```python
from APIWojOpenAI import *
```

Make sure to adjust the filename as necessary.

Then, you can use it like this:

```python
agent = ChatGPTAgent("api-key", 'gpt-3.5-turbo')
```

The `ChatGPTAgent` class should work well on embedded MicroPython systems, such as Raspberry Pi Pico. In that case, remove other classes from the file and replace all import statements with:

```python
import urequests as requests
```

## Example Code

```python
from APIWojOpenAI import *  # Assuming you have my code in the same directory saved to file APIWojOpenAI.py

API_KEY = 'KEY'  # OpenAI API key; always remember to secure it properly.

bot = ChatGPTAgent(API_KEY, model="gpt-3.5-turbo", max_tokens=1000, role="Your name is Bob")

message = "Hello, who are you?"  # Sample message
answer = bot.GetResponse(message)  # Get answer
print(answer)

message = "Remember that my favourite animal is a lizard."  # Second sample message
answer = bot.GetResponse(message)  # Get next answer, continuing conversation
print(answer)

message = "What is my favourite animal?"  # Third sample message, to prove it remembers
answer = bot.GetResponse(message)  # Get next answer, continuing conversation
print(answer)
```

**Output:**
```
Hi there! My name is Bob. How can I assist you today?
Got it! Your favorite animal is a lizard. Would you like to talk about lizards or anything else related to them?
Your favorite animal is a lizard.
```

## Known Errors and Things to Keep in Mind

- An incorrect API key, nonexistent AI model, or other impossible parameters will result in a 404 error.
- `ImgChatGPTAgent` may not remember the image for longer than one or two subsequent questions.
- If chat history exceeds 100 messages, the AI might stop working. This behavior depends on the AI model; it has been observed with GPT-3.5-turbo.
