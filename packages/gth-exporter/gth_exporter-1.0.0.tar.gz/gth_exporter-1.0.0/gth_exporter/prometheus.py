import logging

import gi

gi.require_version("Soup", "3.0")

from gi.repository import Gio, GLib, Soup  # type: ignore

log = logging.getLogger(__name__)


from .metric import Gth


def to_prometheus(gth: Gth) -> str:
    return f"""
# TYPE govee_temperature_celsius gauge
govee_temperature_celsius{{alias="{gth.alias}", address="{gth.address}"}} {gth.temp_celsius}
# TYPE govee_humidity_percent gauge
govee_humidity_percent{{alias="{gth.alias}", address="{gth.address}"}} {gth.humidity_percent}
# TYPE govee_battery_percent gauge
govee_battery_percent{{alias="{gth.alias}", address="{gth.address}"}} {gth.battery_percent}
# TYPE govee_rssi_dbm gauge
# help Received Signal Strength Indicator
govee_rssi_dbm{{alias="{gth.alias}", address="{gth.address}"}} {gth.rssi}
"""


class PushGateway:
    url: str
    user: str | None
    password: str | None
    _session: Soup.Session

    def __init__(self, url: str, user: str | None = None, password: str | None = None):
        self.url = url
        self.user = user
        self.password = password
        self._session = Soup.Session()

        if log.getEffectiveLevel() == logging.DEBUG:
            logger = Soup.Logger.new(Soup.LoggerLogLevel.BODY)
            self._session.add_feature(logger)

    async def send_message(self, gth: Gth):
        uri = GLib.Uri.parse(self.url, GLib.UriFlags.NONE)
        message = Soup.Message.new_from_uri("POST", uri)
        assert self._session
        if self.user and self.password:
            auth_manager = self._session.get_feature(Soup.AuthManager)
            assert auth_manager
            auth = Soup.Auth.new(Soup.AuthBasic, message, "Basic")
            assert auth
            auth.authenticate(self.user, self.password)
            auth_manager.use_auth(message.get_uri(), auth)  # type: ignore

        body = to_prometheus(gth)

        message.set_request_body_from_bytes("application/x-www-form-urlencoded", GLib.Bytes.new(body.encode()))  # type: ignore

        resp_body = await self._session.send_and_read_async(message, GLib.PRIORITY_DEFAULT)  # type: ignore

        if (status := message.get_status()) != Soup.Status.OK:
            log.warning(f"Error Posting to '{self.url}': {Soup.Status.get_phrase(status)} -> {resp_body.get_data().decode()}")
