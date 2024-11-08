import pandas as pd
import logging

def configure_logging():
    """
    Sets up logging to a file for tracking trade events and errors.
    """
    logging.basicConfig(filename="trading_bot.log",
                        level=logging.INFO,
                        format="%(asctime)s %(levelname)s: %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")

def log_event(message, level="info"):
    """
    Logs an event with the specified log level.
    """
    if level == "info":
        logging.info(message)
    elif level == "warning":
        logging.warning(message)
    elif level == "error":
        logging.error(message)
    else:
        logging.debug(message)

def is_trendline_valid(data, low_points_column='low'):
    """
    Checks if two or more points form a valid trendline (for uptrend, lows should align).
    Args:
        data (DataFrame): The DataFrame with price data.
        low_points_column (str): The column used to detect lows.
    Returns:
        bool: True if the trendline is valid, False otherwise.
    """
    # Example: Check if two consecutive lows form an upward trendline
    lows = data[low_points_column]
    slope = (lows.iloc[-1] - lows.iloc[-2]) / 2
    return slope > 0  # Return True if slope is positive

def detect_swing_highs_lows(data, window=3):
    """
    Identifies swing highs and lows within a defined window.
    Args:
        data (DataFrame): Data with high and low prices.
        window (int): The window around each point to define a swing high/low.
    Returns:
        DataFrame: Original data with additional columns 'swing_high' and 'swing_low'.
    """
    data['swing_high'] = data['high'][(data['high'].shift(1) < data['high']) & (data['high'].shift(-1) < data['high'])]
    data['swing_low'] = data['low'][(data['low'].shift(1) > data['low']) & (data['low'].shift(-1) > data['low'])]
    return data

def format_timestamp(timestamp):
    """
    Formats a timestamp for display or logging.
    Args:
        timestamp (datetime): The timestamp to format.
    Returns:
        str: Formatted timestamp as a string.
    """
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")
