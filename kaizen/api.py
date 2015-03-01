from kaizen.client import ApiClient
from kaizen.request import VERBS, Request


def _default_to_empty_str(arg):
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

    @classmethod
    def from_zen_request(cls, zen_request, project_id=None):
        """Creates a ProjectRequest with all the attributes of the ZenRequest.

        Args:
            zen_request: ZenRequest used to get the ProjectRequest attributes
            project_id: id of the Project to work on or None to get access
            to the list of Projects
        """
        request = cls(zen_request.get_api_key())
        request = zen_request.copy(request)
        return request.update_url("/projects/%s" %
                                  _default_to_empty_str(project_id))

    def update(self, name=None, description=None, details=None, owner=None):
        """Update a Project witht the given arguments.

        Args:
            name: name of the project
            description: a short description of the project
            details: a markdown-formatted free-from description of the project
            owner: owner of the project

        Note:
            for the owner see: http://dev.agilezen.com/resources/users.html
        """
        if name is not None:
            self.update_data({"name": name})
        if description is not None:
            self.update_data({"description": description})
        if details is not None:
            self.update_data({"details": details})
        if owner is not None:
            self.data.update({"owner": owner})
        return self.update_verb(VERBS.PUT)

    def phases(self, phase_id=None):
        """Access the Phases resource as a sub-request of a Project.
        If phase_id is None the request will list all Phases you have access
        to in a given Project.

        Args:
            phase_id: id of a specific Phase, defaults to None
        """
        return PhaseRequest.from_project_request(self, phase_id)

    def members(self, user_id=None):
        """Return member(s) within a project.
        If user_id is None it will list members.

        Args:
            user_id: the id of the user you want details from
        """
        return self.update_url("/members/%s" % _default_to_empty_str(user_id))


class PhaseRequest(ApiRequest):
    """Give access to the Phase entry point."""

    @classmethod
    def from_project_request(cls, project_request, phase_id=None):
        """Create a PhaseRequest as a sub-resource of a ProjectRequest

        Args:
            project_request: the ProjectRequest to which the PhaseRequest will
            be linked
            phase_id: the id of the phase we want to access, or None to be able
            to list the Phases of the Project
        """
        request = cls(project_request.get_api_key())
        request = project_request.copy(request)
        return request.update_url("/phases/%s" %
                                  _default_to_empty_str(phase_id))

    def update(self, name, description, index=None, limit=None):
        """Update information of an existing phase.

        Args:
            name: the name of the Phase as displayed on the board
            description: the description of the Phase
            index: zero based index into the list of phases. Backlog phase
            must have index 0 and Archive must have the last index.
            limit: work in progress limit for phase
        """
        # Update is just like add except it uses PUT
        return self.add(name, description, index, limit).update_verb(VERBS.PUT)

    def add(self, name, description, index=None, limit=None):
        """Add a new Phase to a Project.

        Args:
            name: the name of the Phase as displayed on the board
            description: the description of the Phase
            index: zero based index into the list of phases. Backlog phase
            must have index 0 and Archive must have the last index.
            limit: work in progress limit for phase
        """
        self.update_data({"name": name, "description": description})
        if index is not None:
            self.update_data({"index": index})
        if limit is not None:
            self.update_data({"limit": limit})
        return self.update_verb(VERBS.POST)

