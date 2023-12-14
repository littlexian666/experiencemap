import logging
import os
import sys
import yaml
from typing import Optional

from pathlib import Path
root_path = Path(os.path.abspath(__file__)).parent

# 设置读取配置文件
with open(os.path.join(root_path, "config.yaml"), "r", encoding='utf-8') as fp:
    cfg = yaml.safe_load(fp)


def get_logger(
        name: Optional[str] = None,
        use_error_log: bool = False,
        log_dir: Optional[os.PathLike] = None,
        log_filename: Optional[str] = None,
):
    if name is None:
        name = __file__

    def list_handlers(logger):
        return {str(h) for h in logger.handlers}

    logger = logging.getLogger(name)
    logging_level = getattr(logging, "INFO")
    logger.setLevel(logging_level)

    formatter = logging.Formatter(
        fmt="%(asctime)s %(filename)s: %(levelname)s: %(message)s"
    )
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging_level)
    stdout_handler.setFormatter(formatter)
    if str(stdout_handler) not in list_handlers(logger):
        logger.addHandler(stdout_handler)
    if log_dir:  # logging to file
        os.makedirs(log_dir, exist_ok=True)
        if log_filename is None:
            log_filename = "log"
        log_file = os.path.join(log_dir, log_filename)
        fh = logging.FileHandler(log_file, encoding='utf-8')
        fh.setLevel(logging_level)
        fh.setFormatter(formatter)
        if str(fh) not in list_handlers(logger):
            logger.addHandler(fh)

    if use_error_log:
        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setLevel(logging.WARNING)
        stderr_handler.setFormatter(formatter)
        if str(stderr_handler) not in list_handlers(logger):
            logger.addHandler(stderr_handler)

    logger.propagate = 0
    return logger


log_dir = cfg["log"]["log_dir"]
logger = get_logger(
    "address",
    log_dir=log_dir,
    log_filename=cfg["log"]["log_filename"],
)

