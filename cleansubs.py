import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import re

# Enable DPI awareness for Windows
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception as e:
    print("High DPI awareness could not be set:", e)

# Profanity list
PROFANITY_LISTS = {
    "U": ["MOTHERFUCKER", "FATHERFUCKER", "FUCK", "FUCKED", "FUCKER", "FUCKING", "FUCKTARD", "BITCH",
          "Son of a Bitch", "Biatch", "BASTARD", "BALLS", "CUNT", "DICK", "DICKHEAD", "ASSHOLE", "ARSEHOLE",
          "COCK", "BLOW JOB", "HANDJOB", "BONER", "FELLATIO", "FELTCH", "HARD ON", "JIZZ", "RIMJOB", "CUNNILINGUS",
          "MASTURBATE", "ERECTION", "CAMELTOE", "PUSSY", "SLUT", "HOE", "WHORE", "BUTTHOLE", "SHITHOLE", "CRAPHOLE",
          "SUCK", "BALLOCKS", "NUTS", "NUTSACK", "BEANBAG", "TITS", "BOOBS", "PENIS", "VAGINA", "TESTICLE",
          "SCROTUM", "BREAST", "BUTTOCKS", "BUM", "SUCKER", "BASTARDS", "ASSHOLES", "BITCHES"],
    "P12 & 13": ["MOTHERFUCKER", "FATHERFUCKER", "FUCK", "FUCKED", "FUCKER", "FUCKING", "FUCKTARD", "BITCH",
                "Son of a Bitch", "Biatch", "BASTARD", "BALLS", "CUNT", "DICK", "DICKHEAD", "ASSHOLE", "ARSEHOLE",
                "COCK", "BLOW JOB", "HANDJOB", "BONER", "FELLATIO", "FELTCH", "HARD ON", "JIZZ", "RIMJOB", "CUNNILINGUS",
                "MASTURBATE", "ERECTION", "CAMELTOE", "PUSSY", "WANKER", "JERK OFF", "JERKING", "WANKING", "SUCK",
                "SUCKER", "BASTARDS", "ASSHOLES", "BITCHES"],
    "16 & 18": ["MOTHERFUCKER", "FATHERFUCKER", "FUCK", "FUCKED", "FUCKER", "FUCKING", "FUCKTARD", "BITCH",
               "Son of a Bitch", "Biatch", "BASTARD", "BALLS", "CUNT", "DICK", "DICKHEAD", "ASSHOLE", "ARSEHOLE",
               "COCK", "BLOW JOB", "HANDJOB", "BONER", "FELLATIO", "FELTCH", "HARD ON", "JIZZ", "RIMJOB", "CUNNILINGUS",
               "MASTURBATE", "ERECTION", "PUSSY", "WANKER", "JERK OFF", "JERKING", "WANKING", "SUCK",
               "SUCKER", "BASTARDS", "ASSHOLES", "BITCHES"]
}

def load_srt_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='ISO-8859-1') as file:
            content = file.read()
    return content.strip().split("\n\n")

def find_profanities_in_text(text, profanity_list):
    text = text.upper()
    for word in profanity_list:
        word = word.upper()
        if re.search(r'\b' + re.escape(word.rstrip('S')) + r'S?\b', text):
            return True
    return False

def parse_time_to_seconds(time_str):
    try:
        time_str = time_str.split(',')[0]
        h, m, s = map(int, time_str.split(':'))
        return h * 3600 + m * 60 + s
    except Exception:
        return None

def seconds_to_hhmmss(total_seconds):
    total_seconds = total_seconds % 86400
    h = int(total_seconds // 3600)
    m = int((total_seconds % 3600) // 60)
    s = int(total_seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def process_files(filepaths, classification, movie_start_str, output_widget):
    profanity_list = PROFANITY_LISTS.get(classification, [])
    output_widget.delete("1.0", "end")

    movie_start_seconds = parse_time_to_seconds(movie_start_str)
    if movie_start_seconds is None:
        messagebox.showerror("Invalid Time Format", "Please enter a valid movie starting time in HH:MM:SS format.")
        return

    for filepath in filepaths:
        filename = os.path.basename(filepath)
        output_widget.insert("end", f"Processing file: {filename}\n")
        blocks = load_srt_file(filepath)
        flagged_entries = []

        for block in blocks:
            lines = block.splitlines()
            if len(lines) >= 3:
                subtitle_text = " ".join(lines[2:])
                if find_profanities_in_text(subtitle_text, profanity_list):
                    time_line = lines[1]
                    parts = time_line.split(" --> ")
                    if len(parts) >= 1:
                        block_start = parts[0]
                        block_start_seconds = parse_time_to_seconds(block_start)
                        absolute_time_str = seconds_to_hhmmss(movie_start_seconds + block_start_seconds) if block_start_seconds is not None else "Unknown Time"
                    else:
                        absolute_time_str = "Unknown Time"
                    flagged_entries.append((block, absolute_time_str))
            else:
                if find_profanities_in_text(block, profanity_list):
                    flagged_entries.append((block, "Unknown Time"))

        if flagged_entries:
            output_widget.insert("end", f"Found profanities in {len(flagged_entries)} entries:\n\n")
            for idx, (entry, abs_time) in enumerate(flagged_entries, start=1):
                output_widget.insert("end", f"{idx}. At {abs_time}:{entry}\n{'-'*40}\n")
        else:
            output_widget.insert("end", "No profanities found.\n")
        output_widget.insert("end", "\n")

    messagebox.showinfo("Scan Complete", "The scan for profanities is complete.")

def select_files():
    filepaths = filedialog.askopenfilenames(filetypes=[("Subtitle files", "*.srt"), ("All files", "*.*")])
    if filepaths:
        files_var.set("; ".join(filepaths))
    return filepaths

def on_scan():
    file_list = files_var.get().split("; ")
    if not file_list or file_list == ['']:
        messagebox.showwarning("No Files Selected", "Please select one or more SRT files before scanning.")
        return
    classification = classification_var.get()
    movie_start = movie_time_var.get()
    process_files(file_list, classification, movie_start, output_text)

# Initialize UI
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("CleanSubs by github.com/zafriiii")
app.geometry("600x650")

frame = ctk.CTkFrame(app)
frame.pack(padx=10, pady=10, fill="x")

files_var = ctk.StringVar()
classification_var = ctk.StringVar(value="U")
movie_time_var = ctk.StringVar(value="00:00:00")

file_button = ctk.CTkButton(frame, text="Select SRT Files", command=select_files)
file_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

file_label = ctk.CTkLabel(frame, textvariable=files_var, width=600, anchor="w")
file_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")

class_label = ctk.CTkLabel(frame, text="Select Classification:")
class_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

class_dropdown = ctk.CTkOptionMenu(frame, variable=classification_var, values=["U", "P12 & 13", "16 & 18"])
class_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="w")

movie_label = ctk.CTkLabel(frame, text="Movie Starting Time (HH:MM:SS):")
movie_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

movie_entry = ctk.CTkEntry(frame, textvariable=movie_time_var, width=150)
movie_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

scan_button = ctk.CTkButton(frame, text="Scan", command=on_scan)
scan_button.grid(row=3, column=0, padx=5, pady=10, sticky="w")

output_text = ctk.CTkTextbox(app, wrap="word")
output_text.pack(padx=10, pady=10, fill="both", expand=True)

app.mainloop()
