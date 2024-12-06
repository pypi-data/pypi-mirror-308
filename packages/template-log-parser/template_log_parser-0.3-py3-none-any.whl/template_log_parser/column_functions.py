# Pre-built functions to run on columns that need additional processing


def split_name_and_mac(name_and_mac):
    """
    Return a tuple of two strings including client name and client mac address after splitting string at colon

        Args:
            name_and_mac (str):
                must either be in the format of 'client_name:client_mac_address', or simply 'client_mac_address'
        Returns:
            tup:
                (client_name, client_mac_address) or ('unnamed', client_mac_address) if string includes only mac address
    """
    # Split at colon
    client_name_and_mac = name_and_mac.split(":")
    # Unnamed by default
    client_name = "unnamed"
    # client name will be extracted if present(len == 2), otherwise it will remain unnamed
    if len(client_name_and_mac) == 2:
        client_name = client_name_and_mac[0]
        client_mac = client_name_and_mac[1]

    # This leaves the possibility open that splits lists of three items or greater will be processed incorrectly
    # This issue should be addressed at the template stage and not by this function
    else:
        client_mac = client_name_and_mac[0]

    return client_name, client_mac


def calc_time(time_string, increment="minutes"):
    """
    Return float value of time in specified increment deciphered from string data
     including h,m,s, converted to seconds, minutes, or hours

        Args:
            time_string (str):
                formatted as 23h4m, 47m, or 45s
            increment (optional) (default 'minutes') {'seconds', 'minutes', 'hours'}:
                type of desired time conversion

        Returns:
            float:
                float value of time calculated in requested increment
    """
    # Default conversion to minutes, values that will be used to divide once data is converted to a numeric type
    s, m, h = 60, 1, 1
    time = 0
    if increment == "seconds":
        s, m, h = 1, (1 / 60), (1 / 3600)
    elif increment == "minutes":
        s, m, h = 60, 1, (1 / 60)
    elif increment == "hours":
        s, m, h = 3600, 60, 1
    # Time presented in seconds ex: '45s'
    if "s" in time_string:
        # Divide by the appropriate conversion number
        time = int(time_string.replace("s", "")) / s

    # Time in only minutes will be in the format 46m, 8m etc
    if len(time_string) < 4 and "m" in time_string:
        # Divide by the appropriate conversion number
        time = int(time_string.replace("m", "")) / m

    # Time in hours will be in the format 24h8m
    if len(time_string) > 3:
        time_split = time_string.split("h")
        # Divide by the appropriate conversion numbers
        hours = int(time_split[0]) / h
        minutes = int(time_split[1].replace("m", "")) / m

        time = hours + minutes

    return time


def calc_data_usage(data_string, increment="MB"):
    """
    Return float value of data usage in specified increment deciphered from string data including bytes, KB, MB, or GB

        Args:
            data_string (str):
                formatted as '0 bytes', '313.5KB', '535MB', or '12GB', spaces will be removed
            increment (optional) (default 'MB') {'KB', 'MB', 'GB'}:
                type of desired data conversion

        Returns:
            float:
                data usage in specified increment
        Notes:
            Conversions are performed using factors of 10 for simplicity.
    """
    # Default conversion to MB, function will select appropriate conversion rates if a different selection is made
    b, k, m, g = 1000000, 1000, 1, (1 / 1000)
    if increment == "KB":
        b, k, m, g = 1000, 1, (1 / 1000), (1 / 1000000)
    if increment == "MB":
        b, k, m, g = 1000000, 1000, 1, (1 / 1000)
    if increment == "GB":
        b, k, m, g = 1000000000, 1000000, 1000, 1
    # Remove all spaces
    data_string = data_string.replace(" ", "")
    # Remove alphanumeric characters and adjust to appropriate magnitude
    data_usage = 0
    if "bytes" in data_string:
        data_usage = float(data_string.replace("bytes", "")) / b
    if "KB" in data_string:
        data_usage = float(data_string.replace("KB", "")) / k

    if "MB" in data_string:
        data_usage = float(data_string.replace("MB", "")) / m

    if "GB" in data_string:
        data_usage = float(data_string.replace("GB", "")) / g

    return data_usage


def isolate_ip_from_parentheses(ip_string):
    """
    Isolate and return an ip address from surrounding parentheses

        Args:
            ip_string (str):
                formatted 10.0.10.10, (10.20.30.6), WORKGROUP(10.90.10.3), etc

        Returns:
            str: ip address

        Note: Conversion to IPv4/IPv6 Address object is not performed
    """

    # Check if parentheses are present before splitting/selecting the appropriate index
    if "(" in ip_string:
        ip_string = ip_string.split("(")[1]
    if ")" in ip_string:
        ip_string = ip_string.split(")")[0]

    return ip_string
