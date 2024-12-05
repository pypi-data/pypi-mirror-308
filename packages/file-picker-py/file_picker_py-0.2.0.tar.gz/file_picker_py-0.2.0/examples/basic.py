from file_picker_py import (
    pick_file_blocking,
    pick_files_blocking,
    pick_folder_blocking,
    pick_folders_blocking,
    pick_save_file_blocking
)

# Pick a single file
file_path = pick_file_blocking()
if file_path:
    print(f"Selected file: {file_path}")

# Pick multiple files
file_paths = pick_files_blocking()
for path in file_paths:
    print(f"Selected file: {path}")

# Pick a single folder
folder_path = pick_folder_blocking()
if folder_path:
    print(f"Selected folder: {folder_path}")

# Pick multiple folders
folder_paths = pick_folders_blocking()
for path in folder_paths:
    print(f"Selected folder: {path}")

# Pick a save file location
save_path = pick_save_file_blocking()
if save_path:
    print(f"Save location: {save_path}")