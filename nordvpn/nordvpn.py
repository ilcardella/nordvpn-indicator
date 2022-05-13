from enum import Enum, unique
from subprocess import CalledProcessError, run
from typing import Optional

from nordvpn import (
    NordVpnSettings,
    NordVpnStatus,
    Protocols,
    SettingsNames,
    Technologies,
)
from nordvpn.utils import parse_words


class NordVpn:
    """
    NordVPN Client interface
    """

    @unique
    class Messages(Enum):
        UPDATE_WARNING = (
            "A new version of NordVpn is available! Please update the application."
        )
        LOGIN_WARNING = "Please enter your login details."
        CONNECT_SUCCESS = "You are connected to"
        DISCONNECT_SUCCESS = "You are disconnected from NordVPN"
        INVALID_COMMAND = "The command you entered is not valid."
        INVALID_CITIES_COMMAND = "Servers by city are not available for this country"

    def __init__(self):
        pass

    # Connection interfaces

    def connect(self) -> bool:
        """
        Connect with a NordVpn server
        """
        return self._run_nordvpn_connect_command()

    def connect_to_country(self, country: str) -> bool:
        """
        Connect to a NordVpn server in the specified country

        Args:
            country: Country name
        """
        return self._run_nordvpn_connect_command(country.replace(" ", "_"))

    def connect_to_group(self, group: str) -> bool:
        """
        Connect to a NordVpn server group
        """
        return self._run_nordvpn_connect_command(group.replace(" ", "_"))

    def connect_to_city(self, city: str) -> bool:
        """
        Connect to a specific NordVpn city server
        """
        return self._run_nordvpn_connect_command(city.replace(" ", "_"))

    def disconnect(self) -> bool:
        """
        Disconnect from the NordVpn server
        """
        output = self._run_nordvpn_command("disconnect")
        return self.Messages.DISCONNECT_SUCCESS.value in output

    # Getters and Setters interfaces

    def get_status(self) -> NordVpnStatus:
        """
        Returns the VPN connection status
        """
        output = self._run_nordvpn_command("status")
        return NordVpnStatus(output)

    def get_countries(self) -> list[str]:
        """
        Returns a list of string representing the available countries
        """
        raw_countries = self._run_nordvpn_command("countries")
        if raw_countries is None:
            return []
        countries = parse_words(raw_countries)
        countries.sort()
        return countries

    def get_groups(self) -> list[str]:
        """
        Returns a list of string representing the available groups
        """
        raw_groups = self._run_nordvpn_command("groups")
        if raw_groups is None:
            return []
        groups = parse_words(raw_groups)
        groups.sort()
        return groups

    def get_cities(self, country: str) -> list[str]:
        """
        Return the list of cities available for the specified country
        """
        raw_cities = self._run_nordvpn_command(f"cities {country}")
        if (
            raw_cities is None
            or NordVpn.Messages.INVALID_CITIES_COMMAND.value in raw_cities
        ):
            return []
        cities = parse_words(raw_cities)
        cities.sort()
        return cities

    def get_settings_help_message(self, setting: SettingsNames) -> str:
        """
        Returns the help message relative to the specified setting
        """
        formatted_setting = self._format_setting_name(setting.value.lower())
        return self._run_nordvpn_command(f"set {formatted_setting} --help")

    def get_settings(self) -> NordVpnSettings:
        """
        Return the current NordVpn settings
        """
        output = self._run_nordvpn_command("settings")
        return NordVpnSettings(output)

    def set_technology(self, technology: Technologies) -> bool:
        return self._run_nordvpn_set_command(
            SettingsNames.TECHNOLOGY, technology.value.lower()
        )

    def set_firewall(self, enable: bool) -> bool:
        return self._run_nordvpn_set_command(
            SettingsNames.FIREWALL, "on" if enable else "off"
        )

    def set_kill_switch(self, enable: bool) -> bool:
        return self._run_nordvpn_set_command(
            SettingsNames.KILL_SWITCH, "on" if enable else "off"
        )

    def set_cybersec(self, enable: bool) -> bool:
        return self._run_nordvpn_set_command(
            SettingsNames.CYBERSEC, "on" if enable else "off"
        )

    def set_notify(self, enable: bool) -> bool:
        return self._run_nordvpn_set_command(
            SettingsNames.NOTIFY, "on" if enable else "off"
        )

    def set_auto_connect(self, enable: bool, args: Optional[str] = None) -> bool:
        if enable and args is not None:
            return self._run_nordvpn_set_command(
                SettingsNames.AUTO_CONNECT, f"on {args}"
            )
        else:
            return self._run_nordvpn_set_command(
                SettingsNames.AUTO_CONNECT, "on" if enable else "off"
            )

    def set_ipv6(self, enable: bool) -> bool:
        return self._run_nordvpn_set_command(
            SettingsNames.IPV6, "on" if enable else "off"
        )

    def set_dns(self, enable: bool, servers: list[str] = []) -> bool:
        return self._run_nordvpn_set_command(
            SettingsNames.DNS, " ".join(servers) if enable else "off"
        )

    def add_whitelisted_subnet(self, subnet: str) -> bool:
        return self._run_nordvpn_whitelist_command(f"add subnet {subnet}")

    def remove_whitelisted_subnet(self, subnet: str) -> bool:
        return self._run_nordvpn_whitelist_command(f"remove subnet {subnet}")

    def add_whitelisted_port(
        self, port: str, protocol: Optional[Protocols] = None
    ) -> bool:
        command = f"add port {port}"
        if protocol:
            command += f" {protocol.value}"
        return self._run_nordvpn_whitelist_command(command)

    def remove_whitelisted_port(
        self, port: str, protocol: Optional[Protocols] = None
    ) -> bool:
        command = f"remove port {port}"
        if protocol:
            command += f" {protocol.value}"
        return self._run_nordvpn_whitelist_command(command)

    def _run_command(self, command: str) -> str:
        """
        Run a shell command and returns its output
        """
        output = "UNKNOWN ERROR"
        try:
            result = run(
                command.strip().split(), capture_output=True, text=True, check=True
            )
            output = result.stdout.strip()
        except CalledProcessError as e:
            output = e.output
        return output

    def _run_nordvpn_command(self, args: str) -> str:
        """
        Run a nordvpn command
        """
        return self._run_command(f"nordvpn {args}")

    def _run_nordvpn_connect_command(self, args: str = "") -> bool:
        """
        Run a nordvpn connect command and return True if successful
        """
        output = self._run_nordvpn_command(f"connect {args}")
        return self.Messages.CONNECT_SUCCESS.value in output

    def _run_nordvpn_set_command(self, setting: SettingsNames, args: str) -> bool:
        """
        Run a nordvpn set command and return True if successful
        """
        formatted_setting = self._format_setting_name(setting.value.lower())
        output = self._run_nordvpn_command(f"set {formatted_setting} {args}")
        return self.Messages.INVALID_COMMAND.value not in output

    def _run_nordvpn_whitelist_command(self, args: str) -> bool:
        """
        Run a nordvpn whitelist command and return True if successful
        """
        output = self._run_nordvpn_command(f"whitelist {args}")
        return self.Messages.INVALID_COMMAND.value not in output

    def _format_setting_name(self, setting_name: str) -> str:
        """
        Return the given setting name formatted for compatibility
        for "nordvpn set" command
        """
        return setting_name.replace(" ", "").replace("-", "").lower()
