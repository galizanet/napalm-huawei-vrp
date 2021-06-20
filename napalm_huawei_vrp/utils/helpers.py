import re


def parse_line_lldp(line):
    """
    This auxiliary method perform a regex search against all defined
    regexes and return the key and match result of the first matching
    regex

    Input: line (str)
    Output: key, value for the first matching regex
    """
    rx_dict = {
        'local_intf': re.compile(r"(?P<local_intf>\S+)(?:\s+has \d+ neighbor\(s\):)"),
        'remote_neigh_count': re.compile(r"(?:\S+\s+has\s+)(?P<remote_neigh_count>\d+)(?:\s+neighbor\(s\):)")
        'remote_port': re.compile(r"(?:Port ID\s+:)(?P<remote_port>\S+$)"),
        'remote_port_description': re.compile(r"(?:Port description\s+:)(?P<remote_port_description>.*$)"),
        'chassis_id': re.compile(r"(?:Chassis ID\s+:)(?P<chassis_id>.*$)"),
        'system_name': re.compile(r"(?:System name\s+:)(?P<system_name>.*$)"),
        'system_description': re.compile(r"(?:System description\s+:)(?P<system_description>.*$)"),
        'system_capab': re.compile(r"(?:System capabilities supported\s+:)(?P<system_capab>.*$)"),
        'system_enable_capab': re.compile(r"(?:System capabilities enabled\s+:)(?P<system_enable_capab>.*$)")
    }
    for key, rx in rx_dict.items():
        match = rx.search(line)
        if match:
            return key, match
    # if there are no matches
    return None, None
