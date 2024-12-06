# Base templates for Omada Log Analysis

# Client Activity
conn_hw = (
    "{time} {hardware_controller}  {omada_time} {controller} - - - [client:{client_name_and_mac}] "
    "is connected to [{network_device_type}:{network_device}:{network_device_mac}] on {network} network."
)

conn_w = (
    "{time} {hardware_controller}  {omada_time} {controller} - - - [client:{client_name_and_mac}] "
    'is connected to [{network_device_type}:{network_device}:{network_device_mac}] with SSID "{ssid}" '
    "on channel {channel}."
)

blocked = (
    "{time} {hardware_controller}  {omada_time} {controller} - - - [client:{client_name_and_mac}] "
    "failed to connected to [{network_device_type}:{network_device}:{network_device_mac}] "
    'with SSID "{ssid}" on channel {channel} because the user '
    "is blocked by Access Control.({number} {discard_text})"
)

blocked_mac = ('{time} {hardware_controller}  {omada_time} {controller} - - - [client:{client_name_and_mac}]'
               ' failed to connect to [{network_device_type}:{network_device}:{network_device_mac}] with SSID "{ssid}" '
               'on channel {channel} because the user was blocked by MAC block/MAC Filter/Lock To AP.({number} {discard_text})')

disc_hw = (
    "{time} {hardware_controller}  {omada_time} {controller} - - - [client:{client_name_and_mac}] "
    'was disconnected from network "{network}" on [{network_device_type}:{network_device}:{network_device_mac}]'
    "(connected time:{connected_time} connected, traffic: {data})."
)

disc_w = (
    "{time} {hardware_controller}  {omada_time} {controller} - - - [client:{client_name_and_mac}] "
    'is disconnected from SSID "{ssid}" on [{network_device_type}:{network_device}:{network_device_mac}] '
    "({connected_time} connected, {data})."
)

roaming = (
    "{time} {hardware_controller}  {omada_time} {controller} - - - [client:{client_name_and_mac}] "
    "is roaming from [{network_device_type}:{network_device}:{network_device_mac}][{channel}] to "
    "[{roaming_network_device_type}:{roaming_network_device}:{roaming_network_device_mac}][{roaming_channel}] "
    "with SSID {roaming_ssid}"
)

disc_hw_recon = (
    "{time} {hardware_controller}  {omada_time} {controller} - - - [client:{client_name_and_mac}] "
    'was disconnected from network "{disc_network}" on '
    "[{network_device_type}:{network_device}:{network_device_mac}](connected time:{connected_time} "
    'connected, traffic: {data}) and connected to network "{recon_network}" on '
    "[{recon_network_device_type}:{recon_network_device}:{recon_network_device_mac}]."
)

disc_w_recon = (
    "{time} {hardware_controller}  {omada_time} {controller} - - - [client:{client_name_and_mac}] "
    'is disconnected from SSID "{disc_ssid}" on [{network_device_type}:{network_device}:{network_device_mac}] '
    '({connected_time} connected, {data}) and connected to SSID "{recon_ssid}" on '
    "[{recon_network_device_type}:{recon_network_device}:{recon_network_device_mac}]."
)

online_hw = (
    "{time} {hardware_controller}  {omada_time} {controller} - - - [client:{client_name_and_mac}] "
    "went online on [{network_device_type}:{network_device}:{network_device_mac}] on {network} network."
)

offline_hw = (
    "{time} {hardware_controller}  {omada_time} {controller} - - - [client:{client_name_and_mac}] "
    'went offline from network "{network}" on '
    "[{network_device_type}:{network_device}:{network_device_mac}](connected time:{connected_time} "
    "connected, traffic: {data})."
)

online_w = (
    "{time} {hardware_controller}  {omada_time} {controller} - - - [client:{client_name_and_mac}] "
    "(IP: {client_ip}, Username: {username} went online on "
    '[{network_device_type}:{network_device}:{network_device_mac}] with SSID "{ssid}" on channel {channel}.'
)

offline_w = (
    "{time} {hardware_controller}  {omada_time} {controller} - - - [client:{client_name_and_mac}] "
    '(IP: {client_ip}, Username: {username}) went offline from SSID "{ssid}" on '
    "[{network_device_type}:{network_device}:{network_device_mac}] ({connected_time} connected, {data})."
)

dhcp_assign = (
    "{time} {hardware_controller}  {omada_time} {controller} - - - "
    "DHCP Server allocated IP address {client_ip} for the client[MAC: {client_mac}].#015"
)

dhcp_reject = (
    "{time} {hardware_controller}  {omada_time} {controller} - - - DHCP Server rejected the request"
    " of the client[MAC: {client_mac} IP: {client_ip}].#015"
)

# Logins
login = (
    "{time} {hardware_controller}  {omada_time} {controller} - - - "
    "{user} logged in to the controller from {login_ip}."
)

failed_login = (
    "{time} {hardware_controller}  {omada_time} {controller} - - - "
    "{user} failed to log in to the controller from {login_ip}."
)

# Auto backup
auto_backup = (
    "{time} {hardware_controller}  {omada_time} {controller} - - - "
    "Auto Backup executed with generating file {filename}."
)

# Network device activity
device_connected = (
    "{time} {hardware_controller}  {omada_time} {controller} - - - "
    "[{network_device_type}:{network_device}:{network_device_mac}] was connected."
)

device_disconnected = (
    "{time} {hardware_controller}  {omada_time} {controller} - - - "
    "[{network_device_type}:{network_device}:{network_device_mac}] was disconnected."
)

dhcps = "{time} {hardware_controller}  {omada_time} {controller} - - - DHCPS initialization {result}.#015"

got_ip_address = (
    "{time} {hardware_controller}  {omada_time} {controller} - - - "
    "[{network_device_type}:{network_device}:{network_device_mac}] "
    "got IP address {ip_address}/{subnet_mask}."
)

online_detection = ("{time} {hardware_controller}  {omada_time} {controller} - - - "
                    "[{network_device_type}:{network_device}:{network_device_mac}]: "
                    "The online detection result of [{interface}] was {state}.#015")

up_or_down = (
    "{time} {hardware_controller}  {omada_time} {controller} - - - "
    "[{interface}] of [{network_device_type}:{network_device}:{network_device_mac}] is {state}.#015"
)

upgrade = ("{time} {hardware_controller}  {omada_time} {controller} - - - "
           "[{network_device_type}:{network_device}:{network_device_mac}] was upgrade to {result}")

# Dictionary of templates 'search_string' : [template, number_of_expected_values, event name]
# Some notes: use of the search string increases the speed of the parsing function
# Search string must be present in the event data for the parsing function to even attempt using a template
# Some search strings (ie: disconnected from SSID, connected to) will be present in multiple log event types
# In order to confirm that the correct template was used, its results will be tested for correct number of values
# The event name will be that value that populates the event_type column as the search string isn't terrific

client_activity_dict = {
    "is connected to": [conn_hw, 9, "hardwired_connection"],
    "connected to": [conn_w, 10, "wireless_connection"],

    "blocked by Access Control": [blocked, 12, "blocked"],
    "blocked by MAC": [blocked_mac, 12, "blocked"],

    "was disconnected from network": [disc_hw, 11, "hardwired_disconnect"],
    "is disconnected from SSID": [disc_w, 11, "wireless_disconnect"],

    "roaming": [roaming, 14, "roaming"],

    "disconnected from network": [disc_hw_recon, 15, "hardwired_reconnect"],
    "disconnected from SSID": [disc_w_recon, 15, "wireless_reconnect"],

    "went online": [online_hw, 9, "hardwired_online"],
    "went offline from network": [offline_hw, 11, "hardwired_offline"],

    "went online on": [online_w, 12, "wireless_online"],
    "went offline from SSID": [offline_w, 13, "wireless_offline"],

    "allocated IP address": [dhcp_assign, 6, "dhcp_assign"],
    "rejected the request": [dhcp_reject, 6, "dhcp_reject"],
}

logins_dict = {
    "logged in to": [login, 6, "login"],
    "failed to log in": [failed_login, 6, "failed_login"],
}

network_devices_activity_dict = {
    "was connected.": [device_connected, 7, "device_connected"],
    "was disconnected.": [device_disconnected, 7, "device_disconnected"],
    "DHCPS initialization": [dhcps, 5, "dhcps_initialization"],
    "] of [": [up_or_down, 9, "interface_up_or_down", ],  # This search string is pretty goofy, but it works
    "got IP address": [got_ip_address, 9, "device_dhcp_assign"],
    'online detection': [online_detection, 9, 'online_detection'],
    'upgrade': [upgrade, 8, 'upgrade'],

}

omada_template_dict = {
    **client_activity_dict,
    **logins_dict,
    **network_devices_activity_dict,
    "Auto Backup executed": [auto_backup, 5, "auto_backup"],
}
