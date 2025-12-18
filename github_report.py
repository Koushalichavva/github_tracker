import requests
username = "Koushalichavva"   # Later you will take input from user
url = f"https://api.github.com/repos/Koushalichavva"
response = requests.get(url)
data = response.json()
print("Number of repositories:", len(data))
for repo in data:
    print(repo["name"])

#commits-url
import requests

username = "Koushalichavva"
repo_name = "gitbasics"
url = f"https://api.github.com/repos/{username}/{repo_name}/commits"

response = requests.get(url)
data = response.json()

print("Number of commits fetched in this page:", len(data))

for commit in data:
    print(commit["commit"]["message"])
import requests

username = "Koushalichavva"
repo_name = "gitbasics"

url = f"https://api.github.com/repos/{username}/{repo_name}/commits"

response = requests.get(url)
data = response.json()

# Latest commit is the first item in the list
latest_commit_date = data[0]["commit"]["author"]["date"]

print("Latest commit date:", latest_commit_date)
from fpdf import FPDF
import os
file_name = "github_report.pdf"
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(0, 10, "GitHub Activity Report", ln=True)
pdf.cell(0, 10, "Username: Koushalichavva", ln=True)
pdf.cell(0, 10, "Total Repositories: 5", ln=True)
pdf.cell(0, 10, "Last Commit Date: 2025-01-02", ln=True)
pdf.output(file_name)
os.startfile(file_name)
