import os
import shutil
import heapq
import time
import traceback
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

sys.setrecursionlimit(500000)


def convert_to_seconds(time_str):
    """Converts a time string (HH:MM:SS or MM:SS) to total seconds."""
    parts = list(map(int, time_str.split(":")))
    if len(parts) == 3:  # HH:MM:SS
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    elif len(parts) == 2:  # MM:SS
        return parts[0] * 60 + parts[1]
    else:
        raise ValueError("Invalid time format")
    
def format_duration(seconds, remove_leading_zeros=False):
    """
    Converts duration in seconds to H:M:S format, with optional removal of leading zeros.
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    if remove_leading_zeros:
        return f"{hours}:{minutes}:{seconds:02}"
    else:
        return f"{hours:02}:{minutes:02}:{seconds:02}"

def write_metadata(folders, path="Solution"):
    for folder_name, contents in folders.items():
        total_duration = sum(audio[1] for audio in contents)
        metadata_file_path = os.path.join(path, f"{folder_name}_METADATA.txt")

        # Write metadata for this folder
        with open(metadata_file_path, "w") as metadata_file:
            metadata_file.write(f"{folder_name}\n")  # Folder name
            for audio_name, audio_duration in contents:
                formatted_duration = format_duration(audio_duration, True)
                metadata_file.write(f"{audio_name} {formatted_duration}\n")
            # Total duration
            metadata_file.write(format_duration(total_duration) + "\n")

# worst fit linear

def worst_fit_linear(audios, path):
    folders = {}
    folder_contents = {} # To store the files in each folder -> for writing the metadata
    for audio in audios:
        audio_name = audio[0]
        audio_duration = audio[1]
        if len(folders) == 0:
            folder_name = f"F{len(folders) + 1}"
            folders[folder_name] = 0
            folder_contents[folder_name] = []
            os.mkdir(f'Solution/{folder_name}')
        max_capacity = -1
        picked_folder = ""
        for folder_name, total_folder_duration in folders.items():
            if total_folder_duration + audio_duration <= max_folder_duration: # Check if file can fit into the folder
                if max_capacity < max_folder_duration - total_folder_duration: # Check if the updated folder capacity is larger than the current max capacity
                    max_capacity = max_folder_duration - total_folder_duration
                    picked_folder = folder_name
        if max_capacity != -1: # Folder found
            folders[picked_folder] += audio_duration
            folder_contents[picked_folder].append((audio_name, audio_duration))
            shutil.copy(f"{path}/Audios/{audio_name}", f"Solution/{picked_folder}")
        else: # No folder found
            folder_name = f"F{len(folders) + 1}"
            folders[folder_name] = audio_duration
            folder_contents[folder_name] = [(audio_name, audio_duration)]
            os.mkdir(f'Solution/{folder_name}')
            shutil.copy(f"{path}/Audios/{audio_name}", f"Solution/{folder_name}")

    return folder_contents

# worst fit decreasing linear

def worst_fit_decreasing_linear(audios, path):
    sorted_audios = sorted(audios, key=lambda x: x[1], reverse=True)
    return worst_fit_linear(sorted_audios, path)

# Worst fit using priority queue

def worst_fit_pq(audios, path):
    pq = []
    folders = {}
    folder_contents = {} # To store the files in each folder -> for writing the metadata
    for audio in audios:
        audio_name = audio[0]
        audio_duration = audio[1]
        if pq and pq[0][0] + audio_duration <= max_folder_duration: # Check if pq not empty and the front have enough capacity for the audio
            total_folder_duration, folder_name = heapq.heappop(pq)
            folders[folder_name] += audio_duration
            heapq.heappush(pq, (total_folder_duration + audio_duration, folder_name))
            folder_contents[folder_name].append((audio_name, audio_duration))
        else: # No folders or no available capacity in the front folder
            folder_name = f"F{len(folders) + 1}"
            folders[folder_name] = audio_duration
            heapq.heappush(pq, (audio_duration, folder_name))
            folder_contents[folder_name] = [(audio_name, audio_duration)]
            os.mkdir(f"Solution/{folder_name}")
        shutil.copy(f"{path}/Audios/{audio_name}", f"Solution/{folder_name}")
    
    return folder_contents


# worst fit decreasing pq

def worst_fit_decreasing_pq(audios, path):
    sorted_audios = sorted(audios, key=lambda x: x[1], reverse=True)
    return worst_fit_pq(sorted_audios, path)


# first Fit Decreasing Algorithm

def first_fit (audios, path):
    folders = {}
    folder_contents = {}
    sorted_audios = sorted(audios, key=lambda x: x[1], reverse=True)
    for audio in sorted_audios:
        audio_name = audio[0]
        audio_duration = audio[1]
        placed = False
        if len(folders) == 0:
            folder_name = f"F{len(folders) + 1}"
            folders[folder_name] = 0
            folder_contents[folder_name] = []
            os.mkdir(f"Solution/{folder_name}")
        for folder_name, total_folder_duration in folders.items():
            if total_folder_duration + audio_duration <= max_folder_duration: # Check if the audio file can fit in the folder
                folders[folder_name] += audio_duration
                folder_contents[folder_name].append((audio_name, audio_duration))
                placed = True
                break
        if not placed:
            folder_name = f"F{len(folders) + 1}"
            folders[folder_name] = audio_duration
            folder_contents[folder_name] = [(audio_name, audio_duration)]
            os.mkdir(f"Solution/{folder_name}")
        shutil.copy(f"{path}/Audios/{audio_name}", f"Solution/{folder_name}")
    return folder_contents


# Folder filling

def folder_filling(audios, path):
    memo = {}
    decision = {}   # Dictionary for backtracking: Key -> tuple of remaining duration and num of files, Value -> taken or not
    def dp(remaining_duration, num_files):
        if (remaining_duration, num_files) in memo:
            return memo[(remaining_duration, num_files)]
        if remaining_duration == 0 or num_files == 0:
            return 0
        
        if audios[num_files - 1][1] > remaining_duration:
            result = dp(remaining_duration, num_files - 1)
            decision[(remaining_duration, num_files)] = False
        else:
            include_result = dp(remaining_duration - audios[num_files - 1][1], num_files - 1) + audios[num_files - 1][1]
            exclude_result = dp(remaining_duration, num_files - 1)
            if include_result >= exclude_result:
                result = include_result
                decision[(remaining_duration, num_files)] = True
            else:
                result = exclude_result
                decision[(remaining_duration, num_files)] = False
        memo[(remaining_duration, num_files)] = result
        return result

    def backtracking(remaining_duration, num_files):
        selected_files = []
        while remaining_duration > 0 and num_files > 0:
            if decision.get((remaining_duration, num_files)):
                selected_files.append(audios[num_files - 1])
                remaining_duration -= audios[num_files - 1][1]
            num_files -= 1
        return selected_files
    
    counter = 1
    folder_contents = {}
    while audios:
        folder_name = f"F{counter}"
        folder_contents[folder_name] = []
        os.mkdir(f"Solution/{folder_name}")
        dp(max_folder_duration, len(audios))
        selected_files = backtracking(max_folder_duration, len(audios))
        for file in selected_files:
            folder_contents[folder_name].append(file)
            shutil.copy(f"{path}/Audios/{file[0]}", f"Solution/{folder_name}")
            audios = [item for item in audios if item[0] != file[0]]
        counter += 1

    return folder_contents

# best fit

def best_fit(audios, path):
    folders = {}
    folder_contents = {}
    for audio in audios:
        audio_name = audio[0]
        audio_duration = audio[1]
        if len(folders) == 0:
            folder_name = f"F{len(folders) + 1}"
            folders[folder_name] = 0
            folder_contents[folder_name] = []
            os.mkdir(f"Solution/{folder_name}")
        min_capacity = max_folder_duration + 1
        picked_folder = ""
        for folder_name, total_folder_duration in folders.items():
            if total_folder_duration + audio_duration <= max_folder_duration: # Check if file can fit into the folder
                if min_capacity > max_folder_duration - total_folder_duration: # Check if the updated folder capacity is less than the current min capacity
                    min_capacity = max_folder_duration - total_folder_duration
                    picked_folder = folder_name
        if min_capacity != max_folder_duration + 1:
                folders[picked_folder] += audio_duration
                folder_contents[picked_folder].append((audio_name, audio_duration))
                shutil.copy(f"{path}/Audios/{audio_name}", f"Solution/{picked_folder}")
        else:
            folder_name = f"F{len(folders) + 1}"
            folders[folder_name] = audio_duration
            folder_contents[folder_name] = [(audio_name, audio_duration)]
            os.mkdir(f"Solution/{folder_name}")
            shutil.copy(f"{path}/Audios/{audio_name}", f"Solution/{folder_name}")
    return folder_contents

# best fit decreasing

def best_fit_decreasing(audios, path):
    sorted_audios = sorted(audios, key=lambda x: x[1], reverse=True)
    return best_fit(sorted_audios, path)

def execute_strategy(strategy, audios, path, max_folder_duration):
    start_time = time.time()

    if strategy == "Worst Fit Linear":
        folder_contents = worst_fit_linear(audios, path)
    elif strategy == "Worst Fit PQ":
        folder_contents = worst_fit_pq(audios, path)
    elif strategy == "Worst Fit Decreasing Linear":
        folder_contents = worst_fit_decreasing_linear(audios, path)
    elif strategy == "Worst Fit Decreasing PQ":
        folder_contents = worst_fit_decreasing_pq(audios, path)
    elif strategy == "First Fit Decreasing":
        folder_contents = first_fit(audios, path)
    elif strategy == "Folder Filling":
        folder_contents = folder_filling(audios, path)
    elif strategy == "Best Fit":
        folder_contents = best_fit(audios, path)
    elif strategy == "Best Fit Decreasing":
        folder_contents = best_fit_decreasing(audios, path)

    end_time = time.time()
    execution_time = end_time - start_time

    write_metadata(folder_contents)

    num_folders = len(os.listdir("Solution")) // 2 # To account for metadata files

    return execution_time, num_folders

def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_path_entry.delete(0, tk.END)
        folder_path_entry.insert(0, folder_path)

def reset():
    folder_path_entry.delete(0, tk.END)
    duration_entry.delete(0, tk.END)
    strategy_var.set(strategy_options[0])
    result_label.config(text="")

def submit():
    path = folder_path_entry.get()
    total_duration = duration_entry.get()
    selected_strategy = strategy_var.get()

    if not path or not total_duration or selected_strategy == strategy_options[0]:
        messagebox.showerror("Error", "Please fill in all fields and select a strategy.")
        return

    try:
        global max_folder_duration
        max_folder_duration = int(total_duration)
    except ValueError:
        messagebox.showerror("Error", "Total duration must be a valid number.")
        return

    try:
        audios = []
        audios_info_path = os.path.join(path, "AudiosInfo.txt")

        with open(audios_info_path, 'r') as file:
            for index, line in enumerate(file.readlines()):
                if index == 0:
                    continue
                data = line.split(" ")
                time_in_seconds = convert_to_seconds(data[1].strip())
                audios.append((data[0], time_in_seconds))

        os.mkdir("Solution")
        execution_time, num_folders = execute_strategy(selected_strategy, audios, path, max_folder_duration)

        result_label.config(text=f"Execution Time: {execution_time} seconds\nNumber of Folders Created: {num_folders}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

    finally:
        if os.path.exists("Solution"):
            shutil.rmtree("Solution")
            messagebox.showinfo("Waiting", "Please wait while the Solution folder is being deleted...")
            while os.path.exists("Solution"):
                time.sleep(1)
            messagebox.showinfo("Notification", "Solution folder has been successfully deleted.")

# Main GUI setup
root = tk.Tk()
root.title("Audio File Manager")

folder_path_label = tk.Label(root, text="Folder Path:")
folder_path_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")

folder_path_entry = tk.Entry(root, width=50)
folder_path_entry.grid(row=0, column=1, padx=10, pady=5)

browse_button = tk.Button(root, text="Browse", command=browse_folder)
browse_button.grid(row=0, column=2, padx=10, pady=5)

duration_label = tk.Label(root, text="Total Duration (seconds):")
duration_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")

duration_entry = tk.Entry(root, width=50)
duration_entry.grid(row=1, column=1, padx=10, pady=5)

strategy_label = tk.Label(root, text="Strategy:")
strategy_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")

strategy_options = [
    "Select Strategy",
    "Worst Fit Linear",
    "Worst Fit PQ",
    "Worst Fit Decreasing Linear",
    "Worst Fit Decreasing PQ",
    "First Fit Decreasing",
    "Folder Filling",
    "Best Fit",
    "Best Fit Decreasing"
]

strategy_var = tk.StringVar(value=strategy_options[0])
strategy_menu = tk.OptionMenu(root, strategy_var, *strategy_options)
strategy_menu.grid(row=2, column=1, padx=10, pady=5, sticky="w")

submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.grid(row=3, column=0, padx=10, pady=10)

reset_button = tk.Button(root, text="Reset", command=reset)
reset_button.grid(row=3, column=2, padx=10, pady=10)

result_label = tk.Label(root, text="", fg="blue", font=("Arial", 12))
result_label.grid(row=4, column=0, columnspan=3, pady=10)


root.mainloop() 
