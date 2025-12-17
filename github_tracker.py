import requests
import time
import os
from fpdf import FPDF
from dotenv import load_dotenv
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
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
def generate_pdf(username, user_data, repo_commit_data, latest_commit_overall):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "GitHub User Report", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, f"Username: {user_data['login']}", ln=True)
    pdf.cell(0, 8, f"Public Repositories: {user_data['public_repos']}", ln=True)
    pdf.cell(0, 8, f"Account Created On: {user_data['created_at']}", ln=True)
    pdf.ln(6)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Repository Commit Summary", ln=True)
    pdf.ln(3)
    pdf.set_font("Arial", size=11)
    for repo in repo_commit_data:
        pdf.multi_cell(
            0,
            8,
            f"Repository Name: {repo['name']}\n"
            f"Commit Count: {repo['commits']}\n"
            f"Last Commit Date: {repo['last_commit']}"
        )
        pdf.ln(3)
    pdf.ln(4)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, f"Last Commit Date (Overall): {latest_commit_overall}", ln=True)
    filename = f"{username}_github_report.pdf"
    pdf.output(filename)
    print(f"PDF generated successfully: {filename}")
def main():
    username = input("Enter GitHub username: ")
    user_data = get_user_details(username)
    if not user_data:
        return
    repos = get_repositories(username)
    repo_commit_data = []   # <-- NEW
    latest_commit_overall = None
    for repo in repos:
        repo_name = repo["name"]
        commit_count, last_commit_date = get_commit_summary(username, repo_name)
        repo_commit_data.append({
            "name": repo_name,
            "commits": commit_count,
            "last_commit": last_commit_date
        })
        if last_commit_date != "No commits":
            if (latest_commit_overall is None) or (last_commit_date > latest_commit_overall):
                latest_commit_overall = last_commit_date
        time.sleep(0.5)
    generate_pdf(username, user_data, repo_commit_data, latest_commit_overall)
if __name__ == "__main__":
    main()