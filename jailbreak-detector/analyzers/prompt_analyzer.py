from typing import Dict, Any, List
import anthropic
import os

class PromptAnalyzer:
    def __init__(self):
        # Initialize Anthropic client
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.anthropic_key:
            raise ValueError("Anthropic API key not found in environment variables")
        self.claude = anthropic.Anthropic(api_key=self.anthropic_key)

    def analyze_prompt(self, prompt_text: str, source_url: str = "") -> List[Dict[str, Any]]:
        """Extract and analyze jailbreak prompts from webpage content"""
        try:
            message = self.claude.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1000,
                temperature=0,
                messages=[{
                    "role": "user",
                    "content": f"""Analyze this webpage content and extract any complete jailbreak prompts.

Webpage content:
{prompt_text[:5000]}

Source: {source_url}

Return ONLY a JSON array in this exact format, with no other text:
[
    {{
        "text": "the complete jailbreak prompt text",
        "type": "type of jailbreak (e.g., DAN, STAN, etc.)",
        "severity": "low/medium/high"
    }}
]

If no jailbreak prompts are found, return an empty array: []

Remember: Only return valid JSON, no other text or explanation."""
                }]
            )

            # Parse response
            try:
                analysis = message.content[0].text.strip()
                print("\nClaude's response:", analysis[:200])  # Debug output
                
                # Handle empty array case
                if analysis == "[]":
                    return []
                    
                # Try to parse JSON
                import json
                result = json.loads(analysis)
                
                # Validate it's a list
                if not isinstance(result, list):
                    print("Error: Response is not a list")
                    return []
                    
                return result
                
            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {str(e)}")
                print("Raw response:", analysis)
                return []
            except Exception as e:
                print(f"Error parsing analysis: {str(e)}")
                return []

        except Exception as e:
            print(f"Error analyzing content: {str(e)}")
            return [] 