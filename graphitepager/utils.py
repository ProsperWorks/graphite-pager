import argparse
import re


def parse_duration_to_seconds(duration_str):
    """
    Parse a duration string (e.g., '10m', '5min', '1h', '30s') to seconds.
    
    Supports formats:
    - '10m' or '10min' = 10 minutes
    - '1h' or '1hour' = 1 hour
    - '30s' or '30sec' = 30 seconds
    
    Args:
        duration_str: String like '10m', '5min', '1h', '30s'
    
    Returns:
        int: Duration in seconds, or None if parsing fails
    """
    if not duration_str:
        return None
    
    # Normalize the string
    duration_str = duration_str.strip().lower()
    
    # Pattern: number followed by unit
    pattern = r'^(\d+)\s*(m|min|minute|minutes|h|hour|hours|s|sec|second|seconds)$'
    match = re.match(pattern, duration_str)
    
    if not match:
        return None
    
    value = int(match.group(1))
    unit = match.group(2)
    
    # Convert to seconds
    if unit in ('s', 'sec', 'second', 'seconds'):
        return value
    elif unit in ('m', 'min', 'minute', 'minutes'):
        return value * 60
    elif unit in ('h', 'hour', 'hours'):
        return value * 3600
    else:
        return None


def parse_args():
    parser = argparse.ArgumentParser(description='Run Graphite Pager')
    parser.add_argument(
        'command',
        choices=['run', 'verify'],
        default='run',
        help='What action to take',
        nargs='?'
    )
    parser.add_argument(
        '-c',
        '--config',
        dest='config',
        default='alerts.yml',
        help='path to the config file'
    )

    args = parser.parse_args()
    return args
