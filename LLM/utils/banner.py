

import sys
import os 

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


def kf_banner(version: str, debug: bool, log_path: str) -> None:
    print(f'''
--------------------------------------------------------------------------------------------------------------------
	______________  ______             __________________
	__  __ \__(_) \/ /__(_)______      ___  __ )__  ____/
	_  / / /_  /__  /__  /__  __ \     __  __  |_  __/   
	/ /_/ /_  / _  / _  / _  / / /     _  /_/ /_  /___   
	\___\_\/_/  /_/  /_/  /_/ /_/      /_____/ /_____/                                                                                        

APP Mode:
- Version: %s
- Debug: %v
- Log file: %s

Topic: https://www.qiniu.com/activity/detail/651297ed0d50912d3d53307b#topic-introduction
Contributer: @IRONICBo @Baihhh @nnnnn319
--------------------------------------------------------------------------------------------------------------------
''' % (version, debug, log_path))
          