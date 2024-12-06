import google.generativeai as genai
import hashlib


CORRECT_PASSWORD_HASH = "8c9c0a3b3c6d6a9e4c1e4c1e4c1e4c1e4c1e4c1e4c1e4c1e4c1e4c1e4c1e4c1"

def verify_password():
    attempts = 3
    while attempts > 0:
        password = input("Enter password to access Gemini Chat: ")
        hashed_input = hashlib.sha256(password.encode()).hexdigest()
        
        if hashed_input == CORRECT_PASSWORD_HASH:
            return True
        
        attempts -= 1
        print(f"Incorrect password. {attempts} attempts remaining.")
    
    return False

def initialize_gemini():
    api_key = "AIzaSyA8GHU0QhwXkgCXEBYnost56YOPmsd2pPs"
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    return model

def chat_loop(model):
    print("Welcome to Gemini Terminal Chat! (Type 'quit' to exit)")
    print("-" * 50)
    
    chat = model.start_chat()
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() in ['quit', 'exit']:
            print("\nGoodbye!")
            break
            
        try:
            response = chat.send_message(user_input)
            print("\nGemini:", response.text)
        except Exception as e:
            print(f"\nError: {str(e)}")

def main():
    try:
        if not verify_password():
            print("Too many failed attempts. Access denied.")
            return
            
        model = initialize_gemini()
        chat_loop(model)
    except Exception as e:
        print(f"Failed to initialize Gemini: {str(e)}")

if __name__ == "__main__":
    main() 