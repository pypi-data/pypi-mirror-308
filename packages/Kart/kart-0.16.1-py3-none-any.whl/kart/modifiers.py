from abc import ABC, abstractmethod

from kart.utils import KartDict, KartMap, default_list


class ContentModifier(ABC):
    """Base ContentModifier class."""

    @abstractmethod
    def modify(self, config: dict, site: KartDict):
        """Takes as input the site and modifies it."""


class MapModifier(ABC):
    """Base MapModifier class."""

    @abstractmethod
    def modify(self, config: dict, site: KartDict, sitemap: KartMap):
        """Takes as input the site and the site map and modifies them."""


class RuleContentModifier(ContentModifier):
    """ContentModifier that executes a list of user defined functions."""

    def __init__(self, rules: list = None):
        self.rules = default_list(rules)  # a rule is a function

    def modify(self, config: dict, site: KartDict):
        for rule in self.rules:
            rule(site)


class RuleMapModifier(MapModifier):
    """MapModifier that executes a list of user defined functions."""

    def __init__(self, rules: list = None):
        self.rules = default_list(rules)  # a rule is a function

    def modify(self, config: dict, site: KartDict, sitemap: KartMap):
        for rule in self.rules:
            rule(sitemap, site)


class CollectionSorter(ContentModifier):
    """Modifier which sorts a collection based on a key."""

    def __init__(self, collection, key, reverse=False):
        self.collection = collection
        self.key = key
        self.reverse = reverse

    def modify(self, config: dict, site: KartDict):
        """Sorts the collection."""
        data = site[self.collection]
        sorted_data = sorted(data.items(), key=lambda x: x[1][self.key])
        if self.reverse:
            sorted_data.reverse()
        site[self.collection] = KartDict(sorted_data)
