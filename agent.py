import os
import sys

# ADK's agent loader imports this file as a submodule of whatever directory
# name it happens to be invoked from (e.g. `<project_dir>.agent`), and only
# adds that directory's *parent* to sys.path -- not this directory itself.
# Without this, `placement_agent` (a sibling package next to this file)
# can't be found as a top-level import.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from placement_agent.coordinator import root_agent

__all__ = ["root_agent"]