from abc import ABC, abstractmethod
from fnmatch import fnmatch
from pathlib import Path
from typing import Dict, Union

from watchfiles import Change, awatch

from kart.utils import KartDict, id_from_path

try:
    from yaml import CSafeLoader as YamlLoader
except ImportError:
    from yaml import SafeLoader as YamlLoader


class Miner(ABC):
    """Base miner class."""

    @abstractmethod
    def read_data(self, config: dict):
        """Reads data from its source."""

    @abstractmethod
    def collect(self, config: dict) -> Dict:
        """Collects all data."""

    @abstractmethod
    def start_watching(self, config: dict, callback):
        """Start watching for data changes.

        Returns an async function that watches for changes and executes the callback after each change
        """

    @abstractmethod
    def stop_watching(self, config: dict):
        """Stop watching for data changes."""


class DefaultMiner(Miner):
    """Base miner class for reading from filesystem."""

    name = None
    dir = None
    extensions = ()
    data = None

    @abstractmethod
    def __init__(self):
        """Initializes the miner.

        Must set the ``name`` and ``dir`` variables.
        """

    @abstractmethod
    def collect_single_file(self, file: Path, config: dict):
        """Reads data from a single file."""

    def valid_path(self, path: Union[Path, str]) -> bool:
        return any(fnmatch(path, "*" + ext) for ext in self.extensions)

    def read_data(self, config: dict):
        """Implements Miner.read_data().

        It iterates over a directory and calls collect_single_file() for each file
        """
        self.data = KartDict()
        for file in filter(self.valid_path, filter(Path.is_file, self.dir.iterdir())):
            data = self.collect_single_file(file, config)
            if data:
                self.data.update(data)

    def collect(self, config: dict):
        return {self.name: self.data}

    def start_watching(self, config: dict, callback):
        """Returns a function that calls collect_single_file() when a file has changed."""

        async def watch():
            async for changes in awatch(self.dir, recursive=False):
                done = False
                for change in changes:
                    change_path = Path(change[1])
                    if not self.valid_path(change_path):
                        continue
                    done = True
                    change_path = change_path.relative_to(Path().absolute())
                    if change[0] == Change.deleted:
                        self.data.pop(id_from_path(self.dir, change_path), None)
                    if change[0] in (Change.added, Change.modified):
                        self.data.update(self.collect_single_file(change_path, config))
                if done:
                    await callback()

        self.read_data(config)
        return watch

    def stop_watching(self, config: dict):
        """Implements Miner.stop_watching().

        It does nothing as no cleanup is needed.
        """


class DefaultMarkupMiner(DefaultMiner):
    """Base miner that implements collect_single_file() for markup files."""

    extensions = (".md",)
    markup = "markdown"

    def get_metadata_and_content(self, data: str):
        """Parses the metadata and content of a markup file."""
        data = data.split("---")
        metadata = YamlLoader(data[1]).get_data()
        content = "---".join(data[2:])
        return metadata, content

    def collect_single_file(self, file: Path, config: dict) -> str:
        """Stores the data included in the frontmatter and content data."""
        metadata, content = self.get_metadata_and_content(file.read_text())
        if "draft" in metadata and metadata["draft"] and not config["draft_mode"]:
            return {}
        slug = id_from_path(self.dir, file)
        data = {}
        data["markup"] = self.markup
        data.update(metadata)
        data["content"] = content
        data["slug"] = slug
        return {slug: data}


class DefaultCollectionMiner(DefaultMarkupMiner):
    """Miner that looks for data in the ``collections`` folder."""

    def __init__(self, collection: str, directory: str = "collections"):
        """Initializes miner.

        Sets the ``name``, ``dir`` and ``collection`` variables.
        """
        self.collection = collection
        self.dir = Path() / directory / collection
        self.name = self.collection


class DefaultTaxonomyMiner(DefaultMarkupMiner):
    """Miner that looks for data in the ``taxonomy`` folder."""

    def __init__(self, taxonomy: str, directory: str = "taxonomies"):
        """Initializes miner.

        Sets the ``name``, ``dir`` and ``taxonomy`` variables.
        """
        self.taxonomy = taxonomy
        self.dir = Path() / directory / taxonomy
        self.name = self.taxonomy


class DefaultPageMiner(DefaultMarkupMiner):
    """Miner that get data from the ``pages`` folder."""

    def __init__(self, directory: str = "pages"):
        """Initializes miner.

        Sets the ``name`` and ``dir`` variables.
        """
        self.dir = Path(directory)
        self.name = "pages"


class DefaultDataMiner(DefaultMiner):
    """Miner that get yaml data from the ``data`` folder."""

    extensions = (".yml", ".yaml")

    def __init__(self, directory: str = "data"):
        """Initializes miner.

        Sets the ``name`` and ``dir`` variables.
        """
        self.dir = Path(directory)
        self.name = "data"

    def collect_single_file(self, file: Path, config: dict) -> str:
        """Users YamlLoader to get data from a yaml file."""
        with file.open("r") as f:
            slug = id_from_path(self.dir, file)
            return {slug: YamlLoader(f.read()).get_data()}


class DefaultRobotsTxtMiner(DefaultMiner):
    """Miner that gets data from a robots.txt file."""

    def __init__(self, directory: str = "data"):
        """Initializes miner.

        Sets the ``name`` and ``dir`` variables.
        """
        self.dir = Path(directory)
        self.name = "robots"

    def valid_path(self, path: Union[Path, str]) -> bool:
        return Path(path).name == "robots.txt"

    def collect_single_file(self, file: Path, config: dict):
        """Collects data from robots.txt if present."""
        with file.open("r") as f:
            return {"content": f.read()}


class WatchDirectoryMiner(Miner):
    """Miner that only watches for changes in a list of directories."""

    def __init__(self, dirs: list):
        self.dirs = dirs

    def read_data(self, config: dict):
        """Implements Miner.read_data().

        It does nothing as this miner does not read data
        """

    def collect(self, _):
        return {}

    def start_watching(self, config: dict, callback):
        """Returns a function that calls collect_single_file() when a file has changed."""

        async def watch():
            async for _ in awatch(*self.dirs, recursive=True):
                await callback()

        return watch

    def stop_watching(self, config: dict):
        """Implements Miner.stop_watching().

        It does nothing as no cleanup is needed.
        """
