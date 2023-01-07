from subprocess import CompletedProcess
from unittest.mock import patch

from nordvpn import ConnectionStatus, NordVpn, Protocols, SettingsNames, Technologies


@patch("nordvpn.nordvpn.run")
def test_connect(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="You are connected to United Kingdom #2462 (uk2462.nordvpn.com)!",
    )
    assert NordVpn().connect() is True
    mock_run.assert_called_once_with(
        "nordvpn connect".split(), capture_output=True, text=True, check=True
    )


@patch("nordvpn.nordvpn.run")
def test_connect_fail(mock_run):
    mock_run.return_value = CompletedProcess(args=[], returncode=1, stdout="Error")
    assert NordVpn().connect() is False
    mock_run.assert_called_once_with(
        "nordvpn connect".split(), capture_output=True, text=True, check=True
    )


@patch("nordvpn.nordvpn.run")
def test_connect_to_country(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="You are connected to United Kingdom #2462 (uk2462.nordvpn.com)!",
    )
    assert NordVpn().connect_to_country("Birmania") is True
    mock_run.assert_called_once_with(
        "nordvpn connect Birmania".split(), capture_output=True, text=True, check=True
    )


@patch("nordvpn.nordvpn.run")
def test_connect_to_country_fail(mock_run):
    mock_run.return_value = CompletedProcess(args=[], returncode=1, stdout="Error")
    assert NordVpn().connect_to_country("Birmania") is False
    mock_run.assert_called_once_with(
        "nordvpn connect Birmania".split(), capture_output=True, text=True, check=True
    )


@patch("nordvpn.nordvpn.run")
def test_connect_to_group(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="You are connected to United Kingdom #2462 (uk2462.nordvpn.com)!",
    )
    assert NordVpn().connect_to_group("secret_group") is True
    mock_run.assert_called_once_with(
        "nordvpn connect secret_group".split(),
        capture_output=True,
        text=True,
        check=True,
    )


@patch("nordvpn.nordvpn.run")
def test_connect_to_group_fail(mock_run):
    mock_run.return_value = CompletedProcess(args=[], returncode=1, stdout="Error")
    assert NordVpn().connect_to_group("secret_group") is False
    mock_run.assert_called_once_with(
        "nordvpn connect secret_group".split(),
        capture_output=True,
        text=True,
        check=True,
    )


@patch("nordvpn.nordvpn.run")
def test_connect_to_city(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="You are connected to United Kingdom #2462 (uk2462.nordvpn.com)!",
    )
    assert NordVpn().connect_to_city("Tortona") is True
    mock_run.assert_called_once_with(
        "nordvpn connect Tortona".split(), capture_output=True, text=True, check=True
    )


@patch("nordvpn.nordvpn.run")
def test_connect_to_city_fail(mock_run):
    mock_run.return_value = CompletedProcess(args=[], returncode=1, stdout="Error")
    assert NordVpn().connect_to_city("Tortona") is False
    mock_run.assert_called_once_with(
        "nordvpn connect Tortona".split(), capture_output=True, text=True, check=True
    )


@patch("nordvpn.nordvpn.run")
def test_disconnect(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="You are disconnected from NordVPN",
    )
    assert NordVpn().disconnect() is True
    mock_run.assert_called_once_with(
        "nordvpn disconnect".split(), capture_output=True, text=True, check=True
    )


@patch("nordvpn.nordvpn.run")
def test_disconnect_fail(mock_run):
    mock_run.return_value = CompletedProcess(args=[], returncode=1, stdout="Error")
    assert NordVpn().disconnect() is False
    mock_run.assert_called_once_with(
        "nordvpn disconnect".split(), capture_output=True, text=True, check=True
    )


@patch("nordvpn.nordvpn.run")
def test_get_status_disconnected(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="Status: Disconnected",
    )
    status = NordVpn().get_status()
    mock_run.assert_called_once_with(
        "nordvpn status".split(), capture_output=True, text=True, check=True
    )
    assert status is not None
    assert status.status == ConnectionStatus.DISCONNECTED
    assert status.current_server is None
    assert status.country is None
    assert status.city is None
    assert status.ip is None
    assert status.protocol is None
    assert status.technology is None
    assert status.transfer is None
    assert status.uptime is None


@patch("nordvpn.nordvpn.run")
def test_get_status_connecting(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="Status: Connecting",
    )
    status = NordVpn().get_status()
    mock_run.assert_called_once_with(
        "nordvpn status".split(), capture_output=True, text=True, check=True
    )
    assert status is not None
    assert status.status == ConnectionStatus.CONNECTING
    assert status.current_server is None
    assert status.country is None
    assert status.city is None
    assert status.ip is None
    assert status.protocol is None
    assert status.technology is None
    assert status.transfer is None
    assert status.uptime is None


@patch("nordvpn.nordvpn.run")
def test_get_status_connected(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="""Status: Connected
Current server: aserver.nordvpn.com
Country: ACountry
City: ACity
Server IP: 1.1.1.1
Current technology: NORDLYNX
Current protocol: UDP
Transfer: 17.16 KiB received, 21.23 KiB sent
Uptime: 3 seconds""",
    )
    status = NordVpn().get_status()
    mock_run.assert_called_once_with(
        "nordvpn status".split(), capture_output=True, text=True, check=True
    )
    assert status is not None
    assert status.status == ConnectionStatus.CONNECTED
    assert status.current_server == "aserver.nordvpn.com"
    assert status.country == "ACountry"
    assert status.city == "ACity"
    assert status.ip == "1.1.1.1"
    assert status.protocol == "UDP"
    assert status.technology == "NORDLYNX"
    assert status.transfer == "17.16 KiB received, 21.23 KiB sent"
    assert status.uptime == "3 seconds"


@patch("nordvpn.nordvpn.run")
def test_get_status_connected_failed_parsing(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="""StatusWRONG: Connected
Current serverWRONG: aserver.nordvpn.com
CountryWRONG: ACountry
CityWRONG: ACity
Server IPWRONG: 1.1.1.1
Current technologyWRONG: NORDLYNX
Current protocolWRONG: UDP
TransferWRONG: 17.16 KiB received, 21.23 KiB sent
UptimeWRONG: 3 seconds""",
    )
    status = NordVpn().get_status()
    mock_run.assert_called_once_with(
        "nordvpn status".split(), capture_output=True, text=True, check=True
    )
    assert status is not None
    assert status.status == ConnectionStatus.DISCONNECTED
    assert status.current_server is None
    assert status.country is None
    assert status.city is None
    assert status.ip is None
    assert status.protocol is None
    assert status.technology is None
    assert status.transfer is None
    assert status.uptime is None


@patch("nordvpn.nordvpn.run")
def test_get_countries(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="""New feature - Meshnet! Link remote devices in Meshnet to connect to them directly over encrypted private tunnels, and route your traffic through another device. Use the `nordvpn meshnet --help` command to get started. Learn more: https://nordvpn.com/features/meshnet/
Albania			Estonia			Latvia			Slovakia
Argentina		Finland			Lithuania		Slovenia
Australia		France			Luxembourg		South_Africa
Austria			Georgia			Malaysia		South_Korea
Belgium			Germany			Mexico			Spain
Bosnia_And_Herzegovina	Greece			Moldova			Sweden
Brazil			Hong_Kong		Netherlands		Switzerland
Bulgaria		Hungary			New_Zealand		Taiwan
Canada			Iceland			North_Macedonia		Thailand
Chile			India			Norway			Turkey
Costa_Rica		Indonesia		Poland			Ukraine
Croatia			Ireland			Portugal		United_Kingdom
Cyprus			Israel			Romania			United_States
Czech_Republic		Italy			Serbia			Vietnam
Denmark			Japan			Singapore""",
    )
    countries = NordVpn().get_countries()
    mock_run.assert_called_once_with(
        "nordvpn countries".split(), capture_output=True, text=True, check=True
    )
    assert countries is not None
    assert len(countries) > 0
    assert countries[0] == "Albania"
    assert countries[-1] == "Vietnam"


@patch("nordvpn.nordvpn.run")
def test_get_groups(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="""New feature - Meshnet! Link remote devices in Meshnet to connect to them directly over encrypted private tunnels, and route your traffic through another device. Use the `nordvpn meshnet --help` command to get started. Learn more: https://nordvpn.com/features/meshnet/
Africa_The_Middle_East_And_India	Onion_Over_VPN
Asia_Pacific				P2P
Double_VPN				Standard_VPN_Servers
Europe					The_Americas
""",
    )
    groups = NordVpn().get_groups()
    mock_run.assert_called_once_with(
        "nordvpn groups".split(), capture_output=True, text=True, check=True
    )
    assert groups is not None
    assert len(groups) > 0
    assert groups[0] == "Africa_The_Middle_East_And_India"
    assert groups[-1] == "The_Americas"


@patch("nordvpn.nordvpn.run")
def test_get_cities(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="""New feature - Meshnet! Link remote devices in Meshnet to connect to them directly over encrypted private tunnels, and route your traffic through another device. Use the `nordvpn meshnet --help` command to get started. Learn more: https://nordvpn.com/features/meshnet/
London		Manchester""",
    )
    cities = NordVpn().get_cities("United_Kingdom")
    mock_run.assert_called_once_with(
        "nordvpn cities United_Kingdom".split(),
        capture_output=True,
        text=True,
        check=True,
    )
    assert cities is not None
    assert len(cities) > 0
    assert cities[0] == "London"
    assert cities[1] == "Manchester"


@patch("nordvpn.nordvpn.run")
def test_get_settings(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="""Technology: NORDLYNX
Firewall: enabled
Kill Switch: disabled
CyberSec: enabled
Notify: disabled
Auto-connect: disabled
IPv6: disabled
DNS: disabled
Whitelisted subnets:
    192.168.0.0/24,172.16.0.0/16
""",
    )
    settings = NordVpn().get_settings()
    mock_run.assert_called_once_with(
        "nordvpn settings".split(),
        capture_output=True,
        text=True,
        check=True,
    )
    assert settings is not None
    assert settings.technology == Technologies.NORDLYNX
    assert settings.firewall is True
    assert settings.kill_swith is False
    assert settings.cybersec is True
    assert settings.notify is False
    assert settings.notify is False
    assert settings.ipv6 is False
    assert settings.dns is False
    assert len(settings.whitelisted_subnets) == 2
    assert settings.whitelisted_subnets[0] == "192.168.0.0/24"
    assert settings.whitelisted_subnets[1] == "172.16.0.0/16"


@patch("nordvpn.nordvpn.run")
def test_set_technology_openvpn(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="Technology is successfully set to 'OPENVPN'.",
    )
    result = NordVpn().set_technology(Technologies.OPENVPN)
    mock_run.assert_called_once_with(
        "nordvpn set technology openvpn".split(),
        capture_output=True,
        text=True,
        check=True,
    )
    assert result


@patch("nordvpn.nordvpn.run")
def test_set_technology_nordlynx(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="Technology is successfully set to 'NORDLYNX'.",
    )
    result = NordVpn().set_technology(Technologies.NORDLYNX)
    mock_run.assert_called_once_with(
        "nordvpn set technology nordlynx".split(),
        capture_output=True,
        text=True,
        check=True,
    )
    assert result


@patch("nordvpn.nordvpn.run")
def test_set_technology_fail(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="The command you entered is not valid.",
    )
    result = NordVpn().set_technology(Technologies.OPENVPN)
    mock_run.assert_called_once_with(
        "nordvpn set technology openvpn".split(),
        capture_output=True,
        text=True,
        check=True,
    )
    assert result is False


@patch("nordvpn.nordvpn.run")
def test_set_firewall(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="Firewall is set to 'enabled' successfully.",
    )
    result = NordVpn().set_firewall(True)
    mock_run.assert_called_once_with(
        "nordvpn set firewall on".split(),
        capture_output=True,
        text=True,
        check=True,
    )
    assert result


@patch("nordvpn.nordvpn.run")
def test_set_firewall_off(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="Firewall is set to 'disabled' successfully.",
    )
    result = NordVpn().set_firewall(False)
    mock_run.assert_called_once_with(
        "nordvpn set firewall off".split(),
        capture_output=True,
        text=True,
        check=True,
    )
    assert result


@patch("nordvpn.nordvpn.run")
def test_set_firewall_fail(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="The command you entered is not valid.",
    )
    result = NordVpn().set_firewall(True)
    mock_run.assert_called_once_with(
        "nordvpn set firewall on".split(),
        capture_output=True,
        text=True,
        check=True,
    )
    assert result is False


@patch("nordvpn.nordvpn.run")
def test_set_kill_switch(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="Kill Switch is set to 'enabled' successfully.",
    )
    result = NordVpn().set_kill_switch(True)
    mock_run.assert_called_once_with(
        "nordvpn set killswitch on".split(),
        capture_output=True,
        text=True,
        check=True,
    )
    assert result


@patch("nordvpn.nordvpn.run")
def test_set_kill_switch_off(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="Kill Switch is set to 'disabled' successfully.",
    )
    result = NordVpn().set_kill_switch(False)
    mock_run.assert_called_once_with(
        "nordvpn set killswitch off".split(),
        capture_output=True,
        text=True,
        check=True,
    )
    assert result


@patch("nordvpn.nordvpn.run")
def test_set_kill_switch_fail(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="The command you entered is not valid.",
    )
    result = NordVpn().set_kill_switch(True)
    mock_run.assert_called_once_with(
        "nordvpn set killswitch on".split(),
        capture_output=True,
        text=True,
        check=True,
    )
    assert result is False


@patch("nordvpn.nordvpn.run")
def test_set_cybersec(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="Cybersec is set to 'enabled' successfully.",
    )
    result = NordVpn().set_cybersec(True)
    mock_run.assert_called_once_with(
        "nordvpn set cybersec on".split(),
        capture_output=True,
        text=True,
        check=True,
    )
    assert result


@patch("nordvpn.nordvpn.run")
def test_set_cybersec_off(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="Cybersec is set to 'disabled' successfully.",
    )
    result = NordVpn().set_cybersec(False)
    mock_run.assert_called_once_with(
        "nordvpn set cybersec off".split(),
        capture_output=True,
        text=True,
        check=True,
    )
    assert result


@patch("nordvpn.nordvpn.run")
def test_set_cybersec_fail(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="The command you entered is not valid.",
    )
    result = NordVpn().set_cybersec(True)
    mock_run.assert_called_once_with(
        "nordvpn set cybersec on".split(),
        capture_output=True,
        text=True,
        check=True,
    )
    assert result is False


@patch("nordvpn.nordvpn.run")
def test_set_notify(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="Notifications are set to 'enabled' successfully.",
    )
    result = NordVpn().set_notify(True)
    mock_run.assert_called_once_with(
        "nordvpn set notify on".split(),
        capture_output=True,
        text=True,
        check=True,
    )
    assert result


@patch("nordvpn.nordvpn.run")
def test_set_notify_fail(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="The command you entered is not valid.",
    )
    result = NordVpn().set_notify(True)
    mock_run.assert_called_once_with(
        "nordvpn set notify on".split(),
        capture_output=True,
        text=True,
        check=True,
    )
    assert result is False


@patch("nordvpn.nordvpn.run")
def test_set_notify_off(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="Notifications are set to 'disabled' successfully.",
    )
    result = NordVpn().set_notify(False)
    mock_run.assert_called_once_with(
        "nordvpn set notify off".split(),
        capture_output=True,
        text=True,
        check=True,
    )
    assert result


@patch("nordvpn.nordvpn.run")
def test_set_auto_connect(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="Auto-connect is set to 'enabled' successfully.",
    )
    result = NordVpn().set_auto_connect(True)
    mock_run.assert_called_once_with(
        "nordvpn set autoconnect on".split(),
        capture_output=True,
        text=True,
        check=True,
    )
    assert result


@patch("nordvpn.nordvpn.run")
def test_set_auto_connect_off(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="Auto-connect is set to 'disabled' successfully.",
    )
    result = NordVpn().set_auto_connect(False)
    mock_run.assert_called_once_with(
        "nordvpn set autoconnect off".split(),
        capture_output=True,
        text=True,
        check=True,
    )
    assert result


@patch("nordvpn.nordvpn.run")
def test_set_auto_connect_with_args(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="Auto-connect is set to 'enabled' successfully.",
    )
    result = NordVpn().set_auto_connect(True, "anOption")
    mock_run.assert_called_once_with(
        "nordvpn set autoconnect on anOption".split(),
        capture_output=True,
        text=True,
        check=True,
    )
    assert result


@patch("nordvpn.nordvpn.run")
def test_set_auto_connect_fail(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="The command you entered is not valid.",
    )
    result = NordVpn().set_auto_connect(True)
    mock_run.assert_called_once_with(
        "nordvpn set autoconnect on".split(),
        capture_output=True,
        text=True,
        check=True,
    )
    assert result is False


@patch("nordvpn.nordvpn.run")
def test_set_ipv6(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="Ipv6 is set to 'enabled' successfully.",
    )
    result = NordVpn().set_ipv6(True)
    mock_run.assert_called_once_with(
        "nordvpn set ipv6 on".split(),
        capture_output=True,
        text=True,
        check=True,
    )
    assert result


@patch("nordvpn.nordvpn.run")
def test_set_ipv6_off(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="Ipv6 is set to 'disabled' successfully.",
    )
    result = NordVpn().set_ipv6(False)
    mock_run.assert_called_once_with(
        "nordvpn set ipv6 off".split(),
        capture_output=True,
        text=True,
        check=True,
    )
    assert result


@patch("nordvpn.nordvpn.run")
def test_set_ipv6_fail(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="The command you entered is not valid.",
    )
    result = NordVpn().set_ipv6(True)
    mock_run.assert_called_once_with(
        "nordvpn set ipv6 on".split(),
        capture_output=True,
        text=True,
        check=True,
    )
    assert result is False


@patch("nordvpn.nordvpn.run")
def test_settings_help_message(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="""nordvpn set ipv6
Usage: nordvpn set ipv6 [command options] [enabled]/[disabled]

Use this command to enable or disable ipv6.

Supported values for [disabled]: 0, false, disable, off, disabled
Example: nordvpn set ipv6 off

Supported values for [enabled]: 1, true, enable, on, enabled
Example: nordvpn set ipv6 on

Options:
   --help, -h  show help (default: false)""",
    )
    message = NordVpn().get_settings_help_message(SettingsNames.IPV6)
    mock_run.assert_called_once_with(
        "nordvpn set ipv6 --help".split(),
        capture_output=True,
        text=True,
        check=True,
    )
    assert message == mock_run.return_value.stdout


@patch("nordvpn.nordvpn.run")
def test_set_dns(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="""Disabling CyberSec.
DNS is set to '1.1.1.1, 2.2.2.2, 3.3.3.3' successfully.""",
    )
    result = NordVpn().set_dns(True, ["1.1.1.1", "2.2.2.2", "3.3.3.3"])
    mock_run.assert_called_once_with(
        "nordvpn set dns 1.1.1.1 2.2.2.2 3.3.3.3".split(),
        capture_output=True,
        text=True,
        check=True,
    )
    assert result


@patch("nordvpn.nordvpn.run")
def test_set_dns_off(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="DNS is set to 'disabled' successfully.",
    )
    result = NordVpn().set_dns(False)
    mock_run.assert_called_once_with(
        "nordvpn set dns off".split(),
        capture_output=True,
        text=True,
        check=True,
    )
    assert result


@patch("nordvpn.nordvpn.run")
def test_set_dns_fail(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="The command you entered is not valid.",
    )
    result = NordVpn().set_dns(True, ["1.1.1.1"])
    mock_run.assert_called_once_with(
        "nordvpn set dns 1.1.1.1".split(),
        capture_output=True,
        text=True,
        check=True,
    )
    assert result is False


@patch("nordvpn.nordvpn.run")
def test_add_whitelisted_subnet(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="""Subnet 192.168.0.0/16 is whitelisted successfully.""",
    )
    result = NordVpn().add_whitelisted_subnet("192.168.0.0/16")
    mock_run.assert_called_once_with(
        "nordvpn whitelist add subnet 192.168.0.0/16".split(),
        capture_output=True,
        text=True,
        check=True,
    )
    assert result


@patch("nordvpn.nordvpn.run")
def test_add_whitelisted_subnet_fail(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="The command you entered is not valid.",
    )
    result = NordVpn().add_whitelisted_subnet("192.168.0.0/16")
    mock_run.assert_called_once_with(
        "nordvpn whitelist add subnet 192.168.0.0/16".split(),
        capture_output=True,
        text=True,
        check=True,
    )
    assert result is False


@patch("nordvpn.nordvpn.run")
def test_remove_whitelisted_subnet(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="""Subnet 192.168.0.0/16 is removed successfully.""",
    )
    result = NordVpn().remove_whitelisted_subnet("192.168.0.0/16")
    mock_run.assert_called_once_with(
        "nordvpn whitelist remove subnet 192.168.0.0/16".split(),
        capture_output=True,
        text=True,
        check=True,
    )
    assert result


@patch("nordvpn.nordvpn.run")
def test_add_whitelisted_port(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="""Port 1234 is whitelisted successfully.""",
    )
    result = NordVpn().add_whitelisted_port("1234")
    mock_run.assert_called_once_with(
        "nordvpn whitelist add port 1234".split(),
        capture_output=True,
        text=True,
        check=True,
    )
    assert result


@patch("nordvpn.nordvpn.run")
def test_add_whitelisted_port_fail(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="The command you entered is not valid.",
    )
    result = NordVpn().add_whitelisted_port("1234")
    mock_run.assert_called_once_with(
        "nordvpn whitelist add port 1234".split(),
        capture_output=True,
        text=True,
        check=True,
    )
    assert result is False


@patch("nordvpn.nordvpn.run")
def test_remove_whitelisted_port(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="""Port 1234 is removed successfully.""",
    )
    result = NordVpn().remove_whitelisted_port("1234")
    mock_run.assert_called_once_with(
        "nordvpn whitelist remove port 1234".split(),
        capture_output=True,
        text=True,
        check=True,
    )
    assert result


@patch("nordvpn.nordvpn.run")
def test_add_whitelisted_port_protocol(mock_run):
    mock_run.return_value = CompletedProcess(
        args=[],
        returncode=0,
        stdout="""Port 1234 TCP is whitelisted successfully.""",
    )
    result = NordVpn().add_whitelisted_port("1234", Protocols.TCP)
    mock_run.assert_called_once_with(
        "nordvpn whitelist add port 1234 TCP".split(),
        capture_output=True,
        text=True,
        check=True,
    )
    assert result
