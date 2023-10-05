from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

text = "Ever noticed how plane seats appear to be getting smaller and smaller? "
max_length = 150

app = Flask(__name__)
CORS(app)

bot_input_ids = None  # Initialize bot_input_ids


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data['message']
    # context or (if empty or length is 0) simple prompt to start conversation
    context = data['context']

    new_user_input_ids = tokenizer.encode(
        user_message + tokenizer.eos_token, return_tensors='pt')
    context_ids = tokenizer.encode(
        context + tokenizer.eos_token, return_tensors='pt')
    # only if context length is greater than 0, concatenate context and new_user_input_ids
    bot_input_ids = torch.cat([context_ids, new_user_input_ids],
                              dim=-1) if len(context) > 0 else new_user_input_ids
    decoded_input = tokenizer.decode(
        bot_input_ids[0], skip_special_tokens=False)

    response_ids = model.generate(
        bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)

    # Extract the generated response text using slicing
    text = tokenizer.decode(
        response_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

    print("DialoGPT: {}".format(text))

    return jsonify({'response': text, 'context': decoded_input + text})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
