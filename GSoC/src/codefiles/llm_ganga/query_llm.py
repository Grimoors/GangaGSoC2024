import openai
import os

# Load the OpenAI API key from GITHUB Secrets
openai_api_key = os.getenv("OPENAI_API_KEY")
# openai_api_key =  "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"


# Ensure the API key is present
if not openai_api_key:
    raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

# Initialize OpenAI API
openai.api_key = openai_api_key

# Craft the prompt
prompt = """Write Python code to execute a job in Ganga that calculates an approximation to Pi using an accept-reject 
simulation method with one million simulations. The job should be split into a number of subjobs that each do a thousand simulations."""

# Send the request
response = openai.Completion.create(
    model="gpt-4-turbo-preview",
    prompt=prompt,
    temperature=0.5,
    max_tokens=350,
    n=1,
    stop=None,
    api_key=openai_api_key
)

# Extract and print the generated code
generated_code = response.choices[0].text.strip()
print(generated_code)
