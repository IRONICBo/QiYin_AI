import utils.config as config
import utils.log as log
from utils import banner
import constants.constants as constants
from router.router import get_api

import os
import uvicorn

# Version 1.1.0
logger = None


def run(config: config.QYConfig):
    app = get_api(config)

    uvicorn.run(app, host=config.get_app_host(), port=config.get_app_port())


def main():
    # Init system
    kf_config = config.QYConfig("config.yaml")
    global logger
    log.QYLog.init_logger(
        kf_config.get_app_log_path(), constants.LOG_LEVEL_DEBUG
        if kf_config.get_app_debug() else constants.LOG_LEVEL_INFO)
    logger = log.QYLog.get_logger()
    banner.kf_banner(kf_config.get_app_version(), kf_config.get_app_debug(),
                     kf_config.get_app_log_path())

    # Init env
    os.environ["OPENAI_API_KEY"] = kf_config.get_openai_api_key()
    os.environ["OPENAI_API_BASE"] = "http://" + kf_config.get_fastchat_openai_api_server_host() + \
        ":" + kf_config.get_fastchat_openai_api_server_port() + "/v1"

    # Run
    run(kf_config)


if __name__ == "__main__":
    main()