"""Github API client."""

import posixpath
from urllib.parse import (
    urlparse,
    urlunparse,
)

import github
import requests
from requests.adapters import (
    HTTPAdapter,
    Retry,
)


class GitHubAPIError(Exception):
    """Base Github API error."""


class GitHubAPIClient:
    """Client for interacting with the GitHub API."""

    def __init__(self, api_user, api_token, api_root="https://api.github.com/"):
        """
        Initialize the GitHubAPIClient instance.

        Args:
            api_user (str): The GitHub username.
            api_token (str): The GitHub API token.
            api_root (str): The root URL for the GitHub API. Defaults to "https://api.github.com/".
        """
        self._client = None
        self._requests = requests.sessions.Session()
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        self._requests.mount("https://", HTTPAdapter(max_retries=retries))
        self._authorize(api_user, api_token)
        self._api_root = api_root

    def _authorize(self, api_user, api_token):
        """
        Authorize the client with GitHub.

        Args:
            api_user (str): The GitHub username.
            api_token (str): The GitHub API token.
        """
        self._requests.auth = (api_user, api_token)
        self._client = github.Github(api_token)

    def _make_url_for(self, *elements):
        """
        Construct a GitHub API URL by joining the provided elements.

        Args:
            *elements: The parts of the URL path.

        Returns:
            str: The constructed URL.
        """
        parsed = list(urlparse(self._api_root))
        parsed[2] = posixpath.join(parsed[2], *elements)
        return urlunparse(parsed)

    def _make_org_membership_url_for_user(self, org, member):
        """
        Construct the URL for checking or modifying a user's membership in an organization.

        Args:
            org (str): The organization name.
            member (str): The username of the member.

        Returns:
            str: The constructed URL.
        """
        return self._make_url_for("orgs", org, "memberships", member)

    def check_membership(self, org, member):
        """
        Check if a user is a member of an organization.

        Raise an error if we are not ourselves a member, since we can then
        only check public membership, which is not good enough for leavers.

        Args:
            org (str): The organization name.
            member (str): The username of the member.

        Returns:
            bool: True if the member is in the organization, False otherwise.

        Raises:
            GitHubAPIError: If an unexpected status code is returned.
        """
        url = self._make_org_membership_url_for_user(org, member)
        response = self._requests.get(url, allow_redirects=False)
        if response.status_code == 200:
            return True
        if response.status_code == 404:
            return False
        response.raise_for_status()
        raise GitHubAPIError(
            f"unexpected non-error status code {response.status_code} from {url}"
        )

    def remove_membership(self, org, member):
        """
        Remove a user from an organization.

        There are two endpoints that sound like they ought to handle removal:

        * Remove an organization member:
            https://docs.github.com/en/rest/reference/orgs#remove-an-organization-member

        * Remove organization membership for a user:
            https://docs.github.com/en/rest/reference/orgs#remove-organization-membership-for-a-user

        We use the latter because it yields a 403 instead of a 404 when the
        token lacks admin:org. The first yields a 404, which is useless.

        It's unclear why there are two similar APIs. Perhaps the latter is
        a newer version of the first, with the ability to raise a 403?

        Args:
            org (str): The organization name.
            member (str): The username of the member to remove.

        Returns:
            bool: True if the removal was successful, False otherwise.

        Raises:
            GitHubAPIError: If an unexpected status code is returned.
        """
        url = self._make_org_membership_url_for_user(org, member)
        response = self._requests.delete(url)
        if response.status_code == 204:
            return True
        response.raise_for_status()
        raise GitHubAPIError(
            f"unexpected non-error status code {response.status_code} from {url}"
        )

    def get_user_id(self, username):
        """
        Get the GitHub user ID from a username.

        Args:
            username (str): The GitHub username.

        Returns:
            int or None: The user ID if found, None if the user does not exist.

        Raises:
            github.UnknownObjectException: If an error occurs while fetching the user.
        """
        try:
            return self._client.get_user(username).id
        except github.UnknownObjectException as e:
            # It seems there were occurrences of 404 on rate limits too
            # Let's check the message then
            if e.data.get("message") == "Not Found":
                return None
            raise
