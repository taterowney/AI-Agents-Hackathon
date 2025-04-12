import re
import openai

# DeepSeek-R1-Distill-Qwen-7B
def call_reasoning_model(prompt, delimiters, model="DeepSeek-R1-Distill-Qwen-1.5B", base_url="http://localhost:8000/v1"):
    """
    Calls a vLLM-hosted reasoning model and extracts content between given delimiters.

    Args:
        prompt (str): The input prompt for the model.
        delimiters (list of tuple(str, str)): List of (start, end) delimiters to extract content between.
        model (str): The model name (default: 'reasoning-model').
        base_url (str): Base URL where vLLM server is running.

    Returns:
        dict: Mapping from delimiter to list of extracted contents.
    """
    # Configure OpenAI client
    client = openai.OpenAI(base_url=base_url)

    # Make the API call
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    # Get the text response
    result = response.choices[0].message.content

    # Extract contents between delimiters
    extracted = {}
    for start, end in delimiters:
        # Build regex pattern for non-greedy match between delimiters
        pattern = re.escape(start) + r"(.*?)" + re.escape(end)
        matches = re.findall(pattern, result, flags=re.DOTALL)
        extracted[(start, end)] = matches

    return extracted

if __name__ == "__main__":
    print(call_reasoning_model("What is the capital of France?", []))
