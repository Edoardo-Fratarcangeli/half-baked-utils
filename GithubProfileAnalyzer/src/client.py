import requests

class GitHubClient:
    ENDPOINT = "https://api.github.com/graphql"

    def __init__(self, token: str):
        self.headers = {"Authorization": f"Bearer {token}"}

    def fetch_profile(self, username: str):
        query = """
        query($login: String!) {
          user(login: $login) {
            repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {
              nodes {
                name
                languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
                  edges {
                    size
                    node { name }
                  }
                }
                defaultBranchRef {
                  target {
                    ... on Commit {
                      history(first: 0) {
                        totalCount
                      }
                    }
                  }
                }
              }
            }
          }
        }
        """
        response = requests.post(
            self.ENDPOINT,
            headers=self.headers,
            json={"query": query, "variables": {"login": username}}
        )
        response.raise_for_status()
        return response.json()
