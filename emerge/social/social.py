"""
Contains an implementation of the louvain modularity graph metric.
"""

# Authors: Grzegorz Lato <grzegorz.lato@gmail.com>
# License: MIT

from typing import Dict, Any
from enum import auto
import logging
import coloredlogs

from networkx import DiGraph
import community as community_louvain

from emerge.abstractresult import AbstractResult
from emerge.results import FileResult, EntityResult
from emerge.log import Logger
from emerge.graph import GraphRepresentation, GraphType

# enums and superclass of the given metric
from emerge.metrics.abstractmetric import EnumLowerKebabCase
from emerge.metrics.metrics import GraphMetric


LOGGER = Logger(logging.getLogger('metrics'))
coloredlogs.install(level='E', logger=LOGGER.logger(), fmt=Logger.log_format)

class SocialNetworkMetric(GraphMetric):
    class Keys(EnumLowerKebabCase):
        _DEPENDENCY_GRAPH = auto()
        _DEPENDENCY_GRAPH = auto()
        _DEPENDENCY_GRAPH = auto()
        _DEPENDENCY_GRAPH = auto()
        _DEPENDENCY_GRAPH = auto()
        _DEPENDENCY_GRAPH = auto()
        _DEPENDENCY_GRAPH = auto()
        _DEPENDENCY_GRAPH = auto()
        _DEPENDENCY_GRAPH = auto()
        _DEPENDENCY_GRAPH = auto()
        _DEPENDENCY_GRAPH = auto()
        _DEPENDENCY_GRAPH = auto()
        _DEPENDENCY_GRAPH = auto()
        _DEPENDENCY_GRAPH = auto()
        _DEPENDENCY_GRAPH = auto()
        _DEPENDENCY_GRAPH = auto()
        _DEPENDENCY_GRAPH = auto()
        _DEPENDENCY_GRAPH = auto()
        _DEPENDENCY_GRAPH = auto()
        _DEPENDENCY_GRAPH = auto()
        _DEPENDENCY_GRAPH = auto()
        _DEPENDENCY_GRAPH = auto()
        _DEPENDENCY_GRAPH = auto()
        _DEPENDENCY_GRAPH = auto()
        _DEPENDENCY_GRAPH = auto()
        _DEPENDENCY_GRAPH = auto()
        _DEPENDENCY_GRAPH = auto()
        _DEPENDENCY_GRAPH = auto()
        _DEPENDENCY_GRAPH = auto()
        