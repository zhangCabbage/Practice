#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""

import os
import sys
import shlex
import signal
import subprocess
import threading
import traceback


__version__ = '0.0.1'
__author__ = 'jiahua'
__license__ = 'MIT'
__copyright__ = 'Copyright 2009 Kenneth Reitz'


def _terminate_process(process):
    if sys.platform == 'win32': # indicate windows
        import ctypes
        PROCESS_TERMINATE = 1
        handle = ctypes.windll.kernel32.OpenProcess(PROCESS_TERMINATE, False, process.pid)
        ctypes.windll.kernel32.TerminateProcess(handle, -1)
        ctypes.windll.kernel32.CloseHandle(handle)
    else:  # linux like
        os.kill(process.pid, signal.SIGTERM)

def _kill_process(process):
    if sys.platform == 'win32':
        _terminate_process(process)
    else:
        os.kill(process.pid, signal.SIGKILL)

def _is_alive(thread):
    """ 查看线程是否超时，仍存活 """
    if hasattr(thread, "is_alive"):
        return thread.is_alive()
    else:
        return thread.isAlive() ## apply to the version before python 2.6


class Command(object):
    """ 一个完整的命令对象 """
    def __init__(self, cmd):
        super(Command, self).__init__()
        self.cmd = cmd
        self.process = None
        self.out = None
        self.err = None
        self.returncode = None
        self.data = None
        self.exc = None  ## 是否有异常

    def run(self, data, timeout, kill_timeout, env, cwd):
        self.data = data
        environ = dict(os.environ)
        environ.update(env or {})

        def target():
            try:
                self.process = subprocess.Popen(
                    self.cmd,
                    universal_newlines=True,
                    shell=False,
                    env=environ,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    bufsize=0,
                    cwd=cwd
                )

                # 针对python
                if sys.version_info[0] >= 3:
                    self.out, self.err = self.process.communicate(
                        input = bytes(self.data, "utf-8") if self.data else None
                    )
                else:
                    self.out, self.err = self.process.communicate(self.data)
            except Exception as exc:
                self.exc = exc

        thread = threading.Thread(target=target)
        thread.start()
        thread.join(timeout) ## block

        if self.exc:
            raise self.exc

        if _is_alive(thread):
            # 超时，那么杀死系统命令进程
            _kill_process(self.process)
            thread.join(kill_timeout)

            if _is_alive(thread):
                _kill_process(self.process)
                thread.join()

        self.returncode = self.process.returncode
        return self.out, self.err


class Response(object):
    """ 命令处理完之后的response对象 """
    def __init__(self):
        super(Response, self).__init__()
        self.command = None
        self.std_out = None
        self.std_err = None
        self.status_code = None
        self.history = [] #用来做历史记录

    def __repr__(self):
        if len(self.command):
            return '<Response [{0}]>'.format(self.command[0])
        else:
            return '<Response>'

def expand_args(command):
    """ use to parse command string """
    splitter = shlex.shlex(command)
    splitter.whitespace = '|'
    splitter.whitespace_split = True
    command = []

    while True:
        token = splitter.get_token()
        if token:
            command.append(token)
        else:
            break
    print command
    command = map(shlex.split, command)
    return command


def run(command, data=None, timeout=None, kill_timeout=None, env=None, cwd=None):
    """  """
    command = expand_args(command)

    history = []
    for c in command:
        if len(history):
            # ？
            data = history[-1].std_out

        cmd = Command(c)
        try:
            out, err = cmd.run(data, timeout, kill_timeout, env, cwd)
            status_code = cmd.returncode
        except OSError as e:
            out, err = '', u"\n".join([e.strerror, traceback.format_exc()])
            status_code = 127

        r = Response()
        r.command = c
        r.std_out = out
        r.std_err = err
        r.status_code = status_code

        history.append(r)

    r = history.pop()
    r.history = history

    return r


if __name__ == '__main__':
    """ use to test! """
    cmd = "ls | grep java"
    a = expand_args(cmd)
    r = run(cmd)
    print r.std_out
