"""
This module is an entrypoint to AgentQL service
"""

from playwright.sync_api import Page as _Page

from agentql.ext.playwright._network_monitor import PageActivityMonitor
from agentql.ext.playwright.sync_api import Page
from agentql.ext.playwright.sync_api._utils_sync import (
    add_dom_change_listener_shared,
    add_request_event_listeners_for_page_monitor_shared,
)


def wrap(page: _Page) -> Page:
    """
    Casts a Playwright Sync `Page` object to an AgentQL `Page` type to get access to the AgentQL's querying API.
    See `agentql.ext.playwright.sync_api.Page` for API details.
    """
    # pylint: disable=W0212
    # This is added to capture pages that have already navigated without calling `goto()`
    if page._page_monitor is None:
        page._page_monitor = PageActivityMonitor()
        add_request_event_listeners_for_page_monitor_shared(page, page._page_monitor)

    add_dom_change_listener_shared(page)
    return page  # type: ignore
