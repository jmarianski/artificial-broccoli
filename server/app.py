from flask import Flask, request, jsonify
# Import CORS and enable it for all routes
from flask_cors import CORS
from transformers import GPT2Tokenizer, GPTNeoForCausalLM
import torch

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

text = "Ever noticed how plane seats appear to be getting smaller and smaller? "
max_length = 150

app = Flask(__name__)

CORS(app)

# Conversation history to maintain context
conversation_history = []

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data['message']

    # encode the new user input, add the eos_token and return a tensor in Pytorch
    new_user_input_ids = tokenizer.encode(user_message + tokenizer.eos_token, return_tensors='pt')

    # append the new user input tokens to the chat history
    bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if step > 0 else new_user_input_ids

    # generated a response while limiting the total chat history to 1000 tokens, 
    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

    text = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

    print("DialoGPT: {}".format(text))

    # return output as an object with response key
    return jsonify({'response': text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)