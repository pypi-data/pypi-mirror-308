import argparse
import asyncio
import fnmatch
import shutil
from pathlib import Path

from aiohttp import web

from kart.utils import KartMap, default_dict, default_list, merge_dicts


class Kart:
    """Main Kart class."""

    def __init__(
        self,
        miners: list = None,
        content_modifiers: list = None,
        mappers: list = None,
        map_modifiers: list = None,
        renderers: list = None,
        config: dict = None,
        build_location: str = "_site",
    ):
        self.miners = default_list(miners)
        self.content_modifiers = default_list(content_modifiers)
        self.mappers = default_list(mappers)
        self.map_modifiers = default_list(map_modifiers)
        self.renderers = default_list(renderers)
        self.config = default_dict(config)

        self.site = {}
        self.map = {}
        self.build_location = Path(build_location)

        self.served_urls = {}
        self.served_regexes = {}
        self.renderer_dict = {}
        self.ws = []

    def check_config(self):
        """Checks if the config has all the necessary fields and sets them to default values if not."""
        default = {
            "name": "Example",
            "site_url": "https://example.org",
            "base_url": "http://localhost:9000",
            "pagination": {"per_page": 5, "skip": 0},
            "code_highlighting": {"style": "default", "noclasses": True},
            "timezone": "UTC",
            "serving": False,
            "dev_server_port": 9000,
        }
        self.config = merge_dicts(self.config, default)

    def mine_data(self, start: bool = True):
        """Calls miners and content modifiers."""
        self.site = {}
        for miner in self.miners:
            if start:
                miner.read_data(self.config)
            self.site = merge_dicts(self.site, miner.collect(self.config))
        for modifier in self.content_modifiers:
            modifier.modify(self.config, self.site)

    def create_map(self):
        """Calls mappers and map modifiers."""
        self.map = KartMap(
            base_url=self.config["base_url"], site_url=self.config["site_url"]
        )
        for mapper in self.mappers:
            self.map.update(mapper.map(self.config, self.site))
        for modifier in self.map_modifiers:
            modifier.modify(self.config, self.site, self.map)

    def write(self):
        """Calls renderers."""
        for renderer in self.renderers:
            renderer.render(self.config, self.site, self.map, self.build_location)

    def build(self):
        """Build the entire site."""
        self.check_config()
        self.mine_data()
        self.create_map()
        shutil.rmtree(self.build_location, ignore_errors=True)
        self.build_location.mkdir(parents=True, exist_ok=True)
        self.write()

    def update_data(self):
        """Update the site data after a file has been changed."""
        self.mine_data(False)
        self.create_map()
        self.served_urls = {}
        self.served_regexes = {}
        for slug, page in self.map.items():
            self.served_urls[page["url"]] = slug
            if "*" in page["url"] or "?" in page["url"]:
                self.served_regexes[page["url"]] = slug

    async def ws_endpoint(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        self.ws.append(ws)
        try:
            async for _ in ws:
                pass
        finally:
            self.ws.remove(ws)
        return ws

    async def ws_reload(self):
        for ws in self.ws:
            await ws.send_str("reload")

    async def ws_on_shutdown(self, _):
        for ws in self.ws:
            await ws.close()

    async def js_reload(self, request):
        js_reload = (Path(__file__).parent / "js" / "hot_reload.js").read_text()
        return web.Response(text=js_reload, content_type="text/javascript")

    async def serve_page(self, request):
        """Serve a single page."""
        url = str(request.rel_url.path)
        if url in self.served_urls:
            page = self.map[self.served_urls[url]]
        else:
            try:
                pattern = next(
                    x for x in self.served_regexes if fnmatch.fnmatch(url, x)
                )
                page = self.map[self.served_regexes[pattern]]
            except StopIteration:
                page = None
        if page:
            renderer = self.renderer_dict[page["renderer"]]
            return await renderer.serve(request, page, self.config, self.site, self.map)

    def serve(self, port: int = 9000):
        """Main loop for serving the site."""

        self.check_config()

        async def changed_callback():
            self.update_data()
            await self.ws_reload()

        loop = asyncio.new_event_loop()
        for miner in self.miners:
            func = miner.start_watching(self.config, changed_callback)
            if func:
                loop.create_task(func())

        shutil.rmtree(self.build_location, ignore_errors=True)
        self.renderer_dict = {}
        for renderer in self.renderers:
            self.renderer_dict[renderer.name] = renderer
            renderer.start_serving(self.config)
        self.update_data()

        app = web.Application()
        app.on_shutdown.append(self.ws_on_shutdown)
        app.add_routes([web.get("/hot_reload", self.js_reload)])
        app.add_routes([web.get("/ws_hot_reload", self.ws_endpoint)])
        app.add_routes([web.get("/{tail:.*}", self.serve_page)])
        web.run_app(app, port=port, loop=loop, shutdown_timeout=0.1)

        for miner in self.miners:
            miner.stop_watching(self.config)
        for renderer in self.renderers:
            renderer.stop_serving(self.config)

    def run(self):
        """Starts the kart execution.

        See --help for more information
        """

        parser = argparse.ArgumentParser()
        parser.add_argument(
            "command", help="command to execute", choices={"build", "serve"}
        )
        parser.add_argument(
            "-p", "--port", help="port to bind to", default=None, type=int
        )
        parser.add_argument(
            "--url",
            help="specify website url",
            type=str,
        )
        parser.add_argument("-D", "--draft", help="draft mode", action="store_true")
        args = parser.parse_args()

        self.config["serving"] = args.command == "serve"
        self.config["draft_mode"] = args.draft
        if args.port:
            self.config["dev_server_port"] = args.port

        if self.config["serving"]:
            self.config["base_url"] = ""
        elif args.url:
            self.config["base_url"] = args.url
        else:
            self.config["base_url"] = self.config["site_url"]

        if args.command == "build":
            self.build()
        if args.command == "serve":
            self.serve(self.config["dev_server_port"])
