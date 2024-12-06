from snowflake.demos._constants import DEMO_NUM_STEPS_COLUMN, DEMO_REPO_URL_COLUMN
from snowflake.demos._demo_connection import DemoConnection
from snowflake.demos._telemetry import api_telemetry
from snowflake.demos._utils import (
    cleanup_demo,
    create_demo_notebooks,
    create_notebook_url_from_demo_name,
    download_repo,
    get_repo_name_from_url,
    read_demo_mapping_with_cache,
)


class DemoHandle:
    """Handle to interact with a demo.

    When a demo is loaded using `load_demo`, a `DemoHandle` object is returned.
    This object can be used to interact with the demo.
    Please don't try to instantiate this class directly. Use `load_demo` to get a handle for any demo.

    Examples
    ________
    To load a demo:

    >>> from snowflake.demos import load_demo
    >>> demo = load_demo('<demo_name>')
    >>> demo.show()

    To show the next step in the demo:

    >>> demo.show_next()

    To teardown the objects created during the demo:

    >>> demo.teardown()

    To show a specific step in the demo:

    >>> demo.show(2)

    """

    def __init__(self, name: str):
        self._name = name
        self._current_step = 0
        self._num_steps = 0
        self._repo_url = ""
        self._repo_name = ""
        self._demo_connection = DemoConnection()
        self._telemetry_client = None
        self._setup_complete = False

    def _setup_handle(self, refresh_demo: bool = False):
        demo_mapping = read_demo_mapping_with_cache()
        demo_info = demo_mapping[self._name]
        self._num_steps = int(demo_info[DEMO_NUM_STEPS_COLUMN])
        self._repo_url = demo_info[DEMO_REPO_URL_COLUMN]
        self._repo_name = get_repo_name_from_url(demo_info[DEMO_REPO_URL_COLUMN])
        # call this to create the root
        self._demo_connection.setup()
        self._demo_connection = self._demo_connection
        self._telemetry_client = self._demo_connection.get_telemetry_client()
        download_repo(self._repo_url, self._repo_name, refresh_demo)
        create_demo_notebooks(self._name, self._repo_name, self._num_steps, self._demo_connection.get_root())
        self._setup_complete = True

    def _check_is_valid_step(self, step: int) -> None:
        if not (0 <= step < self._num_steps):
            raise ValueError(f"Invalid step. Please provide a step between 0 and {self._num_steps - 1}")

    def _check_setup(self):
        if not self._setup_complete:
            raise ValueError(
                f"Setup not complete. Please reload the demo using load_demo('{self._name}', refresh_demo=True). If the issue persists, please contact Snowflake support."  # noqa: E501
            )

    @api_telemetry
    def show(self, step: int = 0):
        self._check_setup()
        self._check_is_valid_step(step)
        print(
            f"Showing step {step}. Please click on this link to open the notebook: {create_notebook_url_from_demo_name(self._name, self._demo_connection, step)}"  # noqa: E501
        )

    @api_telemetry
    def show_next(self):
        self._check_setup()
        self._current_step += 1
        self._check_is_valid_step(self._current_step)
        print(
            f"Showing step {self._current_step}. Please click on this link to open the notebook: {create_notebook_url_from_demo_name(self._name, self._demo_connection, self._current_step)}"  # noqa: E501
        )

    def teardown(self):
        """Teardown the demo.

        This will delete all the objects created for showing the demo.
        Please note it might not delete the objects created within the demo.

        Examples
        ________
        To teardown the demo:

        >>> from snowflake.demos import load_demo
        >>> demo = load_demo('<demo_name>')
        >>> demo.teardown()
        """
        self._check_setup()
        self._setup_complete = False
        cleanup_demo(self._name, self._num_steps, self._demo_connection.get_root())

    def __repr__(self) -> str:
        self._check_setup()
        return f"Showing step {self._current_step}. Please click on this link to open the notebook: {create_notebook_url_from_demo_name(self._name, self._demo_connection)}"  # noqa: E501
