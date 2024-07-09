import requests

# Your current program version
programVersion = "1.0.0"

# GitHub repository details
owner = "MDMAinsley"
repo = "python-auto-updates"

# URL to fetch the latest release version from GitHub API
url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"

try:
    # Fetch the latest release version
    response = requests.get(url)
    response.raise_for_status()
    latest_release = response.json()
    latestReleaseVersion = latest_release['tag_name']

    # Compare the versions
    if latestReleaseVersion == programVersion:
        print("App is up to date!")
    else:
        print(f"A new version is available: {latestReleaseVersion}")

except requests.exceptions.RequestException as e:
    print(f"Error fetching latest release version: {e}")
except KeyError:
    print("Error: Unexpected response structure from GitHub API")
