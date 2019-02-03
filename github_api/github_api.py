from github import Github


class GithubApi:
    def __init__(self, token):
        self.connection = Github(token)

    def get_connection(self):
        return self.connection

    def get_repo_by_name(self, repo_name):
        return self.connection.get_repo(repo_name)

    def get_all_issues(self, repo_name):
        issue_from_repo = self.get_repo_by_name(repo_name).get_issues()
        issues_list = []
        for i in issue_from_repo:
            if len(i.labels) > 0:
                for label in list(i.labels):
                    issues_list.append(
                        {'title': i.title, 'body': i.body, 'label': label.name if label is not None else '',
                         'milestone': i.milestone.title if i.milestone is not None else '',
                         'assignee': i.assignee, 'number': i.number})
            else:
                issues_list.append(
                    {'title': i.title, 'body': i.body, 'label': '',
                     'milestone': i.milestone.title if i.milestone is not None else '', 'assignee': i.assignee,
                     'number': i.number})

        return issues_list

    def get_all_labels_in_repo(self, repo_name):
        return [label.name for label in self.get_repo_by_name(repo_name).get_labels()]

    def get_names_of_branch(self, repo_name):
        return [branch.name for branch in self.get_repo_by_name(repo_name).get_branches()]

    def create_new_issue(self, repo_name, title, body=None, label=None, milestone=None):
        repo = self.get_repo_by_name(repo_name)
        current_milestones = repo.get_milestones()
        current_milestones_name = [milestone.title for milestone in repo.get_milestones()]

        if not milestone:
            repo.create_issue(title=title, body=body, labels=[label])
        elif milestone and milestone not in current_milestones_name:
            milestone = repo.create_milestone(milestone)
            repo.create_issue(title=title, body=body, labels=[label], milestone=milestone)
        elif milestone is not None:
            milestone = current_milestones[current_milestones_name.index(milestone)]
            repo.create_issue(title=title, body=body, labels=[label], milestone=milestone)
