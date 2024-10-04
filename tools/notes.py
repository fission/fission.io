import requests
import re

repo_owner = 'fission'
repo_name = 'fission'

def remove_author_info(input_string):
    """
    Remove the 'by @username in' substring from the input string.

    :param input_string: The original string.
    :return: The modified string without the author information.
    """
    # Use regex to match ' by @username in' where username can be alphanumeric and contain dashes
    modified_string = re.sub(r' by @[a-zA-Z0-9-]+ in', '', input_string)

    # Strip leading and trailing whitespace
    return modified_string.strip()

def get_merged_pr_commit_sha(repo_owner, repo_name, pr_number):
    """
    Get the commit SHA of a merged pull request from a public repository.

    :param repo_owner: The owner of the repository (GitHub username or organization).
    :param repo_name: The name of the repository.
    :param pr_number: The number of the pull request.
    :return: Commit SHA if PR is merged, otherwise None.
    """
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}"

    response = requests.get(url)

    if response.status_code == 200:
        pr_data = response.json()
        if pr_data['merged_at']:  # Check if the PR is merged
            return pr_data['merge_commit_sha']
        else:
            print("Pull request is not merged.")
    else:
        print(f"Failed to retrieve PR: {response.status_code} - {response.text}")

    return None

def read_file(file_name):
    """Read content from a file and return the content as a string."""
    with open(file_name, 'r') as f:
        return f.read()

def format_commit_and_pull_link(line):
    """Format the commit and pull link based on the provided line."""
    cols = line.split(' ')
    if len(cols) > 2:
        pull_number = cols[-1].lstrip('#')
        commit = get_merged_pr_commit_sha(repo_owner=repo_owner, repo_name=repo_name, pr_number=pull_number)
        # Format commit link
        commit_link = "[{0}](https://github.com/fission/fission/commit/{0})".format(commit[:8])

        # Put pull number, format and replace in the column
        formatted_pull_link = "[{0}](https://github.com/fission/fission/pull/{1})".format(pull_number, pull_number.replace('#', ''))
        cols[-1] = formatted_pull_link
        cols = ' '.join(cols)
        cols = remove_author_info(cols)

        return '* ' + commit_link + ' ' + cols

    return line

def main():
    data = read_file('notes.txt')
    lines = data.split('\n')

    for line in lines:
        formatted_line = format_commit_and_pull_link(line)
        print(formatted_line)

if __name__ == "__main__":
    main()
