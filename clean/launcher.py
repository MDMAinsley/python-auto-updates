import os
import subprocess
import sys

import requests


def get_latest_version(latest_version_url):
    response = requests.get(latest_version_url)
    response.raise_for_status()
    latest_release = response.json()
    return latest_release['tag_name']


def get_current_version(app_exe_path):
    result = subprocess.run([app_exe_path, "--version"], capture_output=True, text=True)
    return result.stdout.strip()


def check_for_update(current_version, latest_version_url):
    latest_version = get_latest_version(latest_version_url)
    return latest_version != current_version


def main():
    main_application_name = "application.exe"
    updater_application_name = "updater.exe"
    app_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    app_exe_path = os.path.join(app_dir, main_application_name)
    current_version = get_current_version(app_exe_path)
    owner = "username"
    repo = "repo_name"    
    latest_version_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    updater_path = os.path.join(app_dir, updater_application_name)

    try:
        if check_for_update(current_version, latest_version_url):
            print("Update available. Running updater...")
            subprocess.run([updater_path], check=True)
        else:
            print("No update available. Starting application...")
            subprocess.run([app_exe_path], check=True)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
