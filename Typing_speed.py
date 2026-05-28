from tkinter import *
import time

# ---------------- WINDOW ---------------- #

window = Tk()
window.title("Typing Speed Test")
window.geometry("1000x850")
window.config(bg="#f8fafc")

# ---------------- DATA ---------------- #

sentences = [
    "Python is a powerful programming language.",
    "Artificial intelligence is changing the world.",
    "Typing speed improves with daily practice.",
    "Success comes from continuous learning and practice.",
    "Coding becomes easier with consistency.",
    "Data analytics helps businesses make decisions.",
    "Programming skills improve through regular practice.",
    "Technology is shaping the future of education."
]

start_time = 0
best_wpm = 0
history = []
timer_running = False
current_level = 0

# ---------------- TIMER ---------------- #

def update_timer():
    if timer_running:
        elapsed = int(time.time() - start_time)
        timer_label.config(text=f"⏳ Timer: {elapsed} sec")
        window.after(1000, update_timer)

# ---------------- ERROR CHECK ---------------- #

def check_typing(event=None):
    text_area.tag_remove("wrong", "1.0", END)

    # ✅ FIXED HERE
    typed = text_area.get("1.0", "end-1c")
    original = sentence_label.cget("text")

    error_label.config(text="")

    for i in range(min(len(typed), len(original))):
        if typed[i] != original[i]:

            text_area.tag_add("wrong", f"1.{i}", f"1.{i+1}")

            error_label.config(
                text=f"❌ Wrong at position {i+1}: typed '{typed[i]}' instead of '{original[i]}'"
            )
            break

    text_area.tag_config("wrong", foreground="red")

# ---------------- STRICT INPUT BLOCK ---------------- #

def prevent_wrong_input(event):
    # ✅ FIXED HERE
    typed = text_area.get("1.0", "end-1c")
    original = sentence_label.cget("text")

    pos = len(typed)

    if pos < len(original) and event.char:
        if event.char != original[pos]:
            error_label.config(
                text=f"❌ Wrong letter! Expected '{original[pos]}'"
            )
            return "break"

    if len(typed) >= len(original):
        return "break"

# ---------------- START TEST ---------------- #

def start_test():
    global start_time, timer_running, current_level

    username = username_entry.get().strip()

    if username == "":
        warning_label.config(text="⚠ Please enter your name before starting the test!")
        return
    else:
        warning_label.config(text="")

    current_level = 0

    sentence_label.config(text=sentences[current_level])
    level_label.config(text=f"Level {current_level + 1}")

    text_area.delete("1.0", END)
    error_label.config(text="")

    start_time = time.time()
    timer_running = True
    update_timer()

# ---------------- SUBMIT ---------------- #

def submit_test():
    global best_wpm, timer_running, start_time

    original = sentence_label.cget("text")
    typed = text_area.get("1.0", "end-1c")

    correct = 0
    for i in range(min(len(original), len(typed))):
        if original[i] == typed[i]:
            correct += 1

    accuracy = round((correct / len(original)) * 100)

    timer_running = False
    end_time = time.time()

    total_time = end_time - start_time
    words = len(typed.split())

    wpm = 0 if total_time == 0 else round((words / total_time) * 60)

    username = username_entry.get()
    history.append(f"{username} → {wpm} WPM | {accuracy}%")

    if wpm > best_wpm:
        best_wpm = wpm
        message = "🔥 Amazing! New High Score!"
    elif wpm >= 40:
        message = "👏 Great Typing Speed!"
    else:
        message = "💪 Keep Practicing!"

    test_frame.pack_forget()
    result_frame.pack(fill="both", expand=True)

    current_score.config(text=f"⚡ Speed: {wpm} WPM")
    accuracy_label.config(text=f"🎯 Accuracy: {accuracy}%")
    best_score.config(text=f"🏆 Best Score: {best_wpm} WPM")
    appreciation_label.config(text=message)

    history_box.delete(0, END)
    for item in history:
        history_box.insert(END, item)

    next_btn.config(state=NORMAL)

# ---------------- NEXT ---------------- #

def next_sentence():
    global current_level, start_time, timer_running

    result_frame.pack_forget()
    test_frame.pack(fill="both", expand=True)

    current_level += 1

    if current_level < len(sentences):
        sentence_label.config(text=sentences[current_level])
        level_label.config(text=f"Level {current_level + 1}")
        text_area.delete("1.0", END)
        error_label.config(text="")

        start_time = time.time()
        timer_running = True
        update_timer()
    else:
        sentence_label.config(text="🎉 You completed all levels!")
        level_label.config(text="Completed")

# ---------------- RESET ---------------- #

def try_again():
    global current_level

    current_level = 0

    result_frame.pack_forget()
    test_frame.pack(fill="both", expand=True)

    sentence_label.config(text=sentences[0])
    level_label.config(text="Level 1")

    text_area.delete("1.0", END)
    error_label.config(text="")
    timer_label.config(text="⏳ Timer: 0 sec")

# ---------------- UI ---------------- #

test_frame = Frame(window, bg="#f8fafc")
test_frame.pack(fill="both", expand=True)

Label(test_frame, text="⌨ Typing Speed Test",
      font=("Poppins", 34, "bold"),
      bg="#f8fafc").pack(pady=20)

username_entry = Entry(test_frame, font=("Poppins", 15), justify="center")
username_entry.pack(ipady=8)

warning_label = Label(test_frame, fg="red", bg="#f8fafc")
warning_label.pack()

Button(test_frame, text="▶ Start Test", command=start_test,
       bg="#2563eb", fg="white").pack(pady=15)

level_label = Label(test_frame, text="Level 1",
                    font=("Poppins", 18, "bold"),
                    bg="#f8fafc", fg="#2563eb")
level_label.pack()

sentence_label = Label(test_frame, text="Click Start Test",
                       font=("Poppins", 16),
                       bg="#dbeafe", wraplength=700)
sentence_label.pack(pady=20)

# ERROR LABEL
error_label = Label(test_frame, text="",
                    font=("Poppins", 14, "bold"),
                    bg="#f8fafc", fg="red")
error_label.pack(pady=5)

timer_label = Label(test_frame, text="⏳ Timer: 0 sec",
                    bg="#f8fafc", fg="#2563eb")
timer_label.pack()

text_area = Text(test_frame, font=("Poppins", 14), height=5, width=70)
text_area.pack()

# EVENTS
text_area.bind("<KeyRelease>", check_typing)
text_area.bind("<KeyPress>", prevent_wrong_input)

Button(test_frame, text="✔ Submit", command=submit_test,
       bg="#2563eb", fg="white").pack(pady=20)

# ---------------- RESULT ---------------- #

result_frame = Frame(window, bg="#f8fafc")

Label(result_frame, text="📊 Results",
      font=("Poppins", 30, "bold")).pack(pady=20)

current_score = Label(result_frame, font=("Poppins", 18))
current_score.pack()

accuracy_label = Label(result_frame, font=("Poppins", 18))
accuracy_label.pack()

best_score = Label(result_frame, font=("Poppins", 18))
best_score.pack()

appreciation_label = Label(result_frame, font=("Poppins", 18))
appreciation_label.pack(pady=10)

next_btn = Button(result_frame, text="➡ Next Sentence",
                  command=next_sentence,
                  bg="#16a34a", fg="white",
                  state=DISABLED)
next_btn.pack(pady=10)

history_box = Listbox(result_frame, width=50)
history_box.pack(pady=10)

Button(result_frame, text="🔄 Try Again",
       command=try_again,
       bg="#2563eb", fg="white").pack(pady=10)

window.mainloop()