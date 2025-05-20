import tkinter as tk
from tkinter import ttk, scrolledtext, font 
import pygame
import random
import time
from PIL import Image, ImageTk, ImageDraw
import json
import requests
import math
from datetime import datetime
import colorsys
import random

class CustomButton(tk.Canvas):
    def __init__(self, parent, text, command, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(highlightthickness=0, bg='#f0f0f0')
        
        self.command = command
        
        # Create rounded rectangle
        self.create_rounded_rect(5, 5, 200, 50, 15)  # Width, height, and corner radius
        self.text_id = self.create_text(100, 25, text=text, fill='white', font=('Arial', 11, 'bold'))
        
        # Bind events
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        self.bind('<Button-1>', self.on_click)
        
    def create_rounded_rect(self, x1, y1, x2, y2, radius):
        """Draws a rounded rectangle on the canvas."""
        self.create_arc(x1, y1, x1 + 2 * radius, y1 + 2 * radius, start=90, extent=90, fill='#4a90e2', outline='')
        self.create_arc(x2 - 2 * radius, y1, x2, y1 + 2 * radius, start=0, extent=90, fill='#4a90e2', outline='')
        self.create_arc(x2 - 2 * radius, y2 - 2 * radius, x2, y2, start=270, extent=90, fill='#4a90e2', outline='')
        self.create_arc(x1, y2 - 2 * radius, x1 + 2 * radius, y2, start=180, extent=90, fill='#4a90e2', outline='')

        self.create_rectangle(x1 + radius, y1, x2 - radius, y2, fill='#4a90e2', outline='')
        self.create_rectangle(x1, y1 + radius, x2, y2 - radius, fill='#4a90e2', outline='')

    def on_enter(self, event):
        """Handles hover effect for the button."""
        self.itemconfig(self.text_id, fill='#cfe2ff')
        self.configure(bg='#357abd')

    def on_leave(self, event):
        """Resets the button appearance on hover leave."""
        self.itemconfig(self.text_id, fill='white')
        self.configure(bg='#4a90e2')

    def on_click(self, event):
        """Calls the assigned command on click."""
        self.command()

class BreathingCircle(tk.Canvas):
    def __init__(self, parent, breath_in_seconds=4, breath_out_seconds=6, hold_seconds=1):
        super().__init__(parent, width=400, height=400, bg='black', highlightthickness=0)
        
        # Breathing configuration
        self.breath_in_seconds = breath_in_seconds
        self.breath_out_seconds = breath_out_seconds
        self.hold_seconds = hold_seconds
        
        # Animation parameters
        self.size = 100
        self.max_size = 250
        self.animation_speed = 2
        self.phase = 'breathe_in'
        self.current_time = 0
        
        # Styling
        self.custom_font = font.Font(family='Arial', size=16, weight='bold')
        self.instruction_font = font.Font(family='Arial', size=12)
        
        # Create initial visualization
        self.create_breathing_circle()
        
    def create_gradient_colors(self, steps, start_hue=240, end_hue=280):
        """Create a gradient of colors from start_hue to end_hue"""
        colors = []
        for i in range(steps):
            # Interpolate between start and end hue
            hue = (start_hue + (i * (end_hue - start_hue) / steps)) % 360 / 360
            # Use softer saturation and brightness for calming effect
            rgb = colorsys.hsv_to_rgb(hue, 0.6, 0.8)
            colors.append('#{:02x}{:02x}{:02x}'.format(
                int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255)
            ))
        return colors
    
    def create_breathing_circle(self):
        """Create the breathing visualization with gradient and instructions"""
        # Clear previous drawings
        self.delete('all')
        
        # Create gradient circles
        gradient_colors = self.create_gradient_colors(20)
        
        for i in range(len(gradient_colors)-1, -1, -1):
            size = self.size - (i * 3)
            if size > 0:
                # Create softer, more blended gradient circles
                self.create_oval(
                    200-size/2, 200-size/2,
                    200+size/2, 200+size/2,
                    fill=gradient_colors[i],
                    outline='',
                    tags='breathing_circle'
                )
        
        # Add breathing instructions
        if self.phase == 'breathe_in':
            instruction = f"Breathe In\n{self.breath_in_seconds} seconds"
            color = 'lightblue'
        elif self.phase == 'hold':
            instruction = f"Hold\n{self.hold_seconds} seconds"
            color = 'lightgreen'
        else:  # breathe_out
            instruction = f"Breathe Out\n{self.breath_out_seconds} seconds"
            color = 'lavender'
        
        # Create central text
        self.create_text(
            200, 200,
            text="Breathe",
            fill='white',
            font=self.custom_font,
            tags='central_text'
        )
        
        # Create instruction text
        self.create_text(
            200, 250,
            text=instruction,
            fill=color,
            font=self.instruction_font,
            tags='instruction_text'
        )
    
    def animate(self):
        """Animate breathing cycle with precise timing"""
        # Breathing In
        if self.phase == 'breathe_in':
            self.size += self.animation_speed
            self.current_time += 0.05
            
            if self.current_time >= self.breath_in_seconds:
                self.phase = 'hold'
                self.current_time = 0
            
        # Holding Breath
        elif self.phase == 'hold':
            self.current_time += 0.05
            
            if self.current_time >= self.hold_seconds:
                self.phase = 'breathe_out'
                self.current_time = 0
        
        # Breathing Out
        elif self.phase == 'breathe_out':
            self.size -= self.animation_speed
            self.current_time += 0.05
            
            if self.current_time >= self.breath_out_seconds:
                self.phase = 'breathe_in'
                self.current_time = 0
        
        # Ensure size stays within bounds
        self.size = max(100, min(self.size, self.max_size))
        
        # Update visualization
        self.create_breathing_circle()
        
        # Continue animation
        self.after(50, self.animate)

class MentalHealthAssistant:
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mental Health Assistant")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a1a')  # Dark theme
        
        # Indian crisis helpline numbers
        self.crisis_numbers = {
            "AASRA": "91-9820466726",
            "Sneha India": "044-24640050",
            "Vandrevala Foundation": "1860-2662-345",
            "iCall": "022-25521111",
            "Emergency": "112"
        }
        
        # Enhanced empathetic responses
        self.responses = {
            "depression": [
                "I hear the pain in your words, and I want you to know that you're not alone in this journey. Could you tell me more about what's weighing on your heart?",
                "It takes courage to share these feelings. Depression can feel overwhelming, but together we can explore ways to help you feel better. What has been particularly challenging lately?",
                "I'm here to support you through this difficult time. Sometimes taking small steps can make a difference. Would you like to try a gentle breathing exercise together?",
                "Your feelings are valid, and it's okay to not be okay. Let's work together to find moments of light in these dark times."
            ],
            "anxiety": [
                "I can sense that you're feeling anxious, and that's perfectly normal. Let's take a moment to breathe together and ground ourselves. Would you like that?",
                "Anxiety can feel like a storm inside. I'm here to be your calm harbor. Can you tell me what's triggering these feelings?",
                "You're showing strength by reaching out. Let's explore some gentle techniques that might help ease your anxiety. Would you like to try a grounding exercise?",
                "Your feelings matter, and we'll work through this together at your pace. What would feel most supportive right now?"
            ],
            "gratitude": [
                "I'm so glad I could be here for you. Remember, you can always return whenever you need support. Take good care of yourself! 🌸",
                "Thank you for trusting me with your feelings. You've shown great courage today. Please come back anytime you need someone to talk to. Be gentle with yourself! 💫",
                "I'm happy that you're feeling better. Remember, seeking help is a sign of strength, not weakness. Wishing you peace and well-being! ✨",
                "Your well-being matters, and I'm here whenever you need support. Take care and be kind to yourself! 🌟"
            ]
        }
        
        self.create_enhanced_gui()
        self.initialize_visualization()
        
    def create_enhanced_gui(self):
        # Main container with gradient background
        main_container = ttk.Frame(self.root)
        main_container.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Configure grid
        main_container.grid_columnconfigure(0, weight=7)
        main_container.grid_columnconfigure(1, weight=3)
        
        # Create chat interface
        self.create_enhanced_chat_interface(main_container)
        
        # Create exercise panel
        self.create_enhanced_exercise_panel(main_container)
        
    def create_enhanced_chat_interface(self, container):
        chat_frame = ttk.LabelFrame(container, text="Chat with Your Mental Health Assistant")
        chat_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Styled chat history
        style = ttk.Style()
        style.configure("Custom.TFrame", background="#2d2d2d")
        
        self.chat_history = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            width=50,
            height=30,
            font=("Arial", 15),
            bg="#2d2d2d",
            fg="#ffffff",
            insertbackground="#ffffff"
        )
        self.chat_history.pack(padx=10, pady=10, expand=True, fill="both")
        
        # Styled input area
        input_frame = ttk.Frame(chat_frame, style="Custom.TFrame")
        input_frame.pack(fill="x", padx=10, pady=5)
        
        self.input_field = tk.Entry(
            input_frame,
            font=("Arial", 11),
            bg="#3d3d3d",
            fg="#ffffff",
            insertbackground="#ffffff"
        )
        self.input_field.pack(side="left", expand=True, fill="x", padx=(0, 5))
        self.input_field.bind("<Return>", self.process_input)
        
        send_button = CustomButton(
            input_frame,
            text="Send",
            command=lambda: self.process_input(None),
            width=200,
            height=50
        )
        send_button.pack(side="right")
        
        # Welcome message
        self.display_message("Assistant: Hello! 🌟 I'm here to support you on your journey. How are you feeling today?")
        
    def create_enhanced_exercise_panel(self, container):
        exercise_frame = ttk.LabelFrame(container, text="Wellness Center")
        exercise_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # Visualization canvas
        self.viz_canvas = tk.Canvas(
            exercise_frame,
            width=300,
            height=200,
            bg='black',
            highlightthickness=0
        )
        self.viz_canvas.pack(pady=10)
        
        # Exercise buttons
        exercises = [
            ("Deep Breathing Journey", self.start_breathing_exercise),
            ("Calming Visualization", self.start_visualization),
            ("Grounding Experience", self.start_grounding_exercise),
            ("Mindful Meditation", self.start_mindfulness_exercise)
        ]
        
        for text, command in exercises:
            CustomButton(
                exercise_frame,
                text=text,
                command=command,
                width=200,
                height=50
            ).pack(pady=5)
        
        # Crisis resources with styling
        ttk.Label(
            exercise_frame,
            text="24/7 Support Lines",
            font=("Arial", 12, "bold"),
            foreground="#4a90e2"
        ).pack(pady=(20, 10))
        
        for service, number in self.crisis_numbers.items():
            frame = ttk.Frame(exercise_frame)
            frame.pack(fill="x", pady=5, padx=10)
            
            ttk.Label(
                frame,
                text=f"{service}:",
                font=("Arial", 15, "bold")
            ).pack(side="left")
            
            ttk.Label(
                frame,
                text=number,
                font=("Arial", 15)
            ).pack(side="right")
    
    def initialize_visualization(self):
        self.particles = []
        self.update_visualization()
    
    def update_visualization(self):
        self.viz_canvas.delete("all")
        
        # Create calming particle effect
        t = time.time() * 0.5
        for i in range(20):
            x = 150 + math.cos(t + i * 0.5) * 50
            y = 100 + math.sin(t + i * 0.5) * 50
            color = '#{:02x}{:02x}{:02x}'.format(
                int(128 + math.sin(t) * 64),
                int(128 + math.cos(t * 0.5) * 64),
                255
            )
            self.viz_canvas.create_oval(
                x-5, y-5, x+5, y+5,
                fill=color,
                outline=''
            )
        
        self.root.after(50, self.update_visualization)
    
    def process_input(self, event):
        user_input = self.input_field.get()
        if user_input.strip() == "":
            return
        
        self.display_message(f"You: {user_input}")
        self.input_field.delete(0, tk.END)
        
        # Check for exit keywords
        if any(word in user_input.lower() for word in ["thank you", "thanks", "feeling better", "goodbye", "bye"]):
            response = random.choice(self.responses["gratitude"])
        else:
            response = self.generate_enhanced_response(user_input.lower())
        
        self.display_message(f"Assistant: {response}")
        
        # Check for crisis keywords
        if any(word in user_input.lower() for word in ["suicide", "kill myself", "end it all","end my life","die"]):
            self.display_crisis_resources()
    
    def generate_enhanced_response(self, user_input):
        if any(word in user_input for word in ["depressed", "sad", "hopeless", "lonely"]):
            return random.choice(self.responses["depression"])
        elif any(word in user_input for word in ["anxious", "worried", "panic", "stress"]):
            return random.choice(self.responses["anxiety"])
        elif any(word in user_input for word in ["suicide", "kill myself", "end it all","end my life","dont want to live"]):
            return "I'm deeply concerned about your safety and well-being. You are valuable and your life matters. Please let me connect you with someone who can help right now. Would you like the number for a crisis helpline?"
        else:
            return "I hear you, and I'm here to support you. Could you tell me more about what's on your mind?"
    
    def display_message(self, message):
        timestamp = datetime.now().strftime("%H:%M")
        self.chat_history.insert(tk.END, f"[{timestamp}] {message}\n")
        self.chat_history.see(tk.END)
        
        # Add some visual styling
        self.chat_history.tag_add("timestamp",
            f"end-{len(message)+12}c linestart",
            f"end-{len(message)}c"
        )
        self.chat_history.tag_config("timestamp", foreground="#808080")
    
    def start_breathing_exercise(self):
        exercise_window = tk.Toplevel(self.root)
        exercise_window.title("Deep Breathing Journey")
        exercise_window.geometry("400x400")
        exercise_window.configure(bg='black')
        
        breathing_circle = BreathingCircle(exercise_window)
        breathing_circle.pack(expand=True, fill="both", padx=20, pady=20)
        breathing_circle.animate()
    
    def start_visualization(self):
        exercise_window = tk.Toplevel(self.root)
        exercise_window.title("Calming Visualization")
        exercise_window.geometry("400x400")
        exercise_window.configure(bg='black')
        
        canvas = tk.Canvas(exercise_window, width=400, height=400, bg='black', highlightthickness=0)
        canvas.pack()
        
        def update_particles():
            canvas.delete("all")
            t = time.time()
            for i in range(30):
                x = 200 + math.cos(t + i * 0.2) * (100 + math.sin(t * 0.5) * 20)
                y = 200 + math.sin(t + i * 0.2) * (100 + math.cos(t * 0.5) * 20)
                size = 5 + math.sin(t + i) * 2
                
                hue = (t * 0.1 + i * 0.02) % 1.0
                rgb = colorsys.hsv_to_rgb(hue, 0.8, 0.9)
                color = '#{:02x}{:02x}{:02x}'.format(
                    int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255)
                )
                
                canvas.create_oval(
                    x-size,
                    y-size, 
                x+size, 
                y+size, 
                fill=color, 
                outline=''
                )

            canvas.after(50, update_particles)

        update_particles()

    def start_grounding_exercise(self):
        exercise_window = tk.Toplevel(self.root)
        exercise_window.title("Grounding Experience")
        exercise_window.geometry("400x400")
        exercise_window.configure(bg='black')

        label = ttk.Label(
            exercise_window,
            text="5-4-3-2-1 Grounding Technique:\n\n"
                 "5 Things You Can See\n"
                 "4 Things You Can Touch\n"
                 "3 Things You Can Hear\n"
                 "2 Things You Can Smell\n"
                 "1 Thing You Can Taste\n\n"
                 "Take your time to observe your surroundings.",
            font=("Arial", 22),
            foreground="black",
            background="white",
            justify="center",
            wraplength=380
        )
        label.pack(pady=20)

    def start_mindfulness_exercise(self):
        exercise_window = tk.Toplevel(self.root)
        exercise_window.title("Mindful Meditation")
        exercise_window.geometry("400x400")
        exercise_window.configure(bg='black')

        label = ttk.Label(
            exercise_window,
            text="Let's meditate for a moment. Close your eyes, focus on your breath, "
                 "and let go of any tension. Imagine a calm, peaceful place. "
                 "Breathe deeply in... and out...",
            font=("Arial", 22),
            foreground="black",
            background="white",
            justify="center",
            wraplength=380
        )
        label.pack(pady=20)

    def display_crisis_resources(self):
        crisis_window = tk.Toplevel(self.root)
        crisis_window.title("Crisis Helpline Numbers")
        crisis_window.geometry("300x200")
        crisis_window.configure(bg='white')

        ttk.Label(
            crisis_window,
            text="You are not alone. Please reach out to these helplines:",
            font=("Arial", 22, "bold"),
            foreground="red",
            background="white",
            wraplength=280
        ).pack(pady=10)

        for service, number in self.crisis_numbers.items():
            ttk.Label(
                crisis_window,
                text=f"{service}: {number}",
                font=("Arial", 20),
                foreground="red",
                background="white"
            ).pack(anchor="w", padx=10)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = MentalHealthAssistant()
    app.run()