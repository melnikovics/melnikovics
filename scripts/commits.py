import os
import requests
import json
from datetime import datetime, timezone, timedelta

# GitHub username and API endpoint
GITHUB_USERNAME = "melnikovics"
GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"
GITHUB_TOKEN_VAR = "GITHUB_TOKEN"

# Default success and error responses for the shields.io badge
# Color is blue for 0 commits, brightgreen for >0 commits
DEFAULT_SUCCESS_RESPONSE = {"schemaVersion": 1, "label": "Commits heute", "message": "0", "color": "blue"}
ERROR_RESPONSE = {"schemaVersion": 1, "label": "Commits heute", "message": "Error fetching", "color": "red"}

def get_todays_commit_count():
    """
    Fetches the number of commits made by the user today using GitHub GraphQL API.
    Returns a dictionary for shields.io badge.
    """
    github_token = os.getenv(GITHUB_TOKEN_VAR)

    if not github_token:
        print(f"Error: {GITHUB_TOKEN_VAR} environment variable not set.")
        return ERROR_RESPONSE

    # Get today's date range in UTC
    now_utc = datetime.now(timezone.utc)
    start_of_day_utc_str = now_utc.strftime("%Y-%m-%dT00:00:00Z")
    end_of_day_utc_str = now_utc.strftime("%Y-%m-%dT23:59:59Z") # Ensure full day coverage

    # GraphQL query
    query = f"""
    query {{
      user(login: "{GITHUB_USERNAME}") {{
        contributionsCollection(from: "{start_of_day_utc_str}", to: "{end_of_day_utc_str}") {{
          totalCommitContributions
        }}
      }}
    }}
    """

    headers = {
        "Authorization": f"Bearer {github_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(GITHUB_GRAPHQL_URL, headers=headers, json={"query": query}, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4XX or 5XX)
        
        data = response.json()

        if "errors" in data and data["errors"]:
            print(f"GraphQL API errors: {data['errors']}")
            return ERROR_RESPONSE

        commit_count = data.get("data", {}).get("user", {}).get("contributionsCollection", {}).get("totalCommitContributions")

        if commit_count is None:
            print("Could not find 'totalCommitContributions' in GraphQL response.")
            return ERROR_RESPONSE
        
        status_dict = DEFAULT_SUCCESS_RESPONSE.copy()
        status_dict["message"] = str(commit_count)
        if commit_count > 0:
            status_dict["color"] = "brightgreen"
        # If commit_count is 0, color remains "blue" as per DEFAULT_SUCCESS_RESPONSE
        
        return status_dict

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error fetching commit data: {e}. Response: {e.response.text if e.response else 'No response text'}")
        return ERROR_RESPONSE
    except requests.exceptions.RequestException as e:
        print(f"Error fetching commit data: {e}")
        return ERROR_RESPONSE
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response from GitHub API: {e}")
        return ERROR_RESPONSE
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return ERROR_RESPONSE

def main():
    """
    Main function to get commit count and write to file.
    """
    status_data = get_todays_commit_count()

    try:
        os.makedirs("data", exist_ok=True)
    except OSError as e:
        print(f"Error creating directory data/: {e}")
        # Let file writing attempt proceed and handle its own error

    try:
        with open("data/commits.json", "w") as f:
            json.dump(status_data, f, indent=4)
        print(f"Successfully wrote commit status to data/commits.json: {status_data.get('message', 'N/A')}")
    except IOError as e:
        print(f"Error writing status to data/commits.json: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while writing to file: {e}")

if __name__ == "__main__":
    main()
