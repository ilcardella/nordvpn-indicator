from enum import Enum, unique
from typing import Optional

from nordvpn.utils import find_string_value


@unique
class ConnectionStatus(Enum):
    CONNECTED = "Connected"
    DISCONNECTED = "Disconnected"
    CONNECTING = "Connecting"


class NordVpnStatus:
    """
    NordVpn client application status
    """

    warnings: set[str] = set()
    status: ConnectionStatus = ConnectionStatus.DISCONNECTED
    current_server: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    ip: Optional[str] = None
    protocol: Optional[str] = None
    technology: Optional[str] = None
    transfer: Optional[str] = None
    uptime: Optional[str] = None

    @unique
    class Param(Enum):
        STATUS = "Status"
        CURRENT_SERVER = "Current server"
        COUNTRY = "Country"
        CITY = "City"
        IP = "Server IP"
        PROTOCOL = "Current protocol"
        TECHNOLOGY = "Current technology"
        TRANSFER = "Transfer"
        UPTIME = "Uptime"

    def __init__(self, raw_status: str):
        try:
            self._parse_raw_status(raw_status)
        except ValueError:
            return

    def _parse_raw_status(self, raw_status: str) -> None:
        self.status_as_string = raw_status

        self.status = ConnectionStatus(
            find_string_value(NordVpnStatus.Param.STATUS.value, raw_status)
        )
        if self.status == ConnectionStatus.CONNECTED:
            self.current_server = find_string_value(
                NordVpnStatus.Param.CURRENT_SERVER.value, raw_status
            )
            self.country = find_string_value(
                NordVpnStatus.Param.COUNTRY.value, raw_status
            )
            self.city = find_string_value(NordVpnStatus.Param.CITY.value, raw_status)
            self.ip = find_string_value(NordVpnStatus.Param.IP.value, raw_status)
            self.protocol = find_string_value(
                NordVpnStatus.Param.PROTOCOL.value, raw_status
            )
            self.technology = find_string_value(
                NordVpnStatus.Param.TECHNOLOGY.value, raw_status
            )
            self.transfer = find_string_value(
                NordVpnStatus.Param.TRANSFER.value, raw_status
            )
            self.uptime = find_string_value(
                NordVpnStatus.Param.UPTIME.value, raw_status
            )

    def to_string(self):
        return self.status_as_string.split("-")[-1].strip()
