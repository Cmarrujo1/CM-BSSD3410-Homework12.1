# Code Taken From: https://rosettacode.org/wiki/LZW_compression#Python

import pickle
from io import StringIO

def compress(uncompressed):
    """Compress a string to a list of output symbols."""

    # Build the dictionary.
    dict_size = 256
    dictionary = {chr(i): i for i in range(dict_size)}
    # in Python 3: dictionary = {chr(i): i for i in range(dict_size)}

    w = ""
    result = []
    for c in uncompressed:
        wc = w + c

        if wc in dictionary:
            w = wc

        else:
            result.append(dictionary[w])
            # Add wc to the dictionary.
            dictionary[wc] = dict_size
            dict_size += 1
            w = c

    # Output the code for w.
    if w:
        result.append(dictionary[w])
    return result

def decompress(compressed):
    """Decompress a list of output ks to a string."""

    # Build the dictionary.
    dict_size = 256
    dictionary = {i: chr(i) for i in range(dict_size)}
    # in Python 3: dictionary = {i: chr(i) for i in range(dict_size)}

    # use StringIO, otherwise this becomes O(N^2)
    # due to string concatenation in a loop
    result = StringIO()
    w = chr(compressed.pop(0))
    result.write(w)
    for k in compressed:
        if k in dictionary:
            entry = dictionary[k]

        elif k == dict_size:
            entry = w + w[0]

        else:
            raise ValueError(f"Bad compressed : {k}")
        result.write(entry)

        # Add w+entry[0] to the dictionary.
        dictionary[dict_size] = w + entry[0]
        dict_size += 1
        w = entry
    return result.getvalue()


def save_compressed_data(filename, compressed_data):
    with open(filename, 'wb') as file:
        pickle.dump(compressed_data, file)


def load_and_decompress(filename):
    with open(filename, 'rb') as file:
        compressed_data = pickle.load(file)
    return decompress(compressed_data)


def main():
    with open("alice.txt", 'r', encoding='utf-8') as file:
        text = file.read()
    text = ''.join([char for char in text if ord(char) < 128])

    compressed_data = compress(text)
    print("Compression done.")

    save_compressed_data("compressed_alice.pkl", compressed_data)
    print("Saved file.")

    decompressed_text = load_and_decompress("compressed_alice.pkl")
    print("Decompressed data loaded...")
    print("45 characters :")
    print(decompressed_text[:45])

if __name__ == "__main__":
    main()
