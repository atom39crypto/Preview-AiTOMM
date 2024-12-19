import json
import os
import tiktoken

history_file_path = 'engine\Weilder\memory.json'
tokenizer = tiktoken.get_encoding("cl100k_base")


def load_conversation_history():
    if os.path.exists(history_file_path):
        with open(history_file_path, 'r') as f:
            return json.load(f)
    return []  # Start with an empty history if the file does not exist


def save_conversation_history(history):
    with open(history_file_path, 'w') as f:
        json.dump(history, f)


def update_conversation_history(conversation_history,role, content):
 
    user = f"{content}" 
    conversation_history.append({"role": role, "content": user})
    save_conversation_history(conversation_history)

def tokenize(prompt):
    prompt_tokens = tokenizer.encode(prompt)
    token_count = len(prompt_tokens)

    max_completion_tokens = 1024 - token_count
    max_completion_tokens = max(0, max_completion_tokens)

    return max_completion_tokens


   
if __name__ == "__main__":
    update_conversation_history("user","what ?","what.......")