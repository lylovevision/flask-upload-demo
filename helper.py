import os
import uuid
from datetime import datetime

def random_filename(filename):
    ts = datetime.now().strftime('%Y%m%d%H%M%S%f')
    rand_id = uuid.uuid5(uuid.NAMESPACE_DNS, ts).hex
    store_name = '{0}@{1}'.format(rand_id, filename)
    return store_name

def ensure_folder(folder):
    if not os.path.isdir(folder):
        if os.path.exists(folder):
            raise Exception('已经存在名为 “{}” 的文件, 不能创建文件夹')
        else:
            os.makedirs(folder)