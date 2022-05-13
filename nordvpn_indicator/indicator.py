from nordvpn import NordVpn


class Indicator:
    def __init__(self, nordvpn: NordVpn) -> None:
        print(NordVpn().get_status().status.value)
