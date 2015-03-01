"""This module deals with HTTP related concerns regarding AgileZen API."""
import json
import logging
import requests

_LOG = logging.getLogger(__name__)
# requests logs a line every time a new connection is established
logging.getLogger("requests").setLevel(logging.ERROR)


def default_dict(obj):
    """Returns an empty dict if the object is empty."""
    return obj or {}


class ApiClient(object):
    """Ease making calls to AgileZen API."""

    API_URL = "https://agilezen.com/api/v1"

    def __init__(self, api_key):
        """
        Args:
            api_key: the AgileZen api key
        """
        self._api_key = api_key

    def send_request(self, request, headers=None):
        """Send a HTTP request, from which url, verb, params and data are taken

        Args:
            request: the request to send
            headers: headers to send

        Returns:
            the dict loaded from the json response

        Raises:
            a requests.HTTPError if the status code is not OK
        """
        url = self._get_url(request.url)
        headers = default_dict(headers)
        data = json.dumps(default_dict(request.data))
        params = default_dict(request.params)
        response = requests.request(request.verb, url, params=params,
                                    data=data,
                                    headers=self._get_headers(headers))
        response.raise_for_status()
        _LOG.debug("request issued to '%s' [%s s]", url,
                   response.elapsed.total_seconds())
        return response.json()

    def _get_url(self, resource_path):
        """Return the full URL to an API resource

        Args:
            resource_path: path to the resource from the API root
        """
        resource_path = "/%s" % resource_path.lstrip("/")
        return "%s%s" % (self.__class__.API_URL, resource_path)

    def _get_headers(self, headers):
        """Return the given headers update with headers required by the API.

        Args:
            headers: headers provided by the user
        """
        headers.update({
            "Accept": "application/json",
            "Content-type": "application/json",
            "X-Zen-ApiKey": self._api_key
        })
        return headers

