from src.data_collection import load_data
from src.signals_creation import get_returns_data, train_test_split
import yaml

def yaml_to_dict(config_file_path: str) -> dict:
    """Function that returns all config values contained in a config file

    Args:
        config_file_path (str): path of the config file

    Returns:
        dict: config values
    """
    try:
        from yaml import CLoader as Loader
    except ImportError:
        from yaml import Loader

    stream = open(config_file_path, "r")
    dictionary = yaml.load(stream, Loader=Loader)
    return dictionary

def init():
    global historical_data
    global train_data
    global test_data
    global returns
    global config_values
    config_values = yaml_to_dict("config.yaml")
    historical_data = load_data(config_values["data-collection"]["reload"],
                     config_values["data-collection"]["start_date"],
                       config_values["data-collection"]["coin_pair"],
                       config_values["data-collection"]["status"],
                       config_values["data-collection"]["data_folder"],
                       config_values["col_num_values_threshold"])

    train_data, test_data = train_test_split(historical_data, config_values["train_test_split_ratio"])
    returns = get_returns_data(train_data)