The best way to interact with GitHub API.

> **Note:** _This module is useful for the GitHub API_ <br>
> Your URL should look like this https://api.github.com
> This is working module with your PAT Token


# Prerequisites
```python
from github_module import GitHubHelper
```

# Getting Started

## Connectivity to GitHub

To initialize a connection to GitHub, instantiate the `GitHubHelper` class with your GitHub URL, ORG, and Personal API Token:

```python
github_helper = GitHubHelper(GITHUB_API, API_TOKEN)
```
______________________________________________________________________________
______________________________________________________________________________
# 1. Get the Current PAT API Rate Limit
- Purpose:
  - Fetches the current rate limit from the GitHub API. 
- Parameters:
  - None (The method relies on the instance's github_api and headers)
- Output:
  - The number of remaining API requests allowed before hitting the rate limit. 
- Return:
  - `int`: The remaining rate limit. 
  - `-1`: If there was an error retrieving the rate limit.
```python
remaining_requests = github_helper.get_rate_limit()
print(f"Remaining rate limit: {remaining_requests}")
```

# 2. Check if the Repository exist
- Purpose:
  - Checks if a GitHub repository exists and handles various error scenarios.
- Parameters:
  - `owner` (str): The username or organization that owns the repository.
  - `repo` (str): The name of the repository. 
- Output:
  - A dictionary with the status of the repository check. 
- Return:
  - `dict`:
    - `"status"` (str): Indicates the result of the check. Possible values are "exists", "not_found", "forbidden", "rate_limit_exceeded", and "error".
    - `"message"` (str): A message providing details about the result.
```python
result = github_helper.check_repository(owner="octocat", repo="Hello-World")
print(result["status"])  # e.g., "exists"
print(result["message"])  # e.g., "Repository exists."
```

# 3. Check if the Repository Read-Only
- Purpose:
  - Determines whether a GitHub repository is read-only for the authenticated user. 
- Parameters:
  - `owner` (str): The username or organization that owns the repository. 
  - `repo` (str): The name of the repository.
- Output:
  - A boolean indicating whether the repository is read-only.
- Return:
  - `True`: If the repository is read-only. 
  - `False`: If the repository is writable. 
  - `None`: If there was an error checking the repository (e.g., rate limit too low, repository not found).

# 4. Get the number of days that PAT is about to expire
- Purpose:
  - Determines the number of days that PAT is about to expire
- Parameters:
  - `PAT` (str): The PAT token to check expiry.
- Output:
  - The number of remaining days of PAT token. 
- Return:
  - `int`: The remaining number of days.
  - `-1`: If there is no expiry of the PAT token.
  - `-2`: If there was an error retrieving the number of days.

```python
expiry_days = github_helper.get_token_expiry_days()
print(expiry_days)
if expiry_days >= 0:
    print(f"Token expires in {expiry_days} days.")
elif expiry_days == -1:
    print("Token has no expiration (infinite).")
else:
    print("An error occurred while checking the token expiration.")
```
______________________________________________________________________________
______________________________________________________________________________
# Data Privacy Note

🔒 **We respect your privacy**: This module does **not** store any of your data anywhere. It simply interacts with the GitHub API to perform the requested operations. Ensure you manage your connection details securely.

# Release Notes

- Renaming github_module to github_modules

## Old Releases

### Latest Release 0.4.1 (21 Aug 2024)
- Changing README.md structure for Release Notes
- Updated `get_token_expiry_days` use case code in README.md

### Latest Release: 0.4 (21 Aug 2024)
- We’ve implemented the `get_token_expiry_days` function to determine the number of days remaining on the PAT token. Occasionally, our automation fails due to the use of PATs with limited expiry. To prevent this, we’ve added a check to ensure the token’s validity. 

### Latest Release: 0.3 (05 Aug 2024)
- Implemented the `is_repo_read_only` function to determine whether a repository is read-only, helping users avoid unauthorized write operations.

### Latest Release: 0.2 (05 Aug 2024)
- Added the `check_repository` function to verify if a GitHub repository exists and handle various error scenarios such as permissions issues and rate limit exhaustion.

### Latest Release: 0.1 (05 Aug 2024)
- Introduced the `get_rate_limit` function to fetch the current rate limit from the GitHub API, ensuring users can manage their API request limits effectively.