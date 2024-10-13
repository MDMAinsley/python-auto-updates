import os
import shutil
import subprocess
import sys
import time

# Variable Declaration
application_name = "Main Application Name"
launcher_name = "Launcher Application Name"
background_name = "Background Application Name"


# Function to check if a file can be accessed (not in use)
def can_access_file(file_path):
    try:
        with open(file_path, 'rb'):
            return True
    except PermissionError as e:
        if e.winerror == 32:  # File is in use
            return False
        raise  # Rethrow other permission errors


# Function to replace the outdated files
def replace_files(extract_folder, app_dir):
    max_retries = 5
    retry_delay = 5  # seconds
    max_secondary_retries = 2  # Retry the whole process twice if initial attempts fail
    secondary_retry_delay = 30  # Long delay between secondary retries in seconds

    new_launcher_path = os.path.join(extract_folder, launcher_name)
    new_data_path = os.path.join(extract_folder, application_name)
    new_background_path = os.path.join(extract_folder, background_name)

    current_launcher_path = os.path.join(app_dir, launcher_name)
    current_data_path = os.path.join(app_dir, application_name)
    current_background_path = os.path.join(app_dir, background_name)

    # Create a list of files to move
    files_to_move = [
        (new_launcher_path, current_launcher_path),
        (new_data_path, current_data_path),
        (new_background_path, current_background_path)
    ]

    for secondary_attempt in range(max_secondary_retries):
        for attempt in range(max_retries):
            all_files_ready = True  # Reset before each retry
            for new_path, current_path in files_to_move:
                if os.path.exists(new_path):
                    if not can_access_file(new_path) or not can_access_file(current_path):
                        all_files_ready = False  # Mark that a file is in use
                        print(
                            f"File in use: {new_path} or {current_path},"
                            f" waiting and retrying... ({attempt + 1}/{max_retries})")
                        time.sleep(retry_delay * (attempt + 1))  # Exponential backoff
                        break  # Exit inner loop to retry all files
                else:
                    print(f"File does not exist: {new_path}")
                    all_files_ready = False

            if all_files_ready:
                # All files are ready to be moved
                for new_path, current_path in files_to_move:
                    shutil.move(new_path, current_path)
                return  # Exit after moving files successfully

        # Long delay before secondary retry block
        print(f"Retrying after {secondary_retry_delay} seconds...")
        time.sleep(secondary_retry_delay)

    # After retrying max_secondary_retries times, give up and inform the launcher
    print("Error: Wait for syncing to finish and try updating again later.")
    sys.exit(2)  # Non-zero exit code to signal failure


# Function to remove the update zip and temp folder
def cleanup(extract_folder, zip_file):
    try:
        # Delete the extracted folder and zip file
        if os.path.exists(extract_folder):
            shutil.rmtree(extract_folder)
            # print(f"UPDATER: Deleted extracted folder {extract_folder}.")
        if os.path.exists(zip_file):
            os.remove(zip_file)
    except Exception as e:
        print(f"Error during update cleanup: {e}")


# Function to clear the console on any os
def clear_console():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For Linux/macOS
    else:
        os.system('clear')


# Main Function
def main():
    app_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    extract_folder = sys.argv[1]  # Passed from Launcher
    zip_file = os.path.join(app_dir, os.path.basename(extract_folder).replace("update_", "v") + ".zip")

    max_retries = 5
    retry_delay = 5  # seconds
    max_secondary_retries = 2  # Retry the whole process twice if initial attempts fail
    secondary_retry_delay = 30  # Long delay between secondary retries in seconds

    try:
        for secondary_attempt in range(max_secondary_retries):
            for attempt in range(max_retries):
                try:
                    # Replace launcher and data files
                    replace_files(extract_folder, app_dir)

                    # Clean up the update folder and zip file
                    cleanup(extract_folder, zip_file)

                    # Restart the updated application
                    new_launcher_path = os.path.join(app_dir, launcher_name)
                    subprocess.Popen([new_launcher_path])

                    print("Updated successfully.")
                    time.sleep(1)
                    clear_console()
                    sys.exit(0)  # Exit updater after successful update

                except PermissionError as e:
                    if e.winerror == 32:  # WinErr32: File in use or syncing
                        print(f"Possible OneDrive/Cloud Service sync in progress,"
                              f" waiting and retrying... ({attempt + 1}/{max_retries})")
                        time.sleep(retry_delay * (attempt + 1))  # Exponential backoff
                    else:
                        raise  # Rethrow other permission errors

            # Long delay before secondary retry block
            print(f"Retrying entire update process after {secondary_retry_delay} seconds...")
            time.sleep(secondary_retry_delay)

        # After retrying max_secondary_retries times, give up and inform the launcher
        print("Error: Wait for syncing to finish and try updating again later.")
        sys.exit(2)  # Non-zero exit code to signal failure

    except Exception as e:
        print(f"Error during update: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
