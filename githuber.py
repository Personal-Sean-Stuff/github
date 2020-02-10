#!/usr/bin/python
import argparse
import requests
from requests.auth import HTTPBasicAuth


def returnDict(username, password, org):
    """
    Get the repo names from the organization
    and use findBranches to count the number of branches in each repository
    """
    final_dict = {}
    repositories = requests.get('https://api.github.com/orgs/{}/repos'.format(org),
                                auth=HTTPBasicAuth(username, password)).json()
    for repo in repositories:
        final_dict[repo['name']] = findBranches(username, password, repo['name'], repo['owner']['login'])
    return final_dict


def findBranches(username, password, repo_name, owner):
    count = 0
    branches = requests.get('https://api.github.com/repos/{}/{}/branches'.format(owner, repo_name),
                            auth=HTTPBasicAuth(username, password))
    if branches.status_code == 200:
        branches = branches.json()
        for branch in branches:
            count += 1
    return count


def main():
    parser = argparse.ArgumentParser(description='Process the variables')
    parser.add_argument('org', help='GitHub organization name')
    parser.add_argument('user', help='GitHub user name')
    parser.add_argument('password', help='GitHub password')
    args = parser.parse_args()
    final_dict = returnDict(args.user, args.password, args.org)
    print('{:<8} | {:<15}'.format('Repo Name', 'Branch Number'))
    for k, v in final_dict.items():
        print("{:<8}  | {:<15}".format(k, v))


if __name__ == "__main__":
    main()

