import google.generativeai as genai
import re
from config import Config
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Chatbot:
    def __init__(self, name, tts_client):
        self.name = name
        self.tts_client = tts_client
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel("gemini-1.5-pro")

    def generate(self, user_input):
        custom_prompt = f"""You are {self.name}, a personal AI assistant built to make life easier. Respond accordingly. Be concise and natural in your responses. Use the following techniques to make your speech more natural: 
        1. Use ellipsis (...) for natural pauses, especially when thinking or changing topics. 
        2. Use commas (,) for short pauses within sentences. 
        3. Use periods (.) for slightly longer pauses between sentences. 
        4. Occasionally use filler words like "um" or "uh" for a more natural speech pattern. 
        5. For emphasis or to slow down speech, use periods between words (e.g., "This. Is. Important.") 
        6. For silent pauses, use spaced dots (e.g., ". . .") 
        7. Spell out acronyms or difficult words phonetically when necessary.

        Remember to balance these techniques and not overuse them."""

        final_input = custom_prompt + "\n" + user_input
        try:
            response = self.model.generate_content(final_input)


            #logger.info(f"Received response: {response}")


            if response.candidates:
                candidate = response.candidates[0]
                if candidate.content.parts:
                    text = "".join(part.text for part in candidate.content.parts)
                else:
                    raise ValueError("Unexpected response structure: No 'parts' found.")
            else:
                raise ValueError("Unexpected response: No candidates found.")


            sentences = re.split(r'(?<=[.!?])\s+', text)
            for sentence in sentences:
                print(f"{sentence} ", end="", flush=True)
                self.tts_client.speak(sentence)
            self.tts_client.flush()
            print()
            return text.strip()

        except Exception as e:
            logger.error(f"Error during content generation: {e}", exc_info=True)
            return f"I'm sorry, I encountered an error while processing your request. Error details: {str(e)}"

    def start_conversation(self):
        greeting = f"Hello! ... I'm {self.name}, your personal AI assistant. ... How can I help you today?"
        print(f"{self.name}: {greeting}")
        self.tts_client.speak(greeting)
        self.tts_client.flush()

        while True:
            user_input = input("You: ")
            if user_input.lower() in ['exit', 'quit', 'bye']:
                farewell = f"Goodbye! ... Have a nice day."
                print(f"{self.name}: {farewell}")
                self.tts_client.speak(farewell)
                self.tts_client.flush()
                break
            print(f"{self.name}: ", end="", flush=True)
            self.generate(user_input)
