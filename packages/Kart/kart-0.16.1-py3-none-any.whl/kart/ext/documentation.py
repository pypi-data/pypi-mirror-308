import importlib
import inspect
import os
from pathlib import Path

import mistune
from jinja2 import pass_context
from jinja2.runtime import Context
from mistune.directives import DirectivePlugin, FencedDirective, Include, RSTDirective
from slugify import slugify
from watchfiles import awatch

from kart.ext.markdown import KartMistuneRenderer, TocRenderer
from kart.mappers import Mapper
from kart.miners import DefaultMarkupMiner
from kart.utils import KartDict

try:
    from yaml import CSafeLoader as YamlLoader
except ImportError:
    from yaml import SafeLoader as YamlLoader


class DefaultDocumentationMiner(DefaultMarkupMiner):
    """Miner that recursively looks for data in the ``docs`` folder."""

    def __init__(self, directory: str = "docs"):
        """Initializes miner.

        Sets the ``dir`` variables.
        """
        self.dir = Path(directory)
        self.markdown_data = {}
        self.docs_global_toc = []

    def __recursive_read_data(self, config: dict, path: Path, level: int = 0):
        """Helper function."""
        if path.joinpath("navigation.yml").exists():
            nav_file = path.joinpath("navigation.yml").open()
            nav_data = YamlLoader(nav_file.read()).get_data()
            paths = []
            for x in nav_data:
                if "page" in x.keys():
                    paths.append(path.joinpath(x["page"]))
                elif "section" in x.keys():
                    paths.append(path.joinpath(x["section"]))
        else:
            paths = path.iterdir()
            nav_data = []

        for i, item in enumerate(paths):
            if item.is_file():
                obj = self.collect_single_file(item, config)
                slug, page = list(obj.items())[0]
                toc_entry = {"title": page["title"], "slug": slug, "level": level}
                self.docs_global_toc.append(toc_entry)
                if obj:
                    self.markdown_data.update(obj)
            elif item.is_dir():
                toc_entry = {"title": nav_data[i]["name"], "slug": None, "level": level}
                self.docs_global_toc.append(toc_entry)
                self.__recursive_read_data(config, item, level + 1)

    def read_data(self, config: dict):
        self.markdown_data = KartDict()
        self.docs_global_toc = []
        self.__recursive_read_data(config, self.dir)

    def collect(self, config: dict):
        return {"docs": self.markdown_data, "docs_global_toc": self.docs_global_toc}

    def start_watching(self, config: dict, callback):
        """Returns a function that calls read_data() when a file has changed."""

        self.read_data(config)

        async def watch():
            async for _ in awatch(self.dir, recursive=True):
                self.read_data(config)
                await callback()

        self.read_data(config)
        return watch


class DefaultDocumentationMapper(Mapper):
    """Mapper intended to be used with DefaultDocumentationMapper."""

    def __init__(self, template: str = "page.html", base_url: str = ""):
        self.template = template
        self.base_url = base_url

    def map(self, config: dict, site: KartDict) -> dict:
        urls = {}
        previous_slug = None
        for slug, page in site["docs"].items():
            if "url" in page:
                url = page["url"]
            elif slug == "index":
                url = "/"
            else:
                url = "/" + "/".join(slugify(part) for part in slug.split(".")) + "/"
            if "template" in page:
                template = page["template"]
            else:
                template = self.template
            if len(urls):
                page["previous_page"] = previous_slug
                urls[previous_slug]["data"]["next_page"] = slug
            previous_slug = slug
            map_page = {
                "url": self.base_url + url,
                "data": {**page},
                "template": template,
                "renderer": "default_site_renderer",
            }
            urls[slug] = map_page
        return urls


class DocumentationDirective(DirectivePlugin):
    """Mistune class that add the ``function`` and ``class`` directive to build a techical documentation."""

    def parse(self, block, m, state):
        name = self.parse_type(m)
        loc = self.parse_title(m)
        children = self.parse_tokens(block, self.parse_content(m), state)
        return {"type": f"doc_{name}", "children": children, "attrs": {"loc": loc}}

    def render_html_function(self, renderer, text, loc):
        """Renders the ``function`` directive."""
        module_name = ".".join(loc.split(".")[:-1])
        func_name = loc.split(".")[-1]
        module = importlib.import_module(module_name)
        module = importlib.reload(module)
        func = module.__dict__[func_name]
        sig = inspect.signature(func)
        html = "<dl>"
        html += f'<dt id="{loc}">function {loc}{sig}</dt>'
        html += f"<dd><p>{func.__doc__}</p></dd>"
        html += "</dl>"
        return html

    def render_html_class(self, renderer, text, loc):
        """Renders the ``class`` directive."""
        module_name = ".".join(loc.split(".")[:-1])
        func_name = loc.split(".")[-1]
        module = importlib.import_module(module_name)
        module = importlib.reload(module)
        cls = module.__dict__[func_name]
        parents = []
        for p in cls.__bases__:
            parents.append(p.__module__ + "." + p.__name__)
        html = "<dl>"
        html += f'<dt id="{loc}">class {loc}({", ".join(parents)})</dt>'
        html += f"<dd><p>{cls.__doc__}</p></dd>"
        functions = []
        for x in inspect.getmembers(cls):
            try:
                if x[1].__module__ != module_name:
                    continue
                if x[1].__qualname__.split(".")[0] != cls.__name__:
                    continue
            except Exception:
                continue
            functions.append(cls.__dict__[x[0]])
        if functions:
            html += "<dl>"
        for func in functions:
            sig = inspect.signature(func)
            if inspect.isabstract(cls) and func.__name__ in cls.__abstractmethods__:
                html += "<dt>@abstractmethod</dt>"
            html += f"<dt>{func.__name__}{sig}</dt>"
            if inspect.getdoc(func):
                html += f"<dd><p>{inspect.getdoc(func)}</p></dd>"
        if functions:
            html += "</dl>"

        html += "</dl>"
        return html

    def render_ast(self, children, name, title=None):
        return {"type": name, "children": children, "name": name, "title": title}

    def __call__(self, directive, md):
        for name in ("function", "class"):
            directive.register(name, self.parse)

        if md.renderer.NAME == "html":
            md.renderer.register("doc_function", self.render_html_function)
            md.renderer.register("doc_class", self.render_html_class)
        elif md.renderer.NAME == "ast":
            md.renderer.register("function", self.render_ast)
            md.renderer.register("class", self.render_ast)


@pass_context
def markdown_to_html(context: Context, content: str) -> str:
    """Converts markdown data to html.

    It supports markdown directives to extract the documentation out of python
    docstrings.
    """
    directives = [DocumentationDirective(), Include()]
    markdown = mistune.create_markdown(
        renderer=KartMistuneRenderer(context=context, escape=False),
        plugins=[
            FencedDirective(directives),
            RSTDirective(directives),
        ],
    )
    state = markdown.block.state_cls()
    state.env["__file__"] = str(Path(os.getcwd()) / "placeholder")
    return markdown.parse(content, state)[0]


def markdown_to_toc(content: str) -> str:
    """Extracts a list of header from markdown data."""
    directives = [DocumentationDirective(), Include()]
    markdown = mistune.create_markdown(
        renderer=TocRenderer(),
        plugins=[
            FencedDirective(directives),
            RSTDirective(directives),
        ],
    )
    state = markdown.block.state_cls()
    state.env["__file__"] = str(Path(os.getcwd()) / "placeholder")
    return markdown.parse(content, state)[0]
