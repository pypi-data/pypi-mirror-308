# import API
from .rp2040_api import RP2040API
# load motor map
import os
import yaml

library_path = os.path.dirname(__file__)
yaml_file_name = "motor_map.yaml"
yaml_path = os.path.join(library_path, yaml_file_name)
with open(yaml_path, 'r') as motor_config_file:
    _motor_config = yaml.safe_load(
           motor_config_file
       )
    MOTOR_MAP = _motor_config["motor_map"]
    MIDDLEWARE_MAP = _motor_config["middleware_convention_map"]
    UART_IDS = _motor_config["motor_board_uart_ids"]
