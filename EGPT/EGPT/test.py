from model import *
voc = Voc("name")
def load_model(filename):
    checkpoint = torch.load(filename)
    encoder_sd = checkpoint['encoder']
    decoder_sd = checkpoint['decoder']
    searcher_sd = checkpoint['searcher']
    voc_sd = checkpoint['voc']

    encoder = EncoderRNN(hidden_size, embedding, encoder_n_layers, dropout)
    decoder = LuongAttnDecoderRNN(attn_model, embedding, hidden_size, voc.num_words, decoder_n_layers, dropout)
    searcher = GreedySearchDecoder(encoder, decoder)

    encoder.load_state_dict(encoder_sd)
    decoder.load_state_dict(decoder_sd)
    searcher.load_state_dict(searcher_sd)

    voc = Voc()
    voc.__dict__ = voc_sd

    return encoder, decoder, searcher, voc

encoder, decoder, searcher, voc = load_model('chatbot_model.pth')

def evaluateInput(encoder, decoder, searcher, voc):
    input_sentence = ''
    while(1):
        try:
            # Get input sentence
            input_sentence = input('> ')
            # Check if it is quit case
            if input_sentence == 'q' or input_sentence == 'quit': break
            # Normalize sentence
            input_sentence = normalizeString(input_sentence)
            # Evaluate sentence
            output_words = evaluate(encoder, decoder, searcher, voc, input_sentence)
            # Format and print response sentence
            output_words[:] = [x for x in output_words if not (x == 'EOS' or x == 'PAD')]
            print('Bot:', ' '.join(output_words))

        except KeyError:
            print("Error: Encountered unknown word.")
evaluateInput(encoder, decoder, searcher, voc)