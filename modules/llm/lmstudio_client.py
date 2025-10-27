import requests
import json
import re


class LMStudioClient:
    """
    A client for interacting with a local LM Studio server's API.
    Includes robust error handling and response cleaning.
    """

    def __init__(self, base_url="http://localhost:1234/v1"):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}

    def _clean_json_response(self, text):
        """
        Helper function to clean the LLM's response by removing markdown code fences
        and surrounding whitespace. This is crucial for reliable JSON parsing.
        """
        # Uses a regular expression to find a JSON block within ```json ... ``` or ``` ... ```
        match = re.search(r"```(json)?\s*(\{.*\}|\[.*\])\s*```", text, re.DOTALL)
        if match:
            # If a match is found, return the captured group which is the content inside the fences.
            cleaned_text = match.group(2).strip()
        else:
            # If no markdown fences are found, just strip whitespace from the original text.
            cleaned_text = text.strip()
        return cleaned_text

    def _clean_code_response(self, text):
        """
        Cleans markdown fences from code blocks for saving to files.
        """
        match = re.search(r"```(?:\w+)?\s*(.*)\s*```", text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return text.strip()

    def query(self, prompt, temperature=0.4, is_json=False,
                      system_prompt="You are a helpful AI assistant."):
        """
        Sends a generic prompt to the LM Studio server.

        Args:
            prompt (str): The user's prompt.
            temperature (float): The generation temperature.
            is_json (bool): If True, cleans the response specifically for JSON parsing.
            system_prompt (str): The system prompt to guide the model's behavior.

        Returns:
            str: The generated text or an error message.
        """
        endpoint = f"{self.base_url}/chat/completions"
        data = {
            "model": "local-model",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
        }

        print(f"   -> Sending prompt to LM Studio...")

        try:
            response = requests.post(endpoint, headers=self.headers, data=json.dumps(data), timeout=300)
            response.raise_for_status()
            response_json = response.json()

            if 'choices' in response_json and len(response_json['choices']) > 0:
                generated_text = response_json['choices'][0]['message']['content']
                print(f"   -> Response received.")

                if is_json:
                    return self._clean_json_response(generated_text)
                else:
                    return self._clean_code_response(generated_text)
            else:
                print(f"\n--- CRITICAL: UNEXPECTED RESPONSE FROM LM STUDIO ---")
                print(json.dumps(response_json, indent=2))
                return f"/* Error: Received an unexpected response from LM Studio. */"

        except requests.exceptions.RequestException as e:
            print(f"\n--- CRITICAL: LM STUDIO API ERROR ---")
            print(f"Could not connect to the server at {endpoint}.")
            print("Please ensure LM Studio is running, a model is loaded, and the server is started.")
            print(f"Error details: {e}\n")
            return f"/* Error: Failed to connect to LM Studio. */"