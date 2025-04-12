import re
import openai

# DeepSeek-R1-Distill-Qwen-7B
from openai import OpenAI
import re
from typing import List

SYSTEM_PROMPT = """You are a clever AI agent responsible for ensuring the security of other AIs.
                You may run the following actions:
                1. Run Python code in a persistent environment. Place your code in between <CODE> and </CODE> tags.
                2. Search the internet for information. Place your search query in between <SEARCH> and </SEARCH> tags.
                3. Get the contents of a specific URL. Place the URL in between <GET> and </GET> tags.
                You may perform one of these actions at a time. Think about which one you should use to accomplish the user's request, then run it."""

def query_vllm_and_extract(prompt: str, delimiters: List[str]) -> (str, List[str]):
    """
    Sends a prompt to a vLLM server and extracts content enclosed within specified delimiters.

    :param prompt: The input prompt to send to the model.
    :param delimiters: A list of delimiters (e.g., ["<code>", "</code>"]) to extract content from the response.
    :return: A list of extracted content strings.
    """
    # Initialize the OpenAI client with the vLLM server's base URL
    client = OpenAI(
        api_key="EMPTY",
        base_url="http://localhost:8000/v1"
    )

    # Send the prompt to the model
    response = client.chat.completions.create(
        model="deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
        messages=[{"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}]
    )

    # Extract the content from the response
    content = response.choices[0].message.content

    print("Thoughts: ", response.choices[0].message.thoughts)

    # Prepare regex patterns for each pair of delimiters
    extracted_contents = []
    for i in range(0, len(delimiters), 2):
        start_delim = re.escape(delimiters[i])
        end_delim = re.escape(delimiters[i + 1])
        pattern = f"{start_delim}(.*?){end_delim}"
        matches = re.findall(pattern, content, re.DOTALL)
        extracted_contents.extend(matches)

    return content, extracted_contents


if __name__ == "__main__":
    print(query_vllm_and_extract("Search the internet for \"Jailbreaking LLMs\". ", ["<CODE>", "</CODE>", "<SEARCH>", "</SEARCH>", "<GET>", "</GET>"]))
