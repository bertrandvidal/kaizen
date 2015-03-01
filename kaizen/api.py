from kaizen.client import ApiClient
from kaizen.request import Verbs, Request


def _default(arg):
    """Return the empty string if the arg is None"""
    return arg if arg is not None else ""


class ApiRequest(Request):
    """The base Request object containing common methods."""

    def __init__(self, api_key):
        Request.__init__(self)
        self._api_key = api_key
        self._client = ApiClient(api_key)

    # TODO(bvidal): the method send could cache the result from the API
    # and invalid it if any other method is called. Not sure it's useful
    # though... So I don't need it for now.
    def send(self):
        """Send the request to the API.

        Returns:
            the JSON dict response from AgileZen
        Raises:
            requests.exceptions.HTTPError if the request is not successful
        """
        return self._client.send_request(self)

    def get_api_key(self):
        return self._api_key

    def paginate(self, page, size=100):
        """Paginate results from the api.

        Args:
            page: the index of the page to return
            size: the number of entities on each page
        Note:
            see http://dev.agilezen.com/concepts/pagination.html
        """
        return self.update_params({"page": page, "pageSize": size})

    def where(self, filters):
        """Make it possible to filter resource(s) this request will return.

        Args:
            filters: string to be used as a filter
        Note:
            see http://dev.agilezen.com/concepts/filters.html
        """
        return self.update_params({"where": filters})

    def with_enrichments(self, *enrichments):
        """Adds enrichment to the resource(s) this request will return.

        Args:
            enrichments: one or more enrichments to add to the current
            resource(s). Refer to the AgileZen API documentation to know
            available enrichments on each resource.
        Note:
            see http://dev.agilezen.com/concepts/enrichments.html
        """
        return self.update_params({"with": ",".join(enrichments)})


class ZenRequest(ApiRequest):
    """Entry point to access AgileZen's API resources.

    Getting information on one of your projects is as simple as:
    ZenRequest(api_key).projects(project_id).send()
    """

    def projects(self, project_id=None):
        """Access the Project resource. If project_id is None the request will
        list the Projects you have access to.

        Args:
            project_id: id of a specific Project, defaults to None
        """
        return ProjectRequest.from_zen_request(self, project_id)


class ProjectRequest(ApiRequest):
    """Access the Project resource."""

    def __init__(self, api_key, project_id=None):
        ApiRequest.__init__(self, api_key)
        self.update_url("/projects/%s" % _default(project_id))

    @classmethod
    def from_zen_request(cls, zen_request, project_id=None):
        # FIXME: All request attribute - url, verb, ... - are lost they
        # should be transmitted to the 'child' request
        return cls(zen_request.get_api_key(), project_id)

    def phases(self, phase_id=None):
        """Access the Phases resource as a sub-resource of a Project.
        If phase_id is None the request will list all Phases you have access
        to in a given Project.

        Args:
            phase_id: id of a specific Phase, defaults to None
        """
        return self.update_url("/phases/%s" % _default(phase_id))

    def add_phase(self, name, description, index=None, limit=None):
        """Add a new Phase to a Project.

        Args:
            name: the name of the Phase as displayed on the board
            description: the description of the Phase
            index: zero based index into the list of phases, defaults to the
            index before the Backlog
            limit: work in progress limit for phase
        """
        self.update_verb(Verbs.POST)
        phase_data = {"name": name, "description": description}
        if index is not None:
            phase_data.update({"index": index})
        if limit is not None:
            phase_data.update({"limit": limit})
        self.update_data(phase_data)
        return self.phases()

    def members(self, user_id=None):
        """Return member(s) within a project.
        If user_id is None it will list members.

        Args:
            user_id: the id of the user you want details from
        """
        return self.update_url("/members/%s" % _default(user_id))

