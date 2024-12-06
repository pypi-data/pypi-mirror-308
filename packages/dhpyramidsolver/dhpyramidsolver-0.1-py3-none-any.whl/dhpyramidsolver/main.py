import base64

def print_flag():
    try:
        with open('/flag', 'rb') as f:
            encoded_flag = base64.b64encode(f.read()).decode('utf-8')
            print(f"Encoded flag: {encoded_flag}")
    except FileNotFoundError:
        print("File not found.")
