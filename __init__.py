"""Simple Jira Issue Tracking."""

import os
import traceback
from pathlib import Path

import albertv0 as v0

# initial configuration 

__iid__ = "PythonInterface/v0.2"
__simplename__ = "jira"
__version__ = "0.1"
__trigger__ = "jira "
__author__ = "Gabriel Cesar"
__dependencies__ = []
__prettyname__ = "Simple Jira Plugin"
__homepage__ = "https://github.com/gabrielczar/albert-jira-plugin"

icon_path = os.path.join(os.path.dirname(__file__), "jira_blue")

cache_path = Path(v0.cacheLocation()) / __simplename__
config_path = Path(v0.configLocation()) / __simplename__
data_path = Path(v0.dataLocation()) / __simplename__

server_path = config_path / "server"


def initialize():
    for p in (cache_path, config_path, data_path):
        p.mkdir(parents=False, exist_ok=True)


def finalize():
    pass


def handleQuery(query):
    results = []

    if query.isTriggered:
        try:

            results_setup = setup(query)
            if results_setup:
                return results_setup

            query_string = query.string

            if "remove server" in query_string:
                results.append(
                    v0.Item(
                        id=__prettyname__,
                        icon=icon_path,
                        text="Remove server",
                        actions=[
                            v0.FuncAction(f"Removing stored server", remove_server())
                        ]
                    )
                )
            else:
                results.append(
                    v0.Item(
                        id=__prettyname__,
                        icon=icon_path,
                        text="Open issue...",
                        actions=[v0.UrlAction(
                            f"Open issue in Jira", get_issue_path(query_string))],
                    )
                )

        except Exception:
            results.insert(
                0,
                v0.Item(
                    id=__prettyname__,
                    icon=icon_path,
                    text="Something went wrong! Press [ENTER] to copy error and report it",
                    actions=[
                        v0.ClipAction(
                            f"Copy error - report something",
                            f"{traceback.format_exc()}",
                        )
                    ],
                ),
            )

    return results


def get_issue_path(issue):
    server = load_data("server")
    if not "https://" in server:
        server = "https://" + server
    return server + "/browse/" + issue    

def setup(query):
    results = []

    try: 
        if not server_path.is_file():
            results.append(
                v0.Item(
                    id=__prettyname__,
                    icon=icon_path,
                    text=f"Please specify the JIRA server to connect to",
                    subtext="Fill and press [ENTER]",
                    actions=[
                        v0.FuncAction(
                            "Save JIRA server", lambda: save_data(
                                query.string, "server")
                        )
                    ],
                )
            )
    except Exception:
        remove_server()
        results.insert(
                0,
                v0.Item(
                    id=__prettyname__,
                    icon=icon_path,
                    text="Something went wrong! Please try again!",
                    actions=[
                        v0.ClipAction(
                            f"Copy error - report something",
                            f"{traceback.format_exc()}",
                        )
                    ],
                ),
            )
    return results

def save_data(data: str, data_name: str):
    """Save a piece of data in the configuration directory."""
    with open(config_path / data_name, "w") as f:
        f.write(data)

def load_data(data_name) -> str:
    """Load a piece of data from the configuration directory."""
    with open(config_path / data_name, "r") as f:
        data = f.readline().strip().split()[0]

    return data

def remove_server():
    os.remove(config_path / "server")