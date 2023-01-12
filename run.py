#!/usr/bin/env python
from automagica import *
import os
import argparse
import subprocess
import time
import uuid
import re
import importlib
import match_a_graphic


def cli_interface():
    parser = argparse.ArgumentParser(description='run robot')
    parser.add_argument('--robot', dest='robot_filename', nargs='+',
                        type=str, help='input script', required=True)
    parser.add_argument('--args', dest='robot_arguments', nargs='+',
                        type=str, help='input args', required=False)
    parser.add_argument('--logoff', action='store_true')
    args = parser.parse_args()
    return args


def get_output():
    output = []
    count = 0
    with open('tmp', 'r') as f:
        for line in f:
            if re.match(r'.*my_trace ERROR.*', line) and count == 0:
                first = re.search(r'^.*ERROR in  (.*)$', line)
                name = first.group(1)
                output.append(str('FAIL'))
                output.append(name)
                count += 1
            elif re.match(r'^.*INFO {', line) and count == 0:
                first = re.search(r',\d+\s+(.*) INFO {.*$', line)
                output.append(str('PASS'))
                output.append(first.group(1))
    if count == 0:
        return output[0], output[1]
    else:
        return str('FAIL'), name


def main():
    os.chdir('/home/kevin/PycharmProjects/robots')
    args = cli_interface()
    robot = args.robot_filename[0]
    uf = str(uuid.uuid4().hex)

    if args.robot_arguments:
        pass

    if args.logoff is True:
        Disablelog(switch=True)

    time.tzset()
    began = time.strftime('%x %X %Z')
    pstart = time.time()
    robot_module = importlib.import_module(robot)
    robot_module.start()
    end = time.time()
    finished = time.strftime('%x %X %Z')
    stop_watch = end - pstart
    stop_watch = "{0:.2f}".format(stop_watch)
    result, new_name = get_output()
    subprocess.Popen("/bin/rm tmp", shell=True).communicate()
    h_out = open('history.log', 'a')
    h_out.write(
            '%s - %s start: %s end: %s time taken: %s seconds\n'
            % (result, robot, began, finished, stop_watch))
    h_out.close()


if __name__ == "__main__":
    main()
