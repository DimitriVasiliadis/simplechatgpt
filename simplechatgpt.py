import openai
import os
import json
import sys

# Replace with your OpenAI API key
API_KEY = ""

# Initialize OpenAI API with your key
openai.api_key = API_KEY

def get_openai_response(messages, model="gpt-3.5-turbo", temperature=0.7):
    """
    Queries the OpenAI API with the provided messages and returns the response.
    
    Parameters:
    - messages (list): A list of message dictionaries representing the conversation history.
    - model (str): The OpenAI model to use.
    - temperature (float): Sampling temperature. Higher values (up to 2) make output more random; lower values (closer to 0) make it more focused and deterministic.

    Returns:
    - str: The response from the OpenAI API.
    """
    try:
        # Call the OpenAI API
        response = openai.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature
        )
        # Extract and return the response content
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"An error occurred: {e}"

def load_conversation_history(filename):
    """Load the conversation history from a file."""
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return []

def save_conversation_history(filename, conversation_history):
    """Save the conversation history to a file."""
    with open(filename, 'w') as file:
        json.dump(conversation_history, file, indent=4)

def main():
    # File to save and load conversation history
    history_file = "conversation_history.json"
    
    # Load previous conversation history
    conversation_history = load_conversation_history(history_file)
    
    print("Welcome to ChatGPT! Type 'exit' to end the conversation.")
    print("You can paste multi-line text. End your input with 'END' on a new line.\n")

    while True:
        # Collect multi-line input
        print("Enter your text (end with 'END'): ")
        user_input = []
        
        while True:
            line = sys.stdin.readline().rstrip()
            if line == "END":
                break
            user_input.append(line)
        
        user_input = "\n".join(user_input)

        if user_input.lower() == "exit":
            print("\nEnding the conversation. Goodbye!")
            # Save conversation history
            save_conversation_history(history_file, conversation_history)
            break

        if not user_input:
            print("Please enter a valid question or command.")
            continue

        # Add user message to the conversation history
        conversation_history.append({"role": "user", "content": user_input})

        # Get the response from OpenAI API
        response_text = get_openai_response(conversation_history)

        # Print the response
        print(f"\nChatGPT:\n{response_text}\n")

        # Add the model's response to the conversation history
        conversation_history.append({"role": "assistant", "content": response_text})

if __name__ == "__main__":
    main()