import math
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from typing import List


class KartDict(OrderedDict):
    """Subclass of OrderedDict with a custom iterator."""

    def __iter__(self):
        """Iterate over the dict values instead of the keys."""
        return iter(self.values())


class KartMap(KartDict):
    """Custom dictionary that holds the site map."""

    def __init__(
        self,
        initial_data: dict = None,
        base_url: str = "",
        site_url: str = "",
        **kwargs,
    ):
        initial_data = default_dict(initial_data)
        super().__init__(initial_data, **kwargs)
        self.base_url = base_url
        self.site_url = site_url

    def url(self, *name: List[str], prod: bool = False) -> str:
        """
        Takes as input the slug of a page and returns its absolute url.

        If prod is set to True it uses the website base url even in draft mode
        """
        base_url = self.site_url if prod else self.base_url
        name = ".".join(name)
        if not name:
            return ""
        if name in self.keys():
            return base_url + self[name]["url"]
        if name + ".1" in self.keys():
            return base_url + self[name + ".1"]["url"]
        if "http" in name:
            return name
        if "/" in name:
            return base_url + name
        print(f'Invalid url: "{name}"')
        return ""


def paginate(
    objects: list,
    per_page: int,
    template: str,
    base_url: str,
    slug: str,
    renderer: str,
    additional_data: dict = None,
) -> dict:
    """Splits objects and for each group create an entry in the site map."""
    additional_data = default_dict(additional_data)
    urls = {}
    paginated_objects = [
        objects[x * per_page : (x + 1) * per_page]
        for x in range(max(math.ceil(len(objects) / per_page), 1))
    ]
    for i, objs in enumerate(paginated_objects, 1):
        if i > 1:
            previous_page = f"{slug}.{i-1}"
        else:
            previous_page = ""

        if i < len(paginated_objects):
            next_page = f"{slug}.{i+1}"
        else:
            next_page = ""

        paginator = {
            "objects": objs,
            "index": i,
            "next_page": next_page,
            "previous_page": previous_page,
        }
        data = {"paginator": paginator}
        data.update(additional_data)
        urls[f"{slug}.{i}"] = {
            "url": base_url + f"{i}/" if i > 1 else base_url,
            "data": data,
            "template": template,
            "renderer": renderer,
        }
    return urls


def date_to_string(date: datetime) -> str:
    """Formats a date to be displayed."""
    return date.strftime("%b %d, %Y")


def id_from_path(base_dir: Path, path: Path) -> str:
    """Return the identifier of a page from its relative filepath."""
    path = path.relative_to(base_dir)
    idx = ".".join(path.parts)[: -len(path.suffix)]
    return idx


def merge_dicts(a: dict, b: dict) -> dict:
    """Merge two dicts."""
    c = a.__class__()
    for key in a.keys():
        c[key] = a[key]
    for key in b.keys():
        if key not in a:
            c[key] = b[key]
        else:
            if isinstance(b[key], dict):
                if isinstance(a[key], dict):
                    c[key] = merge_dicts(a[key], b[key])
                else:
                    raise ValueError
    return c


def str_to_bool(x: str) -> (bool, int):
    """Convert strings to boolean."""
    if x in ("y", "yes", "t", "true", "on", "1"):
        return True, 0
    if x in ("n", "no", "f", "false", "off", "0"):
        return False, 0
    return False, 1


def default_list(val, default=None):
    """Returns a default list if input the is None."""
    if val:
        return val
    if default:
        return default
    return []


def default_dict(val, default=None):
    """Returns a default dict if the input is None."""
    if val:
        return val
    if default:
        return default
    return {}
