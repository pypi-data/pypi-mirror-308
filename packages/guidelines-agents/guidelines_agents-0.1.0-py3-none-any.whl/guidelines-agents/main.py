from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

def generate_conversation(prompt, num_responses=5):
    # Load a conversational model and tokenizer from Hugging Face
    model_name = "microsoft/DialoGPT-small"  # A conversational model suitable for dialogue
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    # Encode the initial prompt
    input_ids = tokenizer.encode(prompt + tokenizer.eos_token, return_tensors="pt")

    conversation_history = input_ids  # Initialize the conversation history
    conversation = []  # To store the dialogue

    for step in range(num_responses):
        # Generate a response
        response_ids = model.generate(
            conversation_history,
            max_length=1000,
            pad_token_id=tokenizer.eos_token_id,
            top_k=50,
            top_p=0.95,
            temperature=0.7
        )

        # Decode the response
        response = tokenizer.decode(response_ids[:, conversation_history.shape[-1]:][0], skip_special_tokens=True)

        # Append the response to the conversation
        conversation.append(response)

        # Print the current turn
        print(f"Bot: {response}")

        # Add the response to the conversation history
        conversation_history = torch.cat([conversation_history, response_ids[:, conversation_history.shape[-1]:]], dim=-1)

    return conversation

# Example usage
initial_prompt = "Hello! How are you today?"
conversation = generate_conversation(initial_prompt)
