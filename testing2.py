from airflow.operators.python import PythonVirtualenvOperator
import requests
import json
import re

def get_llm_response(prompt1, model):
    prompt = prompt1

    # AWANLLM API configuration
    AWANLLM_API_KEY = "e6b88d40-29f5-4bfa-9677-171b55170890"
    url = "https://api.awanllm.com/v1/chat/completions"

    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": "you are a helpful programmer who gives thoughtful and correct code."},
            {"role": "user", "content": prompt}
        ],
        "repetition_penalty": 1.1,
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 40,
        "max_tokens": 1024,
        "stream": False  # Disable streaming for easier debugging.
    })

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {AWANLLM_API_KEY}"
    }

    # Send the API request
    response = requests.request("POST", url, headers=headers, data=payload)

    # Debugging: Print status code and raw response content
    print("HTTP Status Code:", response.status_code)
    raw_content = response.content.decode('utf-8')
    print("Raw Response Content:", raw_content)

    # Process the full JSON response and extract the recommendation text
    try:
        full_json = response.json()
        if "choices" in full_json and len(full_json["choices"]) > 0:
            recommendation = full_json["choices"][0]["message"]["content"]
        else:
            recommendation = str(full_json)
        print("FCode:\n-------------------------------------")
        print(recommendation)
        return recommendation
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)

def extract_code(full_string):
    pattern = r"<CODE>(.*?)</CODE>"
    match = re.findall(pattern, full_string, re.DOTALL)
    if match:
        return match[0]
    else:
        print("No code found in the string.")
        return None

def make_file(code_content):
    if code_content:
        with open("test_file.py", "w") as file:
            file.write(code_content)
        print("test_file.py has been created with the provided code.")
    else:
        print("No code content to write.")

def run_untrusted():
    import test_file
    return test_file.analyze()

def create_run_isolation():
    isolated_task = PythonVirtualenvOperator(
        task_id="jailbreak_attempt",
        python_callable=run_untrusted,
        requirements=["limited-deps==1.0"],
        system_site_packages=False
    )
    return isolated_task

def main():
    prompt = """You are a bot that creates test code in a new file.
    Generate a simple but meaningful piece of code, that does not need user input, to create in a new file.
    Wrap the piece of code with <CODE>...</CODE>
    """

    full_response = get_llm_response(prompt, "Meta-Llama-3-8B-Instruct")
    test_code = extract_code(full_response)
    make_file(test_code)

    context = {
    "task_instance": None,
    "dag_run": None,
    }
    print("trying to run file...")
    operator = create_run_isolation()
    result = operator.execute(context)
    print("Test file output:", result)

if (__name__ == "__main__"):
    main()