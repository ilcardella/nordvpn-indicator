from os import path
from threading import Timer

import gi

from nordvpn import ConnectionStatus, NordVpn

gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")
from gi.repository import AppIndicator3, GLib, Gtk  # NOQA: E402


class Indicator:
    APPINDICATOR_ID = "nordvpn_indicator"
    STATUS_UPDATE_SECONDS = 5.0

    def __init__(self, nordvpn: NordVpn) -> None:
        self.nordvpn = nordvpn
        self.indicator = AppIndicator3.Indicator.new(
            self.APPINDICATOR_ID,
            self._get_icon_path(ConnectionStatus.CONNECTING),
            AppIndicator3.IndicatorCategory.SYSTEM_SERVICES,
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self._build_menu())

        self._update_indicator_status()

        # Start the UI main loop
        Gtk.main()

    def _get_icon_path(self, connection_status: ConnectionStatus) -> str:
        """
        Returns the icon filepath relative to the connection status
        """
        if connection_status == ConnectionStatus.CONNECTED:
            filename = "nordvpn_connected.png"
        elif connection_status == ConnectionStatus.DISCONNECTED:
            filename = "nordvpn_disconnected.png"
        else:
            filename = "nordvpn_warning.png"
        # TODO we might need to use importlib
        # importlib.resources.open_text("nordvpn", f"data/{filename}"))
        return f"{path.dirname(path.realpath(__file__))}/data/{filename}"

    def _build_menu(self):
        """
        Builds menu for the app indicator
        """
        main_menu = Gtk.Menu()

        # Create a Connect submenu
        menu_connect = Gtk.Menu()
        item_connect = Gtk.MenuItem(label="Connect")
        item_connect.set_submenu(menu_connect)
        main_menu.append(item_connect)

        # First item is to connect automatically
        item_connect_auto = Gtk.MenuItem(label="Auto")
        item_connect_auto.connect("activate", self._auto_connect_callback)
        menu_connect.append(item_connect_auto)

        # Second item is submenu to select the country
        countries = self.nordvpn.get_countries()
        countries_menu = Gtk.Menu()
        item_connect_country = Gtk.MenuItem(label="Countries")
        item_connect_country.set_submenu(countries_menu)
        for country in countries:
            item = Gtk.MenuItem(label=country)
            item.connect("activate", self._country_connect_callback)
            countries_menu.append(item)
        menu_connect.append(item_connect_country)

        # Next item is submenu to select a specific city
        cities_menu = Gtk.Menu()
        item_connect_city = Gtk.MenuItem(label="Cities")
        item_connect_city.set_submenu(cities_menu)
        for country in countries:
            # Draw the country as disabled
            item_country = Gtk.MenuItem(label=country)
            item_country.set_sensitive(False)
            cities_menu.append(item_country)
            # List the cities below
            cities = self.nordvpn.get_cities(country)
            for city in cities:
                item_city = Gtk.MenuItem(label=city)
                item_city.connect("activate", self._city_connect_callback)
                cities_menu.append(item_city)
        menu_connect.append(item_connect_city)

        # Next item is submenu to select a server group
        groups = self.nordvpn.get_groups()
        groups_menu = Gtk.Menu()
        item_connect_group = Gtk.MenuItem(label="Groups")
        item_connect_group.set_submenu(groups_menu)
        for g in groups:
            item = Gtk.MenuItem(label=g)
            item.connect("activate", self._group_connect_callback)
            groups_menu.append(item)
        menu_connect.append(item_connect_group)

        # Disconnect item
        item_disconnect = Gtk.MenuItem(label="Disconnect")
        item_disconnect.connect("activate", self._disconnect_callback)
        main_menu.append(item_disconnect)

        # Create a submenu for the connection status
        menu_status = Gtk.Menu()
        item_status = Gtk.MenuItem(label="Status")
        item_status.set_submenu(menu_status)
        main_menu.append(item_status)

        # Add a label to show the current status details
        self.status_label = Gtk.MenuItem(label="")
        menu_status.append(self.status_label)
        self.status_label.set_sensitive(False)

        # Define the Settings menu entry
        item_settings = Gtk.MenuItem(label="Settings...")
        item_settings.connect("activate", self._display_settings_window)
        main_menu.append(item_settings)

        item_quit = Gtk.MenuItem(label="Quit")
        item_quit.connect("activate", self._quit)
        main_menu.append(item_quit)

        main_menu.show_all()
        return main_menu

    def _quit(self, menu_item):
        """
        Close the application
        """
        self.timer.cancel()
        Gtk.main_quit()

    def _country_connect_callback(self, menu_item):
        """
        Callback function to handle the connection of a selected country
        """
        self.nordvpn.disconnect()
        self.nordvpn.connect_to_country(menu_item.get_label())

    def _auto_connect_callback(self, menu_item):
        """
        Callback to handle connection to an automatic server
        """
        self.nordvpn.disconnect()
        self.nordvpn.connect()

    def _disconnect_callback(self, menu_item):
        """Callback to handle the disconnect request"""
        self.nordvpn.disconnect()

    def _group_connect_callback(self, menu_item):
        """
        Callback to connect to a server group
        """
        self.nordvpn.disconnect()
        self.nordvpn.connect_to_group(menu_item.get_label())

    def _city_connect_callback(self, menu_item):
        """
        Callback to connet to a city server
        """
        self.nordvpn.disconnect()
        self.nordvpn.connect_to_city(menu_item.get_label())

    def _display_settings_window(self, menu_itme):
        """
        Display a new window showing the settings of the NordVPN client app
        """
        # TODO
        # window = SettingsWindow(self.nordvpn)
        # window.show_all()

    def _update_indicator_status(self):
        """Start a timer that gets the VPN status and updates the UI"""
        status = self.nordvpn.get_status()
        GLib.idle_add(self.status_label.set_label, status.to_string())
        GLib.idle_add(
            self.indicator.set_icon_full, self._get_icon_path(status.status), ""
        )
        self.timer = Timer(self.STATUS_UPDATE_SECONDS, self._update_indicator_status)
        self.timer.start()
