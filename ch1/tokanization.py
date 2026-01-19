import tiktoken

encoder = tiktoken.encoding_for_model('gpt-4o')
print("Vocab Size ", encoder.n_vocab) # 200019

text = "I m learning AI"
encoded_text = encoder.encode(text)
print("Tokens : ",encoded_text) # [40, 284, 7524, 20837]

my_tokens = [40, 284, 7524, 20837]
decoded_text = encoder.decode(my_tokens)
print("Decoded text : ", decoded_text)