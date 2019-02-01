
from github import Github


class GithubApi:
    def __init__(self, token):
        self.connection = Github(token)

    def get_connection(self):
        return self.connection

    def get_repo_by_name(self, repo_name):
        return self.connection.get_repo(repo_name)

    def get_all_issues(self, repo_name):
        return self.get_repo_by_name(repo_name).get_issues()

    def get_all_labels_in_repo(self, repo_name):
        return self.get_repo_by_name(repo_name).get_labels()

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
        elif milestone is not None:
            milestone = current_milestones[current_milestones_name.index(milestone)]
        repo.create_issue(title=title, body=body, labels=[label], milestone=milestone)



# g = GithubApi('aa16de1b380f0f862a65f19feb042787090aad61')
# print(g.get_connection().get_user().login)
# repo = g.get_repo_by_name("dupa, dupa")
# print(list(repo.get_milestones()))
# print([milestone.title for milestone in repo.get_milestones()])
# repo.create_milestone('New')
# d = repo.get_issues()
# for i in d:
#     print(i)




