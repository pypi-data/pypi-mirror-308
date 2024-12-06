from snowflake.demos._demo_connection import DemoConnection
from snowflake.demos._demo_handle import DemoHandle
from snowflake.demos._demos_loader import DemosLoader
from snowflake.demos._utils import cleanup_demos_download, print_demo_list, read_demo_mapping_with_cache


def help() -> None:
    """Print help message."""
    print("Welcome to Snowflake Examples Library")
    print("Run the following in your interactive Python shell:\n")
    print("from snowflake.demos import load_demo")
    print("load_demo('<demo-name>')\n")
    print_demo_list()


def load_demo(demo_name: str, refresh_demo: bool = False) -> DemoHandle:
    """Load the demo with the given name.

    Parameters
    __________
      demo_name: The name of the demo to load.
      refresh_demo: Whether to refresh the demos from snowflake demo repository.

    Returns
    _______
      The demo handle which can be used perform certain actions on demo.
    """
    demo_mapping = read_demo_mapping_with_cache()
    if demo_name not in demo_mapping.keys():
        raise ValueError(f"Demo '{demo_name}' not found. Please call help() to see the list of available demos.")
    return DemosLoader().get_demo_handle(demo_name, refresh_demo)


def teardown() -> None:
    """Teardown all the demo."""
    demo_connection = DemoConnection()
    demo_connection.teardown()
    cleanup_demos_download()
