from github import Github


class GithubApi:
    def __init__(self, username, password):
        self.connection = Github(username, password)

    def get_connection(self):
        return self.connection

    def get_repo_by_name(self, repo_name):
        return self.connection.get_repo(repo_name)

    def get_number_of_issue_in_repo_by_status(self, repo_name, status):
        return list(self.get_repo_by_name(repo_name).get_issues(status=status))

    def get_all_labels_in_repo(self, repo_name):
        return self.get_repo_by_name(repo_name).get_labels()

    def get_names_of_branches(self, repo_name):
        return [branch.name for branch in self.get_repo_by_name(repo_name)]




