import tkinter as tk
from tkinter import filedialog, ttk, messagebox, scrolledtext
import os
import re
import tkinter.font as tkFont

# NOTE: This application does not open any network ports or initiate network connections.
# As a local scanning tool, it should pass Windows Firewall without requiring any special exceptions.
# For enhanced trust and fewer security warnings, please consider digitally signing your executable.

# Enable High DPI Awareness on Windows 10/11
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except Exception as e:
    print("High DPI awareness could not be set:", e)

# Updated profanity lists based on your provided words.
PROFANITY_LISTS = {
    "U": [
        "MOTHERFUCKER", "FATHERFUCKER", "FUCK", "FUCKED", "FUCKER", "FUCKING", "FUCKTARD", "BITCH",
        "Son of a Bitch", "Biatch", "BASTARD", "BALLS", "CUNT", "DICK", "DICKHEAD", "ASSHOLE", "ARSEHOLE",
        "COCK", "BLOW JOB", "HANDJOB", "BONER", "FELLATIO", "FELTCH", "HARD ON", "JIZZ", "RIMJOB", "CUNNILINGUS",
        "MASTURBATE", "ERECTION", "CAMELTOE", "PUSSY", "SLUT", "HOE", "WHORE", "BUTTHOLE", "SHITHOLE", "CRAPHOLE",
        "SUCK", "BALLOCKS", "NUTS", "NUTSACK", "BEANBAG", "TITS", "BOOBS", "PENIS", "VAGINA", "TESTICLE",
        "SCROTUM", "BREAST", "BUTTOCKS", "BUM", "SUCKER", "BASTARDS", "ASSHOLES", "BITCHES"
    ],
    "P12 & 13": [
        "MOTHERFUCKER", "FATHERFUCKER", "FUCK", "FUCKED", "FUCKER", "FUCKING", "FUCKTARD", "BITCH",
        "Son of a Bitch", "Biatch", "BASTARD", "BALLS", "CUNT", "DICK", "DICKHEAD", "ASSHOLE", "ARSEHOLE",
        "COCK", "BLOW JOB", "HANDJOB", "BONER", "FELLATIO", "FELTCH", "HARD ON", "JIZZ", "RIMJOB", "CUNNILINGUS",
        "MASTURBATE", "ERECTION", "CAMELTOE", "PUSSY", "WANKER", "JERK OFF", "JERKING", "WANKING", "SUCK", "SUCKER", "BASTARDS", "ASSHOLES", "BITCHES"
    ],
    "16 & 18": [
        "MOTHERFUCKER", "FATHERFUCKER", "FUCK", "FUCKED", "FUCKER", "FUCKING", "FUCKTARD", "BITCH",
        "Son of a Bitch", "Biatch", "BASTARD", "BALLS", "CUNT", "DICK", "DICKHEAD", "ASSHOLE", "ARSEHOLE",
        "COCK", "BLOW JOB", "HANDJOB", "BONER", "FELLATIO", "FELTCH", "HARD ON", "JIZZ", "RIMJOB", "CUNNILINGUS",
        "MASTURBATE", "ERECTION", "PUSSY", "WANKER", "JERK OFF", "JERKING", "WANKING", "SUCK", "SUCKER", "BASTARDS", "ASSHOLES", "BITCHES"
    ]
}

def load_srt_file(filepath):
    """Load the SRT file and return a list of subtitle blocks."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='ISO-8859-1') as file:
            content = file.read()
    # Split by double newlines as a basic segmentation of SRT blocks.
    blocks = content.strip().split("\n\n")
    return blocks


def find_profanities_in_text(text, profanity_list):
    """Return True if any base form or variation of profanity word is found in the text."""
    text = text.upper()  # Case-insensitive
    for word in profanity_list:
        word = word.upper()
        # Match singular/plural or slight variations
        if re.search(r'\b' + re.escape(word.rstrip('S')) + r'S?\b', text):
            return True
    return False

    """Return True if any profanity word is found in the text."""
    for word in profanity_list:
        pattern = r'\b' + re.escape(word) + r'\b'
        if re.search(pattern, text, flags=re.IGNORECASE):
            return True
    return False

def parse_time_to_seconds(time_str):
    """
    Convert a time string in the format HH:MM:SS or HH:MM:SS,mmm to seconds.
    """
    try:
        # Remove milliseconds if present.
        time_str = time_str.split(',')[0]
        h, m, s = map(int, time_str.split(':'))
        return h * 3600 + m * 60 + s
    except Exception:
        return None

def seconds_to_hhmmss(total_seconds):
    """Convert seconds into a HH:MM:SS formatted string in 24-hour format.
    
    This function applies modulo 86400 (24 hours) to ensure times wrap around.
    """
    total_seconds = total_seconds % 86400  # Wrap around after 24 hours.
    h = int(total_seconds // 3600)
    m = int((total_seconds % 3600) // 60)
    s = int(total_seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def process_files(filepaths, classification, movie_start_str, output_text_widget):
    """Scan each SRT file for profanities and display the results along with adjusted times."""
    profanity_list = PROFANITY_LISTS.get(classification, [])
    output_text_widget.delete(1.0, tk.END)  # Clear previous output

    # Parse the movie starting time provided by the user.
    movie_start_seconds = parse_time_to_seconds(movie_start_str)
    if movie_start_seconds is None:
        messagebox.showerror("Invalid Time Format", "Please enter a valid movie starting time in HH:MM:SS format.")
        return

    for filepath in filepaths:
        filename = os.path.basename(filepath)
        output_text_widget.insert(tk.END, f"Processing file: {filename}\n")
        blocks = load_srt_file(filepath)
        flagged_entries = []

        for block in blocks:
            lines = block.splitlines()
            if len(lines) >= 3:
                subtitle_text = " ".join(lines[2:])
                if find_profanities_in_text(subtitle_text, profanity_list):
                    # Extract the timestamp from the second line.
                    time_line = lines[1]
                    # Expecting format: "HH:MM:SS,mmm --> HH:MM:SS,mmm"
                    parts = time_line.split(" --> ")
                    if len(parts) >= 1:
                        block_start = parts[0]
                        block_start_seconds = parse_time_to_seconds(block_start)
                        if block_start_seconds is not None:
                            # Calculate the absolute time when the profanity appears.
                            absolute_seconds = movie_start_seconds + block_start_seconds
                            absolute_time_str = seconds_to_hhmmss(absolute_seconds)
                        else:
                            absolute_time_str = "Unknown Time"
                    else:
                        absolute_time_str = "Unknown Time"
                    flagged_entries.append((block, absolute_time_str))
            else:
                if find_profanities_in_text(block, profanity_list):
                    flagged_entries.append((block, "Unknown Time"))

        if flagged_entries:
            output_text_widget.insert(tk.END, f"Found profanities in {len(flagged_entries)} entries:\n\n")
            for idx, (entry, abs_time) in enumerate(flagged_entries, start=1):
                # Insert the numbering and time label in bold using the "bold" tag.
                time_label = f"{idx}. At {abs_time}:\n"
                output_text_widget.insert(tk.END, time_label, "bold")
                output_text_widget.insert(tk.END, f"{entry}\n{'-'*40}\n")
        else:
            output_text_widget.insert(tk.END, "No profanities found.\n")
        output_text_widget.insert(tk.END, "\n")

    messagebox.showinfo("Scan Complete", "The scan for profanities is complete.")

def select_files():
    """Open a file dialog to select one or more .srt files."""
    filepaths = filedialog.askopenfilenames(
        title="Select SRT files",
        filetypes=[("Subtitle files", "*.srt"), ("All files", "*.*")]
    )
    if filepaths:
        files_var.set("; ".join(filepaths))
    return filepaths

def on_scan():
    """Triggered when the Scan button is clicked."""
    file_list = files_var.get().split("; ")
    if not file_list or file_list == ['']:
        messagebox.showwarning("No Files Selected", "Please select one or more SRT files before scanning.")
        return
    classification = classification_var.get()
    movie_start = movie_time_var.get()
    process_files(file_list, classification, movie_start, output_text)

# Set up the main Tkinter window.
root = tk.Tk()
root.title("CleanSubs by github.com/zafriiii")
root.geometry("1000x700")

# Define a clean, modern font for high-DPI clarity.
default_font = tkFont.Font(family="Segoe UI", size=10)
root.option_add("*Font", default_font)

# Top frame for file selection, classification, movie start time and scan button.
top_frame = ttk.Frame(root, padding="10")
top_frame.pack(side=tk.TOP, fill=tk.X)

# Row 0: Button to select SRT files.
files_var = tk.StringVar()
select_btn = ttk.Button(top_frame, text="Select SRT Files", command=select_files)
select_btn.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

# Row 0: Label to show selected files.
files_label = ttk.Label(top_frame, textvariable=files_var, wraplength=600)
files_label.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

# Row 1: Classification dropdown label.
classification_label = ttk.Label(top_frame, text="Select Classification:")
classification_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

# Row 1: Dropdown for selecting the classification.
classification_var = tk.StringVar(value="U")
classification_dropdown = ttk.Combobox(top_frame, textvariable=classification_var, state="readonly")
classification_dropdown['values'] = ("U", "P12 & 13", "16 & 18")
classification_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

# Row 2: Input field for movie starting time.
movie_time_label = ttk.Label(top_frame, text="Movie Starting Time (HH:MM:SS):")
movie_time_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
movie_time_var = tk.StringVar(value="00:00:00")  # Default value
movie_time_entry = ttk.Entry(top_frame, textvariable=movie_time_var, width=15)
movie_time_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

# Row 3: Dedicated Scan button placed below movie start time.
scan_btn = ttk.Button(top_frame, text="Scan", command=on_scan)
scan_btn.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)

# ScrolledText widget to display the scan results.
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=30)
output_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
# Configure a "bold" tag for the text widget.
output_text.tag_configure("bold", font=(default_font.actual("family"), default_font.actual("size"), "bold"))

# Start the Tkinter event loop.
root.mainloop()
