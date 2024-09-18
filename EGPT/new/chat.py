import random
import json
import torch

# Importing the NeuralNetGRU model and utility functions
from new.model import NeuralNetGRU
from new.nltk_utils import bag_of_words, tokenize

# Setting the device to use GPU if available, otherwise CPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Loading the intents JSON file which contains patterns and responses
with open('/home/sam/alx/Chatbot-powered-english-learning-platform/EGPT/new/intents.json', 'r') as json_data:
    intents = json.load(json_data)

# Loading the pre-trained model data (weights, word lists, etc.)
FILE = "/home/sam/alx/Chatbot-powered-english-learning-platform/EGPT/new/data.pth"
data = torch.load(FILE)

# Extracting the input size, hidden layer size, output size, word list, and tags from the data
input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

# Initializing the GRU model with the pre-trained weights
model = NeuralNetGRU(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()  # Setting the model to evaluation mode

bot_name = "Sam"

# Function to get the chatbot's response
def get_response(msg):
    # Tokenize the input message
    sentence = tokenize(msg)
    
    # Convert the tokenized sentence into a bag of words (BoW) vector
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, 1, X.shape[0])  # Reshape for GRU: (seq_length, batch_size, input_size)
    X = torch.from_numpy(X).to(device)  # Convert to a tensor and move to GPU/CPU
    
    # Initialize the hidden state for GRU with the correct shape
    hidden = torch.zeros(1, 1, hidden_size).to(device)  # (num_layers, batch_size, hidden_size)

    # Get the output and the hidden state from the GRU model
    output = model(X)
    
    # Get the predicted tag (intent) based on maximum value
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    # Apply softmax to get the probability of the prediction
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    
    # If the probability is above the threshold (e.g., 75%), return a response
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                return random.choice(intent['responses'])
    
    # Fallback response if confidence is too low
    return "I do not understand..."

# Entry point of the chatbot application
if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        sentence = input("You: ")
        if sentence == "quit":
            break

        # Get the response from the chatbot and print it
        resp = get_response(sentence)
        print(f"{bot_name}: {resp}")
