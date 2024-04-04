import tkinter as tk
from tkinter import messagebox
import time
import requests

class TypingSpeedTestApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Typing Speed Test")
        
        self.label = tk.Label(master, text="Type the following text:")
        self.label.pack()
        
        self.sample_text = tk.Text(master, height=5, width=50, state=tk.DISABLED)
        self.sample_text.pack()
        
        self.input_text = tk.Text(master, height=5, width=50)
        self.input_text.pack()
        self.input_text.bind("<Key>", self.check_typing)
        
        self.start_button = tk.Button(master, text="Start Typing Test", command=self.start_test)
        self.start_button.pack()
        
    def start_test(self):
        self.sample_text.config(state=tk.NORMAL)
        self.sample_text.delete('1.0', tk.END)
        sentence = self.get_random_sentence()
        self.sample_text.insert(tk.END, sentence)
        self.sample_text.tag_configure("correct", foreground="green")
        self.sample_text.tag_configure("incorrect", foreground="red")
        self.sample_text.config(state=tk.DISABLED)
        self.start_time = time.time()
        self.input_text.focus_set()
        
    def get_random_sentence(self):
        url = "https://api.quotable.io/random"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("content")
        else:
            print("Failed to fetch random sentence.")
            return "Failed to fetch sentence."
        
    def check_typing(self, event):
        input_text = self.input_text.get("1.0", tk.END).strip()
        sample_text = self.sample_text.get("1.0", tk.END).strip()
        
        if input_text == sample_text:
            self.stop_test()
            return
        
        min_len = min(len(input_text), len(sample_text))
        
        for i in range(min_len):
            if input_text[i] == sample_text[i]:
                self.sample_text.tag_add("correct", f"1.{i}", f"1.{i+1}")
                self.sample_text.tag_remove("incorrect", f"1.{i}", f"1.{i+1}")
            else:
                self.sample_text.tag_add("incorrect", f"1.{i}", f"1.{i+1}")
                self.sample_text.tag_remove("correct", f"1.{i}", f"1.{i+1}")
        
        if len(input_text) > min_len:
            self.sample_text.tag_add("incorrect", f"1.{min_len}", tk.END)
        elif len(sample_text) > min_len:
            self.sample_text.tag_remove("incorrect", f"1.{min_len}", tk.END)
        
    def stop_test(self, event=None):
        end_time = time.time()
        typed_text = self.input_text.get('1.0', tk.END)
        elapsed_time = end_time - self.start_time
        words_typed = len(typed_text.split())
        wpm = int(words_typed / (elapsed_time / 60))
        messagebox.showinfo("Result", f"Your typing speed: {wpm} WPM")

def main():
    root = tk.Tk()
    app = TypingSpeedTestApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
