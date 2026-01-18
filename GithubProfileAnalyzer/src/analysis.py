from collections import defaultdict
import pandas as pd

def process_profile_data(raw_data):
    """
    Process the raw GraphQL response from GitHub API.
    Returns a DataFrame of languages and the total commit count.
    """
    try:
        repos = raw_data["data"]["user"]["repositories"]["nodes"]
    except KeyError:
        return None, 0

    language_totals = defaultdict(int)
    commit_total = 0

    for repo in repos:
        # Count commits
        if repo["defaultBranchRef"] and repo["defaultBranchRef"]["target"]:
             try:
                commit_total += repo["defaultBranchRef"]["target"]["history"]["totalCount"]
             except (TypeError, KeyError):
                pass
        
        # Count languages
        if repo["languages"] and repo["languages"]["edges"]:
            for lang in repo["languages"]["edges"]:
                language_totals[lang["node"]["name"]] += lang["size"]

    if not language_totals:
        return None, 0

    df = pd.DataFrame(
        [{"language": k, "bytes": v} for k, v in language_totals.items()]
    )
    df["percentage"] = df["bytes"] / df["bytes"].sum() * 100
    df = df.sort_values("percentage", ascending=False)
    
    return df, commit_total
