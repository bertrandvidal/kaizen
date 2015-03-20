from kaizen.api import ZenRequest
from parse_this import parse_class, create_parser, Self
from pprint import pprint


@parse_class()
class ZenApi(object):
    """Simplify access to the AgileZen API."""

    @create_parser(Self, str)
    def __init__(self, api_key):
        """
        Args:
            api_key: the API key given by AgileZen
        """
        self._zen_request = ZenRequest(api_key)

    @create_parser(Self)
    def list_projects(self, phases=False, members=False, metrics=False):
        """List all Projects you have access to.

        Args:
            phase: add the phases to the Project object
            members: add the members to the Project object
            metrics: add the metrics to the Project object
        """
        request = self._zen_request.projects()
        enrichments = [name for name, value in
                       [("phases", phases), ("members", members),
                        ("metrics", metrics)]
                       if value]
        if enrichments:
            request = request.with_enrichments(*enrichments)
        return request.send()

    @create_parser(Self, int, bool, bool, int, int)
    def list_stories(self, project_id, tasks=False, tags=False, page=1,
                     size=100):
        """List stories in the Project specified by the given id.

        Args:
            project_id: id of the Project you want to list Stories
            tasks: should the tasks be included in the stories
            tags: should the tags be included in the stories
            page: page number to display, defaults to the first page
            size: max number of stories to return, defaults to 100
        """
        request = self._zen_request.projects(project_id).stories()
        enrichments = [name for name, value in
                       [("tasks", tasks), ("tags", tags)] if value]
        if enrichments:
            request = request.with_enrichments(*enrichments)
        return request.paginate(page, size).send()

    @create_parser(Self, int)
    def list_phases(self, project_id, stories=False, page=1, size=100):
        """List phases in the Project specified by the given id.

        Args:
            project_id: id of the Project you want to list Stories
            stories: should the stories be included in the phases
            page: page number to display, defaults to the first page
            size: max number of stories to return, defaults to 100
        """
        request = self._zen_request.projects(project_id).phases()
        if stories:
            request = request.with_enrichments("stories")
        return request.paginate(page, size).send()

    @create_parser(Self, int, str, str, int, int)
    def add_phase(self, project_id, name, description, index=None, limit=None):
        """Add a Phase to the Project specified by the given id.

        Args:
            project_id: id of the Project to add the Phase to
            name: name of the newly created Phase
            description: description of the newly created Phase
            index: the zero based index into the list of phases
            limit: Work in progress limit for phase
        """
        return self._zen_request.projects(project_id).phases()\
                   .add(name, description, index, limit).send()

    def _get_next_phase_id(self, phase_name, project_id):
        # We can assume we won't need to paginate and go over more than 100 Phases
        phases = self.list_phases(project_id)["items"]
        if phases[-1]["name"] == phase_name:
            raise ValueError("Story is already in the last phase '%s'"
                             % phase_name)
        for (idx, phase) in enumerate(phases):
            if phase["name"] == phase_name:
                return phases[idx + 1]["id"]
        raise ValueError("Unknown phase '%s'" % phase_name)

    @create_parser(Self, int, int, name="bump-phase")
    def move_story_to_next_phase(self, project_id, story_id):
        """The Story will be moved to the next Phase.

        Args:
            project_id: id of the Project
            story_id: id of the Story to move
        """
        request = self._zen_request.projects(project_id)
        story_request = request.stories(story_id)
        story = story_request.send()
        try:
            phase_id = self._get_next_phase_id(story["name"]["name"], project_id)
        except ValueError as error:
            return error.message
        return story_request.update(phase_id=phase_id).send()

    # TODO: Possible methods to implement include:
    #  - pop_next: pop the top Story of the "todo" phase and move it to
    #    "working" assigning it to the user
    #  - stats: list # of Story per user - also grouped by status/phase
    #  - todo: list Story in the "todo" phase
    #  - done: move Story to the "done" phase
    # For those methods the concept of configuration should be introduced. It
    # would contain: the username, name of the "todo" and "working" phases,
    # api key, etc...


def run_cli():
    pprint(ZenApi.parser.call())


if __name__ == "__main__":
    run_cli()
