from PIL import Image
import numpy as np
from random import *
from math import *
import time

def encode_text(text, shift_val):
    result = ""
    for char in text:
        if char.isupper():
            result += chr((ord(char) + shift_val - 65) % 26 + 65)
        elif char.islower():
            result += chr((ord(char) + shift_val - 97) % 26 + 97)
        else:
            result += char
    return result

def decode_text(text, shift_val):
    result = ""
    for char in text:
            if char.isupper():
                result += chr((ord(char) - shift_val - 65) % 26 + 65)
            elif char.islower():
                result += chr((ord(char) - shift_val - 97) % 26 + 97)
            else:
                result += char
    return result

def image_encode(text):
    if text.endswith(".txt") or text.endswith(".text"):
        with open(text, "r", encoding="utf-8") as file:
            text = file.read()

    seed = randint(0,255)
    text = text.encode("ascii", "ignore").decode()
    text_list = list(text)

    for k,v in enumerate(text_list):
        if v.isdigit() and text_list[k-1] == "/" and text_list[k-2] == "/":
            reverse_num = int(v)
            next_chars = text_list[k+1:k+reverse_num+1]
            next_chars.reverse()
            text_list = [*text_list[0:k-2], *next_chars, *text_list[k+reverse_num+1::]]
            
    text = "".join(text_list)
    text = encode_text(text, seed)

    ascii_text = [ord(letter) for letter in text]

    size = len(ascii_text)
    size = (isqrt(size // 3) + 1) ** 2

    pixels = [seed, 0, 0]
    for i in range(size * 3 - 3):
        if i >= len(ascii_text):
            pixels.append(0)
            continue
        pixels.append(ascii_text[i])

    pixels = np.array(pixels, dtype=np.uint8)
    pixels = pixels.reshape((isqrt(size), isqrt(size), 3))

    img = Image.fromarray(pixels)
    print("This image is saved under converted.png")
    img.save("converted.png", format="PNG")

def image_decode(img_title):
    with Image.open(img_title) as img:
        pixels = np.asarray(img)
        pixels = pixels.flatten().tolist()
        seed = pixels[0]
        text = ""
        for i in pixels[3::]:
            text += chr(i)
        text = decode_text(text, seed)
        print(text)
        

valid_ops = ["image", "text", "encode", "decode"]
operation = ""
while operation.lower() not in valid_ops:
    operation = input("Please select an operation (image or text): ")

if operation == "image" or operation == "encode":
    start_time = time.perf_counter()
    image_encode(input("Type in the text or file name you want to encode: "))
else:
    time.sleep(1)
    print("Please make sure your file is in the same folder as this program")
    time.sleep(1)
    start_time = time.perf_counter()
    image_decode(input("Enter file name: "))

end_time = time.perf_counter()
elapsed = end_time - start_time
print(f"{elapsed} secs")
