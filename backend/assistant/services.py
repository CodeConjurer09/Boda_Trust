import openai
from django.conf import settings

def get_ai_response(query_text: str) -> str:
    # Example: integrate with OpenAI or any AI service
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": query_text}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error fetching AI response: {e}"