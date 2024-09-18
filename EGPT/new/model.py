import torch
import torch.nn as nn

class NeuralNetGRU(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNetGRU, self).__init__()
        self.hidden_size = hidden_size
        self.gru = nn.GRU(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        # Initialize hidden state
        h0 = torch.zeros(1, x.size(0), self.hidden_size).to(x.device)

        # Forward propagate GRU
        out, _ = self.gru(x, h0)

        # Take the output of the last time step
        out = self.fc(out[:, -1, :])

        return out
