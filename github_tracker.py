import requests
<<<<<<< HEAD

def get_user_details(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    return response.json()

def get_repositories(username):
    url = f"https://api.github.com/users/{username}/repos?sort=created&direction=asc"
    response = requests.get(url)
    return response.json()

def get_commit_summary(username, repo_name):
    url = f"https://api.github.com/repos/{username}/{repo_name}/commits"
    response = requests.get(url)
    commits = response.json()

    if isinstance(commits, list) and len(commits) > 0:
        commit_count = len(commits)
        last_commit_date = commits[0]["commit"]["author"]["date"]  # latest in this repo
    else:
        commit_count = 0
        last_commit_date = "No commits"

    return commit_count, last_commit_date
=======
import time
import os
from dotenv import load_dotenv
load_dotenv()   # loads variables from .env into environment
GITHUB_TOKEN = os.getenv("MY_GITHUB_TOKEN")
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}"
}

def get_user_details(username):
    url = f"https://api.github.com/users/{username}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Failed to fetch user details:", e)
        return None

def get_repositories(username):
    url = f"https://api.github.com/users/{username}/repos?sort=created&direction=asc"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status() #checks for HTTP errors (like 401, 404, 500).
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Failed to fetch repositories:", e)
        return []

def get_commit_summary(username, repo_name):
    url = f"https://api.github.com/repos/{username}/{repo_name}/commits?per_page=100&page=1"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        commits = response.json()
        if commits:
            commit_count = len(commits)  # usually 1 here due to per_page=1
            last_commit_date = commits[0]["commit"]["author"]["date"]
        else:
            commit_count = 0
            last_commit_date = "No commits"
        return commit_count, last_commit_date
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch commits for {repo_name}:", e)
        return 0, "No commits"
>>>>>>> adc7964 (new token added)

def main():
    username = input("Enter GitHub username: ")
    user_data = get_user_details(username)
    print("Username:", user_data["login"])
    print("Public Repositories:", user_data["public_repos"])
    print("Account Created On:", user_data["created_at"])
    repos = get_repositories(username)
    print("Total Repositories:", len(repos))
    latest_commit_overall = None
    for repo in repos:
        key = repo["name"]
        commit_count, last_commit_date = get_commit_summary(username, key)
        print(key)
        print(f"Number of Commits: {commit_count}")
        if last_commit_date != "No commits":
            if (latest_commit_overall is None) or (last_commit_date > latest_commit_overall):
                latest_commit_overall = last_commit_date
<<<<<<< HEAD
=======
        time.sleep(0.5)
>>>>>>> adc7964 (new token added)
    print("Last Commit Date (overall):", latest_commit_overall)

if __name__ == "__main__":
    main()
