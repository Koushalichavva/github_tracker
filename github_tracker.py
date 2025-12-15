import requests

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
    print("Last Commit Date (overall):", latest_commit_overall)

if __name__ == "__main__":
    main()
