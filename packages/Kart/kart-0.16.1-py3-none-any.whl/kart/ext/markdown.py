from urllib.parse import urlparse

import mistune
from jinja2 import pass_context
from jinja2.runtime import Context
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.styles import get_style_by_name
from slugify import slugify


class KartMistuneRenderer(mistune.HTMLRenderer):
    """Custom mistune renderers used by markdown_to_html()."""

    def __init__(self, context, *args, **kwargs):
        self.context = context
        super().__init__(*args, **kwargs)

    def link(self, text, url, title=None):
        """Renders the ``link`` block."""
        if text is None:
            text = url
        parsed_url = urlparse(url)
        stripped_url = parsed_url._replace(params="", query="", fragment="")
        final_url = urlparse(self.context["url"](stripped_url.geturl()))
        url = final_url._replace(
            params=parsed_url.params,
            query=parsed_url.query,
            fragment=parsed_url.fragment,
        ).geturl()
        a = f'<a href="{url}"'
        if title:
            a += f' title="{mistune.scanner.escape_html(title)}"'
        a += f">{text}</a>"
        return a

    def block_code(self, text, info):
        """Renders the ``code`` block."""
        if not info:
            return f"<pre><code>{mistune.escape(text.strip())}</code></pre>\n"
        lang = info.split(None, 1)[0]
        lexer = get_lexer_by_name(lang, stripall=True)
        config = self.context["config"]["code_highlighting"]
        formatter = HtmlFormatter(
            wrapcode=True,
            style=get_style_by_name(config["style"]),
            noclasses=config["noclasses"],
            prestyles="color: #EEFFFF" if config["noclasses"] else "",
        )
        return highlight(text, lexer, formatter)

    def heading(self, text, level):
        """Renders the ``heading`` block."""
        return f"<h{level} id={slugify(text)}>{text}</h{level}>\n"


@pass_context
def markdown_to_html(context: Context, content: str) -> str:
    """Converts markdown data to html."""
    parsed_markdown = context.environment.from_string(content).render(context)
    return mistune.create_markdown(
        renderer=KartMistuneRenderer(context=context, escape=False),
        plugins=["strikethrough", "table", "task_lists"],
    )(parsed_markdown)


class TocRenderer(mistune.core.BaseRenderer):
    """Mistune renderer used by markdown_to_toc()."""

    def text(self, text):
        """Renders the ``text`` block."""
        return text

    def heading(self, children, level):
        """Renders the ``heading`` block."""
        return {"title": children, "id": slugify(children), "level": level}

    def render_token(self, token, state) -> str:
        try:
            func = self._get_method(token["type"])
        except AttributeError:
            return ""
        attrs = token.get("attrs", {})

        text = []
        if "raw" in token:
            text.append(token["raw"])
        elif "children" in token:
            text.append(self.render_tokens(token["children"], state))
        return func(*text, **attrs)

    def render_tokens(self, tokens, state) -> str:
        data = list(self.iter_tokens(tokens, state))
        if len(data) == 1:
            return data[0]
        return [x for x in data if x]


def markdown_to_toc(content: str) -> str:
    """Extracts a list of header from markdown data."""
    return mistune.Markdown(renderer=TocRenderer())(content)
