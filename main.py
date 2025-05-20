# main.py
# (Include all the previous code but add these imports at the top)
import requests
import json

# Inside the MentalHealthAssistant class, modify the process_input method:
def process_input(self, event):
    user_input = self.input_field.get()
    if user_input.strip() == "":
        return
    
    self.display_message(f"You: {user_input}")
    self.input_field.delete(0, tk.END)
    
    # Send to backend
    try:
        response = requests.post('http://localhost:5000/chat', 
                               json={'message': user_input})
    except requests.exceptions.ConnectionError:
        print("Backend server not connected - running in offline mode")
    
    # Generate and display response
    response = self.generate_response(user_input.lower())
    self.display_message(f"Assistant: {response}")
    
    if any(word in user_input.lower() for word in ["suicide", "kill myself", "end it all"]):
        self.display_crisis_resources()

# Add method to log exercises
def log_exercise(self, exercise_name, duration):
    try:
        requests.post('http://localhost:5000/exercise/log', 
                     json={'type': exercise_name, 'duration': duration})
    except requests.exceptions.ConnectionError:
        print("Backend server not connected - running in offline mode")