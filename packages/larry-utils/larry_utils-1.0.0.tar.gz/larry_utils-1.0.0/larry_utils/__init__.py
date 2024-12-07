from PIL import Image
import io
import json
import logging
from logging import FileHandler
import pickle 
import threading



def get_logger(logger_path: str = './logger',
               logger_name: str = 'video-fps',
               drop_console_handler: bool = False):

    # initialize logger
    logger = logging.getLogger(logger_name)
    # set level: NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler = FileHandler(filename=logger_path)


    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if not drop_console_handler:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger



def read_bytes(file_name, start_num, size, is_image=True):
    with open(file_name, 'rb') as f:
        f.seek(start_num)
        image = f.read(size)
    if is_image:
        image = Image.open(io.BytesIO(image))
    return image


def save_image_bytes(file_name, start_num, size, savename):
    try:
        x = read_bytes(file_name, start_num, size)
        with open(savename, 'wb') as f:
            f.write(x)
        return True
    except Exception as e:
        print(e)
        return False



def read_json(file_path):
    d = open(file_path).read().split('\n')
    res = []
    for line in d:
        try:
            res.append(json.loads(line))
        except:
            continue
    print('all {} lines, success {} lines'.format(len(d), len(res)))

    return res

def write_json(file_path, dat, mode='a'):
    with open(file_path, mode) as f:
        for i in dat:
            f.write(json.dumps(i, ensure_ascii=False) + '\n')

def read_pkl(file_path):
    import pickle 
    return pickle.loads(open(file_path, 'rb').read())

def write_pkl(file_path, d):
    import pickle
    with open(file_path, 'wb') as f:
        f.write(pickle.dumps(d))



def get_resolution(resolution):
    resolutions = [('16:9', 16./9), ('4:3', 4./3), ('1:1', 1), ('3:4', 3./4), ('9:16', 9./16)]
 
    Bmatch, Bdistance = '', 19
    ratio = resolution[0] / resolution[1]
    if True:
        for match, distance in resolutions:
            if abs(ratio - distance) < Bdistance:
                Bmatch = match
                Bdistance = abs(ratio - distance)
    return Bmatch


def hash(x):
    import hashlib
    return hashlib.md5(x.encode()).hexdigest()



def read_excel(file_path, is_ordered=False):
    import pandas as pd
    from collections import OrderedDict

    if '.xlsx' in file_path:
        # org = pd.read_excel(file_path).to_dict()
        xl = pd.ExcelFile(file_path)
        sheet_names = xl.sheet_names

        all_d = []
        for sheet_name in sheet_names:
            org = xl.parse(sheet_name)
            keys = org.keys()

            N = len(org[list(org.keys())[0]])

            dat = []
            for i in range(N):
                if is_ordered:
                    line = OrderedDict()
                else:
                    line = {}
                for k in keys:
                    line[k] = org[k][i]
                dat.append(line)
            all_d.append([sheet_name, dat])

        if len(all_d) == 1:
            return all_d[0][1]
        else:
            return all_d

         
    else:
        org = pd.read_csv(file_path).to_dict()
        keys = org.keys()

        N = len(org[list(org.keys())[0]])

        dat = []
        for i in range(N):
            if is_ordered:
                line = OrderedDict()
            else:
                line = {}
            for k in keys:
                line[k] = org[k][i]
            dat.append(line)

        return dat



def write_excel(file_path, dat):
    import pandas as pd
    pd.DataFrame(dat).to_csv(file_path)



def include_str_and(line, *args):
    for _ in args:
        if _ not in line:
            return False

    return True

def include_str_or(line, *args):
    for _ in args:
        if _  in line:
            return True

    return False




