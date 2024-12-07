import requests

class FreeNeiroAPI:
    def __init__(self, base_url="https://duck.gpt-api.workers.dev/chat/"):
        self.base_url = base_url

    def get_response(self, prompt, preprompt=""):
        try:
            fullprompt = preprompt + prompt
            params = {'prompt': fullprompt}
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()

            json_data = response.json()
            if json_data.get('action') == 'success':
                response_text = json_data.get('response', 'Нет ответа от DuckGPT')
                self.save_request(response_text)
                return response_text
            else:
                return f"API ERROR: {json_data.get('action')}"

        except requests.exceptions.RequestException as e:
            return f"Request error: {e}"
        except ValueError as e:
            return f"JSON decode error: {e}"