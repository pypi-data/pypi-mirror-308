import random
import re
import string

from jupyterhub.handlers import default_handlers
from jupyterhub.handlers.pages import SpawnHandler
from jupyterhub.utils import url_path_join
from tornado import web
from tornado.httputil import url_concat

from ..orm.share import UserOptionsShares


class ShareUserOptionsSpawnHandler(SpawnHandler):
    async def _render_form(
        self,
        for_user,
        spawner_options_form,
        spawner_options_form_values,
        server_name="",
        message="",
    ):
        auth_state = await for_user.get_auth_state()
        share_url = self.request.uri
        _spawn_url = (
            re.sub("/share/user_options/[^/]+", "/spawn", share_url)
            .rstrip("/")
            .rstrip(server_name)
            .rstrip("/")
        )
        spawn_url = url_path_join(_spawn_url, for_user.name, server_name)
        return await self.render_template(
            "share.html",
            for_user=for_user,
            auth_state=auth_state,
            spawner_options_form=spawner_options_form,
            spawner_options_form_values=spawner_options_form_values,
            server_name=server_name,
            error_message=message,
            url=url_concat(spawn_url, {"_xsrf": self.xsrf_token.decode("ascii")}),
            spawner=for_user.spawner,
        )

    def generate_random_id(self):
        chars = string.ascii_lowercase
        all_chars = string.ascii_lowercase + string.digits

        # Start with a random lowercase letter
        result = random.choice(chars)

        # Add 31 more characters from lowercase letters and numbers
        result += "".join(random.choice(all_chars) for _ in range(31))

        return result

    @web.authenticated
    async def get(self, secret):
        user = self.current_user
        db_entry = UserOptionsShares.find_by_share_id(self.db, secret)
        spawner_options_form_values = {}
        if not db_entry:
            raise web.HTTPError(400, f"Unknown share id: {secret}")
        else:
            spawner_options_form_values = db_entry.user_options
        server_name = self.generate_random_id()
        dummy_spawner = user.get_spawner(server_name, replace_failed=True)
        spawner_options_form = await dummy_spawner.get_options_form()
        form = await self._render_form(
            user,
            spawner_options_form=spawner_options_form,
            spawner_options_form_values=spawner_options_form_values,
            server_name=server_name,
        )
        self.finish(form)


default_handlers.append((r"/share/user_options/([^/]+)", ShareUserOptionsSpawnHandler))
