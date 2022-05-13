from enum import Enum, unique
from typing import Optional

from nordvpn.utils import find_bool_value, find_list_value, find_string_value


@unique
class Technologies(Enum):
    NORDLYNX = "NORDLYNX"
    OPENVPN = "OpenVPN"


@unique
class Protocols(Enum):
    UDP = "UDP"
    TCP = "TCP"


@unique
class SettingsNames(Enum):
    TECHNOLOGY = "Technology"
    FIREWALL = "Firewall"
    KILL_SWITCH = "Kill Switch"
    CYBERSEC = "CyberSec"
    NOTIFY = "Notify"
    AUTO_CONNECT = "Auto-connect"
    IPV6 = "IPv6"
    DNS = "DNS"
    WHITELISTED_SUBNETS = "Whitelisted subnets"


class NordVpnSettings:
    """
    NordVpn Settings
    """

    technology: Optional[Technologies] = None
    firewall: Optional[bool] = None
    kill_swith: Optional[bool] = None
    cybersec: Optional[bool] = None
    notify: Optional[bool] = None
    auto_connect: Optional[bool] = None
    ipv6: Optional[bool] = None
    dns: Optional[bool] = None
    whitelisted_subnets: list[str] = []

    def __init__(self, raw_settings: str):
        try:
            self._parse_settings(raw_settings)
        except ValueError:
            return

    def _parse_settings(self, raw: str):
        """
        Parse the raw output of "nordvpn settings" command
        """
        self.technology = Technologies(
            find_string_value(SettingsNames.TECHNOLOGY.value, raw)
        )
        self.firewall = find_bool_value(SettingsNames.FIREWALL.value, raw)
        self.kill_swith = find_bool_value(SettingsNames.KILL_SWITCH.value, raw)
        self.cybersec = find_bool_value(SettingsNames.CYBERSEC.value, raw)
        self.notify = find_bool_value(SettingsNames.NOTIFY.value, raw)
        self.auto_connect = find_bool_value(SettingsNames.AUTO_CONNECT.value, raw)
        self.ipv6 = find_bool_value(SettingsNames.IPV6.value, raw)
        self.dns = find_bool_value(SettingsNames.DNS.value, raw)
        self.whitelisted_subnets = (
            find_list_value(SettingsNames.WHITELISTED_SUBNETS.value, raw) or []
        )
