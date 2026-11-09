# pip install requests bs4

import requests
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import pandas as pd

URL_PATTERN = re.compile(r"https?://[^\s<>\[\]()\"']+")
REPO = "OpenOptimizationOrg/OPL"
LABEL = "new benchmark / problem"
EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")


def get_issues(repo, label, token=None):
    """
    Get all issues from a GitHub repository with a specific label.
    repo: GitHub repository in the format "owner/repo"
    label: label to filter issues by
    token: optional GitHub personal access token
    """
    url = f"https://api.github.com/repos/{repo}/issues"

    headers = {"Accept": "application/vnd.github+json"}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    issues = []
    page = 1

    while True:
        params = {
            "labels": label,
            "state": "all",
            "per_page": 100,
            "page": page,
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()

        batch = response.json()

        if not batch:
            break

        issues.extend(batch)
        page += 1

    return issues


def extract_links(text: str) -> list[str]:
    if not text:
        return []
    links = URL_PATTERN.findall(
        text
    )  # Remove punctuation commonly attached to URLs in prose
    return [link.rstrip(".,;:!?") for link in links]


def extract_emails(text: str) -> list[str]:
    if not text:
        return []
    mails = EMAIL_RE.findall(text)
    return [mail.rstrip(".,;:!?") for mail in mails]


def arxiv_email(arxiv_link: str):
    # Identify arxiv id from link (could be pdf format or /abs format)
    arxiv_id = None
    if "/abs/" in arxiv_link:
        arxiv_id = arxiv_link.split("/abs/")[-1]
    elif "/pdf/" in arxiv_link:
        arxiv_id = arxiv_link.split("/pdf/")[-1].replace(".pdf", "")
    html_url = f"https://arxiv.org/html/{arxiv_id}"

    response = requests.get(html_url, timeout=15)
    if response.status_code != 200:
        return []
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text(" ", strip=True)
    emails = extract_emails(text)
    return emails


def find_paper(citation: str):
    if not citation:
        return None
    url = "https://api.openalex.org/works"

    params = {
        "search": citation,
        "per-page": 10,
    }

    r = requests.get(url, params=params)
    r.raise_for_status()

    results = r.json()["results"]

    if not results:
        return None

    # Verify that the result matches enough
    print(results)
    res = results[0]
    print(res["relevance_score"])
    if res["relevance_score"] < 0.5:
        return None
    else:
        print(res)


if __name__ == "__main__":
    issues = get_issues(
        repo=REPO,
        label=LABEL,
    )
    data = []

    for issue in issues:
        issue_data = {"issue_number": issue["number"], "title": issue["title"]}
        links = extract_links(issue.get("body", ""))
        issue_data["links"] = links
        for l in links:
            if "arxiv.org" in l:
                arxiv_emails = arxiv_email(l)
                issue_data["arxiv_emails"] = arxiv_emails
        paper = find_paper(issue.get("body", ""))
        print(issue_data)
