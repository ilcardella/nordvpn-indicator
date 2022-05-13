#!/usr/bin/env python3

from nordvpn import NordVpn
from nordvpn_indicator import Indicator


def main() -> None:
    _ = Indicator(NordVpn())


if __name__ == "__main__":
    main()
