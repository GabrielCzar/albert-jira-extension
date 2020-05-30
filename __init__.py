"""Simple Jira extension."""

import os
import traceback
from pathlib import Path
import re

import albertv0 as v0

# initial configuration

__iid__ = "PythonInterface/v0.2"
__simplename__ = "jira"
__version__ = "0.1"
__trigger__ = "jira "
__author__ = "Gabriel Cesar"
__dependencies__ = []
__prettyname__ = "Simple Jira extension"
__homepage__ = "https://github.com/gabrielczar/albert-jira-extension"

file_dirname = os.path.dirname(__file__)
icon_path = os.path.join(file_dirname, "static", "images", "jira_blue")

cache_path = Path(v0.cacheLocation()) / __simplename__
config_path = Path(v0.configLocation()) / __simplename__
data_path = Path(v0.dataLocation()) / __simplename__

server_path = config_path / "server"
issue_regex = re.compile(r"\w+\/", re.IGNORECASE)


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
                            v0.FuncAction(
                                f"Removing stored server", remove_server())
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
                results.append(
                    v0.Item(
                        id=__prettyname__,
                        icon=icon_path,
                        text="Search for issue...",
                        actions=[v0.UrlAction(
                            f"Search for issue in Jira", get_search_path(query_string))],
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
                            f"Copied error - report this problem",
                            f"{traceback.format_exc()}",
                        ),
                        v0.UrlAction(
                            f"Report error!", "https://github.com/gabrielczar/albert-jira-extension/issues/new")
                    ],
                ),
            )

    return results


def get_server_path():
    server = load_data("server")
    if not "https://" in server:
        server = "https://" + server
    return server


def get_issue_path(raw_issue):
    server = get_server_path()
    issue = issue_regex.sub("", raw_issue)
    return server + "/browse/" + issue


def get_search_path(text):
    server = get_server_path()
    return server + "/issues/?jql=text%20~%20\"" + text + "\""


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
                        f"Copy error - report this problem",
                        f"{traceback.format_exc()}",
                    ),
                    v0.UrlAction(
                        f"Report error!", "https://github.com/gabrielczar/albert-jira-extension/issues/new")
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
