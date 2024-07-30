import requests
import json

def generate_text(prompt, model="llama2"):
    url = "http://localhost:11434/api/generate"
    
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        return json.loads(response.text)['response']
    else:
        return f"Error: {response.status_code}, {response.text}"

# Example usage
prompt = "Explain the concept of machine learning in simple terms."
result = generate_text(prompt, model="llama3")
print(result)