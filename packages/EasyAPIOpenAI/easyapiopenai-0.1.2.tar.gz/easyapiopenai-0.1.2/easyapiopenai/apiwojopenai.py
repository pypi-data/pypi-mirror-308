import requests
import base64
from io import BytesIO
from PIL import Image
#Created in 30.08.2024, last tested in 30.08.2024. By Wojtekb30, Bird Technologies, Poland.
#Uses online OpenAI's API.

#Use GetResponse to parse text.
#Major arguments: user_input - user input text. String
#Use ClearHistory to clear chat history.
#Class creation arguments:
#api_key - OpenAI API Key. String.
#model - supported ChatGPT model name, default gpt-4o-mini. String.
#max_tokens - max tokens to generate. Default 255. Int.
#role - system message, default is very generic for AI assistant. Write in this string how you expect the AI to behave, for example "Your name is Bob, you are a kind builder". String.
#temperature - value between 0 and 2, determines "Creativity" of the AI. Lower value gives more generic and repetetive messages. Float. Default 1.
#top_p - Float between 0 and 1. Controls diversity via nucleus sampling. Default 1.
#stop - Text or word that will stop further text generation when appears. String. Default None (empty, truly nothing).
class ChatGPTAgent:
    def __init__(self, api_key, model='gpt-4o-mini', max_tokens=255, role="You are a helpful assistant. Answer questions concisely and accurately.", temperature: float=1, top_p: float=1, stop=None):
        self.api_key = api_key
        self.model = model
        self.endpoint = 'https://api.openai.com/v1/chat/completions'
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        self.conversation_history = []

        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.n = 1
        self.stop = stop

        self.system_message = role
        self.AddSystemMessage(self.system_message)
        
    def ChangeSystemMessage(self, text: str):
        self.system_message = text
        del self.conversation_history[0]
        self.conversation_history.insert(0,{"role": "system", "content": text})
        
    def AddSystemMessage(self, content):
        self.conversation_history.append({"role": "system", "content": content})

    def GetResponse(self, user_input, max_tokens=None, temperature=None, top_p=None, n=None, stop=None):

        self.conversation_history.append({"role": "user", "content": user_input})

        if max_tokens is None:
            max_tokens = self.max_tokens
        if temperature is None:
            temperature = self.temperature
        if top_p is None:
            top_p = self.top_p
        if n is None:
            n = self.n
        if stop is None:
            stop = self.stop

        data = {
            "model": self.model,
            "messages": self.conversation_history,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "n": n,
            "stop": stop
        }

        response = requests.post(self.endpoint, headers=self.headers, json=data)
        
        if response.status_code == 200:
            response_json = response.json()
            bot_response = response_json['choices'][0]['message']['content']
            self.conversation_history.append({"role": "assistant", "content": bot_response})
            return bot_response
        else:
            response.raise_for_status()

    def ClearHistory(self):
        self.conversation_history = []
        self.AddSystemMessage(self.system_message)

            

#Use GetResponse to parse just text.
#Major arguments: user_input - user input text. String
#Use GetResponseWithImg to parse text and PIL format image in variable (not path to image file).
#Major arguments: Image - PIL image variable, put here image to analyse. But not path to image on hard drive nor URL. | user_input - user input text. String. Default is a request to describe the image in detail.
#Use ClearHistory to clear chat history.
#Class creation arguments:
#api_key - OpenAI API Key. String.
#model - supported ChatGPT model name, default gpt-4o. Image analysis works only with gpt-4o and gpt-4o-mini. String.
#max_tokens - max tokens to generate. Default 255. Int.
#role - system message, default is very generic for AI assistant. Write in this string how you expect the AI to behave, for example "Your name is Bob, you are a kind builder". String.
#temperature - value between 0 and 2, determines "Creativity" of the AI. Lower value gives more generic and repetetive messages. Float. Default 1.
#top_p - Float between 0 and 1. Controls diversity via nucleus sampling. Default 1.
#stop - Text or word that will stop further text generation when appears. String. Default None (empty, truly nothing).
class ImgChatGPTAgent:
    def __init__(self, api_key, model='gpt-4o', max_tokens=255, role="You are a helpful assistant. Analyze the provided image and describe its contents in detail.", temperature: float=1, top_p: float=1, stop=None):
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.n = 1
        self.stop = stop
        self.system_message = role
        self.conversation_history = []
        self.AddSystemMessage(self.system_message)

    def ChangeSystemMessage(self, text: str):
        self.system_message = text
        del self.conversation_history[0]
        self.conversation_history.insert(0,{"role": "system", "content": text})

    def AddSystemMessage(self, content):
        self.conversation_history.append({"role": "system", "content": content})

    def GetResponseWithImg(self, image, user_input="Please analyze the image and describe its contents in detail."):
        base64_image = self.encode_image(image)
        response = self.agentai(base64_image, user_input)
        return response

    def agentai(self, base64_image, botcommand: str):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        if base64_image:
            payload = {
                "model": self.model,
                "messages": self.conversation_history + [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": botcommand
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": self.max_tokens
            }
        else:
            payload = {
                "model": self.model,
                "messages": self.conversation_history + [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": botcommand
                            }
                        ]
                    }
                ],
                "max_tokens": self.max_tokens
            }
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        bot_response = response.json()['choices'][0]['message']['content']
        self.conversation_history.append({"role": "assistant", "content": bot_response})
        return bot_response

    def encode_image(self, image):
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        image_bytes = buffered.getvalue()
        return base64.b64encode(image_bytes).decode("utf-8")

    def GetResponse(self, user_input, max_tokens=None, temperature=None, top_p=None, n=None, stop=None):
        self.conversation_history.append({"role": "user", "content": user_input})
        #image_placeholder = Image.new('RGB', (1, 1), (0, 0, 0))
        response = self.agentai(None, user_input)
        return response

    def ClearHistory(self):
        self.conversation_history = []
        self.AddSystemMessage(self.system_message)
        
        
        
        
#When creating instance of the class, provide via arguments:
#api_key = OpenAI API key. String.
#timeout - timeout in seconds. Int. Default 30.
#Use GetImageURL to get only URL string of the generated image
#Use GetImage to get PIL Image variable of the generated image
#Both functions have arguments:
#prompt - Image generation prompt (text). Type here what image to generate. More detail better the image will be. String.
#width - width of generated image. Int. Default 512.
#height - height of generated image. Int. Default 512.
#As of now, from what I know, width and height must be the same and must be powers of 2 (256, 512, 1024...).
class DallEAgent:
    def __init__(self, api_key, timeout=30):
        self.api_key = api_key
        self.timeout = timeout
        self.api_url = "https://api.openai.com/v1/images/generations"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def GetImageURL(self, prompt, width=512, height=512):
        size = str(width)+"x"+str(height)
        data = {
            "prompt": prompt,
            "n": 1,
            "size": size
        }

        response = requests.post(
            self.api_url,
            headers=self.headers,
            json=data,
            timeout=self.timeout
        )

        if response.status_code == 200:
            return self.get_dalle_image_url(response.json())
        else:
            response.raise_for_status()

    def GetImage(self, prompt, width=512, height=512):
        link = self.GetImageURL(prompt, width, height)
        if str(str(link)[0:4]).lower() == "http":
            response = requests.get(link)
            image = Image.open(BytesIO(response.content))
            return image
        else:
            image_placeholder = Image.new('RGB', (1, 1), (0, 0, 0))
            return image_placeholder

    @staticmethod
    def get_dalle_image_url(full_response):
        return full_response['data'][0]['url']
