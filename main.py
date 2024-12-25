import os
import shutil
import heapq
import time


def convert_to_seconds(time_str):
    """Converts a time string (HH:MM:SS or MM:SS) to total seconds."""
    parts = list(map(int, time_str.split(":")))
    if len(parts) == 3:  # HH:MM:SS
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    elif len(parts) == 2:  # MM:SS
        return parts[0] * 60 + parts[1]
    else:
        raise ValueError("Invalid time format")

# worst fit linear

def worst_fit_linear(audios, path):
    folders = {}
    for audio in audios:
        audio_name = audio[0]
        audio_size = audio[1]
        if len(folders) == 0:
            folder_name = f"F{len(folders) + 1}"
            folders[folder_name] = 0
            os.mkdir(f'Solution/{folder_name}')
        max_capacity = 0
        picked_folder = ""
        for folder_name, folder_size in folders.items():
            if folder_size + audio_size <= max_folder_duration:
                if max_capacity < max_folder_duration - folder_size:
                    max_capacity = max_folder_duration - folder_size
                    picked_folder = folder_name
        if max_capacity != 0:
            folders[picked_folder] += audio_size
            shutil.copy(f"{path}/Audios/{audio_name}", f"Solution/{picked_folder}")
        else:
            folder_name = f"F{len(folders) + 1}"
            folders[folder_name] = audio_size
            os.mkdir(f'Solution/{folder_name}')
            shutil.copy(f"{path}/Audios/{audio_name}", f"Solution/{folder_name}")


# Worst fit using priority queue

def worst_fit_pq(audios, path):
    pq = []
    folders = {}
    for audio in audios:
        audio_name = audio[0]
        audio_size = audio[1]
        if pq and pq[0][0] + audio_size <= max_folder_duration:
            folder_size, folder_name = heapq.heappop(pq)
            folders[folder_name] += audio_size
            heapq.heappush(pq, (folder_size + audio_size, folder_name))
        else:
            folder_name = f"F{len(folders) + 1}"
            folders[folder_name] = audio_size
            heapq.heappush(pq, (audio_size, folder_name))
            os.mkdir(f"Solution/{folder_name}")
        shutil.copy(f"{path}/Audios/{audio_name}", f"Solution/{folder_name}")


# worst fit decreasing linear

def worst_fit_decreasing_linear(audios, path):
    sorted_audios = sorted(audios, key=lambda x: x[1], reverse=True)
    worst_fit_linear(sorted_audios, path)


# worst fit decreasing pq

def worst_fit_decreasing_pq(audios, path):
    sorted_audios = sorted(audios, key=lambda x: x[1], reverse=True)
    worst_fit_pq(sorted_audios, path)

# first Fit Decreasing Algorithm

def first_fit (audios, path):
    folders = {}
    sorted_audios = sorted(audios, key=lambda x: x[1], reverse=True)
    for audio in sorted_audios:
        audio_name = audio[0]
        audio_size = audio[1]
        placed=False
        if len(folders) == 0:
            folder_name = f"F{len(folders) + 1}"
            folders[folder_name] = 0
            os.mkdir(f"Solution/{folder_name}")
        for folder_name, folder_size in folders.items():
            if folder_size + audio_size <= max_folder_duration:
                folders[folder_name] += audio_size
                placed=True
                break
        if not placed:
            folder_name = f"F{len(folders) + 1}"
            folders[folder_name] = audio_size
            os.mkdir(f"Solution/{folder_name}")
        shutil.copy(f"{path}/Audios/{audio_name}", f"Solution/{folder_name}")

# Folder filling

def folder_filling(audios, path):
    memo = {}
    decision = {}
    def dp(capacity, num_files):
        if (capacity, num_files) in memo:
            return memo[(capacity, num_files)]
        if capacity == 0 or num_files == 0:
            return 0
        
        if audios[num_files - 1][1] > capacity:
            result = dp(capacity, num_files - 1)
            decision[(capacity, num_files)] = False
        else:
            include_result = dp(capacity - audios[num_files - 1][1], num_files - 1) + audios[num_files - 1][1]
            exclude_result = dp(capacity, num_files - 1)
            if include_result >= exclude_result:
                result = include_result
                decision[(capacity, num_files)] = True
            else:
                result = exclude_result
                decision[(capacity, num_files)] = False
        memo[(capacity, num_files)] = result
        return result

    def backtracking(capacity, num_files):
        selected_files = []
        while capacity > 0 and num_files > 0:
            if decision.get((capacity, num_files)):
                selected_files.append(audios[num_files - 1])
                capacity -= audios[num_files - 1][1]
            num_files -= 1
        return selected_files
    
    while audios:
        counter = 1
        folder_name = f"F{counter}"
        os.mkdir(f"Solution/{folder_name}")
        dp(max_folder_duration, len(audios))
        selected_files = backtracking(max_folder_duration, len(audios))
        for file in selected_files:
            shutil.copy(f"{path}/Audios/{file[0]}", f"Solution/{folder_name}")
            audios = [item for item in audios if item[0] != file[1]]
        counter += 1

# best fit

def best_fit(audios, path):
    folders = {}
    for audio in audios:
        audio_name = audio[0]
        audio_size = audio[1]
        if len(folders) == 0:
            folder_name = f"F{len(folders) + 1}"
            folders[folder_name] = 0
            os.mkdir(f"Solution/{folder_name}")
        min_capacity = max_folder_duration + 1
        picked_folder = ""
        for folder_name, folder_size in folders.items():
            if folder_size + audio_size <= max_folder_duration:
                if min_capacity > max_folder_duration - folder_size:
                    min_capacity = max_folder_duration - folder_size
                    picked_folder = folder_name
        if min_capacity != max_folder_duration + 1:
                folders[picked_folder] += audio_size
                shutil.copy(f"{path}/Audios/{audio_name}", f"Solution/{picked_folder}")
        else:
            folder_name = f"F{len(folders) + 1}"
            folders[folder_name] = audio_size
            os.mkdir(f"Solution/{folder_name}")
            shutil.copy(f"{path}/Audios/{audio_name}", f"Solution/{folder_name}")

# best fit decreasing

def best_fit_decreasing(audios, path):
    sorted_audios = sorted(audios, key=lambda x: x[1], reverse=True)
    best_fit(sorted_audios, path)

if __name__ == "__main__":
        try:
            while True:
                path =  input("Enter directory path for audios and metadata: ").strip()
                max_folder_duration = int(input("Enter max folder size: "))
                audios = []

                audios_info_path = os.path.join(path, "AudiosInfo.txt")   
                with open(audios_info_path, 'r') as file:
                    for index, line in enumerate(file.readlines()):
                        if index == 0:
                            continue
                        data = line.split(" ")
                        time_in_seconds = convert_to_seconds(data[1].strip())
                        audios.append((data[0], time_in_seconds))
                strategy = int(input("Please select strategy\n1. Worst fit linear\n2. Worst fit pq\n3. Worst fit decreasing linear\n4. Worst fit decreasing pq\n5. First fit decreasing\n6. Folder filling\n7. Best fit\n8. Best fit decreasing\n"))
                os.mkdir("Solution")

                start_time = time.time()

                if strategy == 1:
                    worst_fit_linear(audios, path)
                elif strategy == 2:
                    worst_fit_pq(audios, path)
                elif strategy == 3:
                    worst_fit_decreasing_linear(audios, path)
                elif strategy == 4:
                    worst_fit_decreasing_pq(audios, path)
                elif strategy == 5:
                    first_fit(audios, path)
                elif strategy == 6:
                    folder_filling(audios, path)
                elif strategy == 7:
                    best_fit(audios, path)
                elif strategy == 8:
                    best_fit_decreasing(audios, path)

                end_time = time.time()
                execution_time = end_time - start_time
                print(f"Execution time: {execution_time}")

                if input("Do you want to exit? (y/n): ") == 'y':
                    exit(0)
                else:
                    shutil.rmtree("Solution")
        except Exception as e:
            print(e)
        finally:
            shutil.rmtree("Solution")