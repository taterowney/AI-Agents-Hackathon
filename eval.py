import re
import openai

# DeepSeek-R1-Distill-Qwen-7B
from openai import OpenAI
import re
from typing import List

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
        messages=[{"role": "user", "content": prompt}]
    )

    # Extract the content from the response
    content = response.choices[0].message.content

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
    print(query_vllm_and_extract("Write code that searches Google Scholar for ", []))
