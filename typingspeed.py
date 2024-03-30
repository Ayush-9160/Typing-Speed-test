import tkinter as tk
import random
import time

class TypingSpeedTest:
    def __init__(self, master):
        self.master = master
        self.master.title("Typing Speed Test")

        self.sentences = [
            "The quick brown fox jumps over the lazy dog.",
            "She sells seashells by the seashore.",
            "Peter Piper picked a peck of pickled peppers.",
            "How much wood would a woodchuck chuck if a woodchuck could chuck wood?",
            "The cat in the hat came back.",
            "A stitch in time saves nine.",
            "All that glitters is not gold.",
            "Better late than never."
        ]
        self.info_label = tk.Label(self.master, text="", wraplength=800,font=('Arial', 15))  
        self.info_label.pack(padx=20, pady=(200, 0))

        self.entry = tk.Entry(self.master, font=('Arial', 14),width='40')
        self.entry.pack(pady=50)

        self.start_button = tk.Button(self.master, text="Start Test", command=self.start_test)
        self.start_button.pack()

        self.reset_button = tk.Button(self.master, text="Reset", command=self.reset)
        self.reset_button.pack()
        self.reset_button['state'] = 'disabled'

        self.result_label = tk.Label(self.master, text="")
        self.result_label.pack()

        self.remaining_time_label = tk.Label(self.master, text="")
        self.remaining_time_label.pack()

        self.timer_running = False

        self.duration_var = tk.StringVar(self.master)
        self.duration_var.set('5 sec')

        self.duration_mapping = {'5 sec': 5,'30 sec': 30, '1 min': 60, '2 min': 120}

    def generate_text(self, duration):
        return ' '.join(random.choices(self.sentences, k=6))

    def start_test(self):
        duration = self.duration_var.get()
        self.start_time = time.time()
        self.end_time = self.start_time + self.duration_mapping[duration]
        self.reset_button['state'] = 'normal'
        self.start_button['state'] = 'disabled'
        self.test_text = self.generate_text(duration)
        self.info_label.config(text=self.test_text)
        self.entry.delete(0, tk.END)
        self.entry.bind('<Return>', self.check_input)
        self.timer_running = True
        self.update_time()

    def update_time(self):
        if self.timer_running:
            remaining_time = max(0, self.end_time - time.time())
            minutes = int(remaining_time // 60)
            seconds = int(remaining_time % 60)
            self.remaining_time_label.config(text=f"Time remaining: {minutes:02d}:{seconds:02d}")
            if remaining_time <= 0:
                self.remaining_time_label.config(text="Time's up!")
                self.timer_running = False
                self.entry.unbind('<Return>')
                self.display_results()
            else:
                self.master.after(1000, self.update_time)

    def display_results(self):
        typed_text = self.entry.get()
        accuracy = self.calculate_accuracy(typed_text)
        wpm = self.calculate_wpm(typed_text)
        self.result_label.config(text=f"Accuracy: {accuracy:.2f}%  WPM: {wpm:.2f}")
        self.start_button['state'] = 'normal'

    def check_input(self, event):
        if not self.timer_running:
            self.entry.unbind('<Return>')
            self.display_results()

    def calculate_accuracy(self, typed_text):
        typed_words = typed_text.lower().split()  
        test_words = self.test_text.lower().split() 
        correct_words = sum(1 for typed, test in zip(typed_words, test_words) if typed == test)
        return (correct_words / len(typed_words)) * 100 if typed_words else 0

    def calculate_wpm(self, typed_text):
        words_typed = len(typed_text.split())
        time_taken = time.time() - self.start_time
        wpm = (words_typed / time_taken) * 60
        return wpm

    def reset(self):
        self.timer_running = False
        self.entry.unbind('<Return>')
        self.reset_button['state'] = 'disabled'
        self.start_button['state'] = 'normal'
        self.info_label.config(text="")
        self.result_label.config(text="")
        self.remaining_time_label.config(text="")
        self.entry.delete(0, tk.END)

    def run(self):
        duration_options = ['5 sec','30 sec', '1 min', '2 min']
        duration_menu = tk.OptionMenu(self.master, self.duration_var, *duration_options)
        duration_menu.pack()

        self.master.mainloop()

root = tk.Tk()
test = TypingSpeedTest(root)
test.run()