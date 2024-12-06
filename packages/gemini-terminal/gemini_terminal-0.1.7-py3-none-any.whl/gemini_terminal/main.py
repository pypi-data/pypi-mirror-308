import google.generativeai as genai
import pyperclip

PASSWORD = "4i4"  # Simple password storage
last_response = ""  # Store the last response

def verify_password():
    attempts = 3
    while attempts > 0:
        password = input("Enter password to access Gemini Chat: ")
        
        if password == PASSWORD:
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
    global last_response
    
    print("Welcome to Gemini Terminal Chat!")
    print("Commands:")
    print("Press enter two times to send your message")
    print("- Type 'quit' or 'exit' to end chat")
    print("- Type 'copy' to copy last response")
    print("-" * 50)
    
    chat = model.start_chat()
    
    while True:
        print("\nYou: ", end='')
        try:
            # Collect all lines until EOF (Ctrl+D/Ctrl+Z) or single line
            lines = []
            while True:
                try:
                    line = input()
                    if not line:  # Empty line means single-line input mode
                        break
                    lines.append(line)
                except EOFError:  # Ctrl+D/Ctrl+Z pressed
                    break
            
            user_input = '\n'.join(lines) if lines else input()
            
            # Handle commands
            if user_input.lower() == 'copy':
                if last_response:
                    # Clean the response before copying
                    cleaned_copy = last_response.replace('```', '').replace('`', '')
                    pyperclip.copy(cleaned_copy)
                    print("Last response copied to clipboard!")
                else:
                    print("No response to copy yet!")
                continue
            
            if user_input.lower() in ['quit', 'exit']:
                print("\nGoodbye!")
                break
                
            try:
                response = chat.send_message(user_input)
                # Clean and store the response
                last_response = response.text.replace('```', '').replace('`', '')
                
                # Format the response with clear separation
                print("\nGemini:", end='\n\n')  # Add extra newline for spacing
                print(last_response)
                print()  # Add extra newline after response
                
            except Exception as e:
                print(f"\nError: {str(e)}")
                
        except KeyboardInterrupt:  # Handle Ctrl+C
            print("\nUse 'quit' or 'exit' to end the chat")
            continue

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