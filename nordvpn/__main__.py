#!/usr/bin/env python3

from nordvpn import Indicator, NordVpn


def main() -> None:
    _ = Indicator(NordVpn())


if __name__ == "__main__":
    main()
