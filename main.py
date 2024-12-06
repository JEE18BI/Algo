import os
from sortedcontainers import SortedDict
import heapq

MAX_FOLDER_SIZE = 100

def convert_to_seconds(time_str):
    """Converts a time string (HH:MM:SS or MM:SS) to total seconds."""
    parts = list(map(int, time_str.split(":")))
    if len(parts) == 3:  # HH:MM:SS
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    elif len(parts) == 2:  # MM:SS
        return parts[0] * 60 + parts[1]
    else:
        raise ValueError("Invalid time format")

audios_map = {}
with open("Sample Tests/Sample 1/INPUT/AudiosInfo.txt", 'r') as file:
    for index, line in enumerate(file.readlines()):
        if index == 0:
            continue
        data = line.split(" ")
        time_in_seconds = convert_to_seconds(data[1].strip())
        audios_map[data[0]] = time_in_seconds

print(audios_map)

# worst fit linear

def worst_fit_linear():
    folders = {}
    for audio_name, audio_size in audios_map.items():
        if len(folders) == 0:
            folders[f"folder_{len(folders) + 1}"] = 0
        max_capacity = 0
        picked_folder = ""
        for folder_name, folder_size in folders.items():
            if folder_size + audio_size <= MAX_FOLDER_SIZE:
                if max_capacity < MAX_FOLDER_SIZE - folder_size:
                    max_capacity = MAX_FOLDER_SIZE - folder_size
                    picked_folder = folder_name
                    picked_folder_size = folder_size
        if max_capacity != 0:
                folders[picked_folder] = picked_folder_size + audio_size
        else:
            folders[f"folder_{len(folders) + 1}"] = audio_size
    print(folders)

print("wosrt fit linear")
worst_fit_linear()

# Worst fit using priority queue

def worst_fit_pq():
    pq = []
    folders = {}
    for audio_name, audio_size in audios_map.items():
        if pq and pq[0][0] + audio_size <= MAX_FOLDER_SIZE:
            folder_size, folder_name = heapq.heappop(pq)
            folders[folder_name] += audio_size
            heapq.heappush(pq, (folder_size + audio_size, folder_name))
        else:
            folder_name = f"folder_{len(folders) + 1}"
            folders[folder_name] = audio_size
            heapq.heappush(pq, (audio_size, folder_name))
    print(folders)


print("wosrt fit pq")
worst_fit_pq()


# worst fit decreasing linear

def worst_fit_Decreasing_linear ():
    folders = {}
    sorted_by_values_desc = dict(sorted(audios_map.items(), key=lambda item: item[1], reverse=True))
    for audio_name, audio_size in sorted_by_values_desc.items():
        if len(folders) == 0:
            folders[f"folder_{len(folders) + 1}"] = 0
        max_capacity = 0
        picked_folder = ""
        for folder_name, folder_size in folders.items():
            if folder_size + audio_size <= MAX_FOLDER_SIZE:
                if max_capacity < MAX_FOLDER_SIZE - folder_size:
                    max_capacity = MAX_FOLDER_SIZE - folder_size
                    picked_folder = folder_name
                    picked_folder_size = folder_size
        if max_capacity != 0:
                folders[picked_folder] = picked_folder_size + audio_size
        else:
            folders[f"folder_{len(folders) + 1}"] = audio_size
    print(folders)

print("wosrt fit decreasing linear")
worst_fit_Decreasing_linear()

# worst fit decreasing pq

def worst_fit_decreasing_pq():
    pq = []
    folders = {}
    sorted_by_values_desc = dict(sorted(audios_map.items(), key=lambda item: item[1], reverse=True))
    for audio_name, audio_size in sorted_by_values_desc.items():
        if pq and pq[0][0] + audio_size <= MAX_FOLDER_SIZE:
            folder_size, folder_name = heapq.heappop(pq)
            folders[folder_name] += audio_size
            heapq.heappush(pq, (folder_size + audio_size, folder_name))
        else:
            folder_name = f"folder_{len(folders) + 1}"
            folders[folder_name] = audio_size
            heapq.heappush(pq, (audio_size, folder_name))
    print(folders)

print("wosrt fit decreasing pq")
worst_fit_decreasing_pq()

#first Fit Decreasing Algorithm

def first_fit ():
    folders = {}
    sorted_by_values_desc = dict(sorted(audios_map.items(), key=lambda item: item[1], reverse=True))
    for audio_name, audio_size in sorted_by_values_desc.items():
        placed=False
        if len(folders) == 0:
            folders[f"folder_{len(folders) + 1}"] = 0
        for folder_name, folder_size in folders.items():
            if folder_size + audio_size <= MAX_FOLDER_SIZE:
                folders[folder_name] = folder_size + audio_size
                placed=True
                break
        if not placed:
            folders[f"folder_{len(folders) + 1}"] = audio_size
    print(folders)

print("first fit")
first_fit()


# best fit
def best_fit():
    folders = {}
    for audio_name, audio_size in audios_map.items():
        if len(folders) == 0:
            folders[f"folder_{len(folders) + 1}"] = 0
        min_capacity = 101
        picked_folder = ""
        for folder_name, folder_size in folders.items():
            if folder_size + audio_size <= MAX_FOLDER_SIZE:
                if min_capacity > MAX_FOLDER_SIZE - folder_size:
                    min_capacity = MAX_FOLDER_SIZE - folder_size
                    picked_folder = folder_name
                    picked_folder_size = folder_size
        if min_capacity != 101:
                folders[picked_folder] = picked_folder_size + audio_size
        else:
            folders[f"folder_{len(folders) + 1}"] = audio_size
    print(folders)

print("best fit")
best_fit()








