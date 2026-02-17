from pathlib import Path

import sys
import time

from workflow_run import run


select = fr'{sys.argv[1]}'
select = Path(select)

run(select)

# print(select)
# time.sleep(5)


# backup_folder = os.getenv(key='BACKUP_FOLDER', default=False)
# collection_folder = os.getenv(key='COLLECTION_FOLDER')