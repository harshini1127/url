from nanoid import generate

# choose an alphabet and size; 7-8 chars is common
ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
SIZE = 7

def generate_short_id():
    return generate(ALPHABET, SIZE)
