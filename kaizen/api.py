from kaizen.client import ApiClient
from kaizen.request import Request


def _default(arg):
  """Return the empty string if the arg is None"""
  return arg if arg is not None else ""


class ZenRequest(Request):
  """The main object to use to retrieve resources from the AgileZen API.

  Getting information on one of your projects is as simply as:
  ZenRequest(api_key).projects(project_id).send()
  """
  # TODO(bvidal): the method send could cache the result from the API
  # and invalid it if any other method is called. Not sure it's useful
  # though... So I don't need it for now.

  def __init__(self, api_key):
    Request.__init__(self)
    self._client = ApiClient(api_key)

  def send(self):
    """Send the request to the API.

    Returns:
      - the JSON dict response from AgileZen
    Raises:
      - requests.exceptions.HTTPError if the request is not successful
    """
    return self._client.make_request(self.verb, self.url, self.params,
                                     self.data)

  def with_enrichments(self, *enrichments):
    """Adds enrichment to the resource(s) this request will return.

    Args:
      enrichments: one or more enrichments to add to the current resource(s).
      Refer to the AgileZen API documentation to know available enrichments on
      each resource.
    """
    return self.update_params({"with": ",".join(enrichments)})

  def projects(self, project_id=None):
    """Access the Project resource. If project_id is None the request will list
    the Project you have access to.

    Args:
      project_id: id of a specific Project, defaults to None
    """
    return self.update_url("/projects/%s" % _default(project_id))

