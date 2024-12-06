import google.generativeai as genai

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
        model = initialize_gemini()
        chat_loop(model)
    except Exception as e:
        print(f"Failed to initialize Gemini: {str(e)}")

if __name__ == "__main__":
    main() 