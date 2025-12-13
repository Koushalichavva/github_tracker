import requests
def get_user_details(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    return response.json()
def main():
    username = input("Enter GitHub username: ")
    user_data = get_user_details(username)
    print("Username:", user_data["login"])
    print("Public Repositories:", user_data["public_repos"])
    print("Account Created On:", user_data["created_at"])
if __name__ == "__main__":
    main()
