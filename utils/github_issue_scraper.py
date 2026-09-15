import requests
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from urllib.parse import urlparse

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
    res = results[0]
    print(res["relevance_score"])
    if res["relevance_score"] < 0.5:
        return None
    corresponding_authors = [
        author["author"]
        for author in res["authorships"]
        if author.get("is_corresponding", False)
    ]
    # if no corresponding authors, take the first author
    if not corresponding_authors:
        corresponding_authors = [
            author["author"]
            for author in res["authorships"]
            if author.get("author_position", "") == "first"
        ]
    print(corresponding_authors)


def get_author_profile(openalex_author_id: str):
    """Get author metadata from OpenAlex."""
    url = f"https://api.openalex.org/authors/{openalex_author_id}"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()


def find_public_email(author_name: str, institution: str | None = None):
    """
    Search the web for a publicly listed professional email.

    Returns:
        {
            "email": ...,
            "url": ...,
            "source": ...
        }
        or None
    """

    query = f'"{author_name}"'

    if institution:
        query += f' "{institution}"'

    query += " email"

    # DuckDuckGo HTML search
    search_url = "https://html.duckduckgo.com/html/"

    response = requests.get(
        search_url,
        params={"q": query},
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30,
    )
    response.raise_for_status()
    print(response.text)

    soup = BeautifulSoup(response.text, "html.parser")

    results = []

    for result in soup.select(".result"):
        link = result.select_one(".result__a")

        if not link:
            continue

        url = link.get("href")

        if not url:
            continue

        title = link.get_text(" ", strip=True)

        snippet = result.select_one(".result__snippet")
        snippet = snippet.get_text(" ", strip=True) if snippet else ""

        results.append(
            {
                "title": title,
                "url": url,
                "snippet": snippet,
            }
        )

    print(results)

    # Search the result pages for an explicitly published email
    for result in results:
        try:
            page = requests.get(
                result["url"],
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=15,
            )

            if not page.ok:
                continue

            emails = EMAIL_RE.findall(page.text)

            # Remove obvious non-personal/irrelevant addresses
            emails = [
                email
                for email in emails
                if not any(
                    x in email.lower()
                    for x in [
                        "example.com",
                        "example.org",
                        "sentry.io",
                        "wixpress.com",
                        "cloudflare",
                    ]
                )
            ]

            if emails:
                return {
                    "email": emails[0],
                    "url": result["url"],
                    "source": result["title"],
                }

        except requests.RequestException:
            continue

    return None


issues = get_issues(
    repo=REPO,
    label=LABEL,
)


"""
for issue in issues:
    links = extract_links(issue.get("body", ""))
    if not links:
        paper = find_paper(issue.get("body", ""))
    print(issue["number"], issue["title"])
    print(links)
"""
