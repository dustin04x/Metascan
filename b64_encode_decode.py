import base64
import re


def encode_to_base64(input_string: str) -> str:
    try:
        sample_string_bytes = input_string.encode("utf-8")
        base64_bytes = base64.b64encode(sample_string_bytes)
        base64_string = base64_bytes.decode("utf-8")
        return base64_string
    except Exception as e:
        raise ValueError(f"Error encoding string: {e}")


def decode_from_base64(base64_string: str) -> str:
    
    try:
        base64_bytes = base64_string.encode("utf-8")
        sample_string_bytes = base64.b64decode(base64_bytes, validate=True)
        sample_string = sample_string_bytes.decode("utf-8")
        return sample_string
    except Exception as e:
        raise ValueError(f"Error decoding base64: {e}")


def is_valid_base64(s: str) -> bool:
    
    if not s or not re.match(r'^[A-Za-z0-9+/]*={0,2}$', s) or len(s) % 4 != 0:
        return False
    try:
        base64.b64decode(s, validate=True)
        return True
    except Exception:
        return False

def main():
    txt = input("Encode or decode (e/d)? ").strip().lower()
    
    if txt == 'e':
        user_input = input("Enter string to encode: ")
        try:
            result = encode_to_base64(user_input)
            print("Encoded string:", result)
        except ValueError as e:
            print(f"Error: {e}")
    elif txt == 'd':
        user_input = input("Enter base64 string to decode: ").strip()
        if not is_valid_base64(user_input):
            print("Error: Invalid base64 format")
            return
        try:
            result = decode_from_base64(user_input)
            print("Decoded string:", result)
        except ValueError as e:
            print(f"Error: {e}")
    else:
        print("Invalid option. Please enter 'e' or 'd'.")


if __name__ == "__main__":
    main()
