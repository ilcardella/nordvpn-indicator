#!/usr/bin/env python3

import signal

from nordvpn import NordVpn
from nordvpn_indicator import Indicator


def main() -> None:
    _ = Indicator(NordVpn())


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
