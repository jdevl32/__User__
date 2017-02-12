#!/usr/bin/env python3
# create.py

"""
...
"""

import argparse
import os
import sys

from itertools import starmap
from jpyz import common, default
from jpyz.constant import Constant
from jpyz.default import Default

_INDEX = "index"
_VALUE = "value"
_OPTION = \
    {
        "a": "all"
        ,
        "p": "prompt"
    }

_PROMPT_SWITCH = "-p"


class _ArgNamespace:
    """
    ...
    """

    def doPrompt(self):
        """
        ...
        :return:
        :rtype: bool
        """

        return self.p or not common.isNull(self.prompt)

    def getArgs(self, arg):
        """
        ...
        :param arg:
        :type arg: list
        :return:
        :rtype: list
        """

        return [(*argt, self.force, self.remove) for argt in arg]

    def getPrompt(self):
        """
        ...
        :return:
        :rtype: str
        """

        _prompt = self.prompt
        return _prompt if common.isNull(_prompt) else _prompt[0]


def _create(rootPath, profileDirName, targetDirName, forceCreate=False, removeOnly=False):
    """
    ...
    :param rootPath:
    :type rootPath: str
    :param profileDirName:
    :type profileDirName: str
    :param targetDirName:
    :type targetDirName: str
    :param forceCreate:
    :type forceCreate: bool
    :param removeOnly:
    :type removeOnly: bool
    :return:
    """

    baseProfilePath = os.path.join(os.path.expanduser(Default.USER_PROFILE_DIR_EXP), profileDirName)

    if forceCreate and not os.path.lexists(baseProfilePath):
        os.makedirs(baseProfilePath, exist_ok=True)

    baseOSPath = Constant.EMPTY
    targetOSName = Constant.EMPTY
    targetOSPath = os.path.join(baseOSPath, targetOSName)
    linkOSName = Constant.EMPTY
    linkOSPath = os.path.join(baseOSPath, linkOSName)
    # todo: extract computer-name from ???
    computerName = Constant.EMPTY
    computerPath = computerName
    basePath = os.path.join(rootPath, Default.SHARE_STORAGE_DIR_NAME)
    targetProfilePath = Constant.EMPTY

    delimiter = os.sep
    list = os.path.join(basePath, targetDirName).strip(delimiter).split(delimiter)
    delimiter = list[0].upper()

    if os.path.splitdrive(basePath)[0].upper() == delimiter:
        list[0] = "[{drive} Drive]".format(drive=delimiter.strip(Constant.COLON))

    list.reverse()

    delimiter = Constant.PLUS_SIGN
    linkProfilePath = delimiter.join(list)
    linkPath = os.path.join(baseProfilePath, linkProfilePath)
    tds = "{} ".format(Constant.COLON)

    if os.path.lexists(linkPath):
        common.trace("Remove", value=linkPath, tds=tds)

        os.remove(linkPath)
    elif removeOnly:
        common.trace\
            (
                tag=None
                ,
                descriptor=common.formatTraceString(linkPath)
                ,
                value="does not exist (cannot remove)!"
                ,
                dvs=" "
            )

    if removeOnly:
        return

    baseTargetPath = os.path.join(basePath, targetOSPath, computerPath)
    targetPath = os.path.join(baseTargetPath, targetProfilePath, targetDirName)

    common.trace\
        (
            "Symlink"
            ,
            descriptor=common.formatTraceString(targetPath)
            ,
            value=common.formatTraceString(linkPath)
            ,
            tds=tds
            ,
            dvs=" <-- "
        )

    os.symlink(targetPath, linkPath)


def _getArgs(arg):
    """
    ...
    :param arg:
    :type arg: list
    :return:
    :rtype: list
    """

    return \
        {
            0: _getCreateAllPlatformArgs
            ,
            1: _getCreateAllArgs
            ,
            2: _getCreatePlatformArgs
            ,
            3: _getCreateArgs
        }\
            .get(len(arg), lambda arg: None)(arg)


def _getCreateAllArgs(arg):
    """
    ...
    :param arg:
    :type arg: list
    :return:
    :rtype: list
    """

    dirName = \
        {
            Default.PROJECTS_DIR_NAME:
                {
                    None:
                        [
                            Default.DEVELOPMENT_DIR_NAME
                        ]
                }
            ,
            Default.DOCUMENTS_DIR_NAME:
                {
                    None:
                        [
                            Default.DOCUMENT_DIR_NAME
                        ]
                }
            ,
            Default.DOWNLOADS_DIR_NAME:
                {
                    None:
                        [
                            Default.DOWNLOAD_DIR_NAME
                        ]
                }
            ,
            Default.MUSIC_DIR_NAME:
                {
                    Default.MEDIA_DIR_NAME:
                        [
                            Default.MUSIC_DIR_NAME
                        ]
                }
            ,
            Default.PICTURES_DIR_NAME:
                {
                    Default.MEDIA_DIR_NAME:
                        [
                            Default.PHOTO_DIR_NAME
                            ,
                            Default.IMAGE_DIR_NAME
                            ,
                            Default.SCAN_DIR_NAME
                        ]
                }
            ,
            Default.VIDEOS_DIR_NAME:
                {
                    Default.MEDIA_DIR_NAME:
                        [
                            Default.VIDEO_DIR_NAME
                        ]
                }
        }

    return \
        [
            (arg[-1], profileDirName, targetDirName)
            for profileDirName, subDir in dirName.items()
            for parentDirName, childDir in subDir.items()
            for targetDirName in
            [
                childDirName
                if common.isNullOrEmpty(parentDirName)
                else
                os.path.join(parentDirName, childDirName)
                for childDirName in childDir
            ]
        ]


def _getCreateArgs(arg):
    """
    ...
    :param arg:
    :type arg: list
    :return:
    :rtype: list
    """

    return [(arg[-1], arg[-3], arg[-2])]


def _getCreateAllPlatformArgs(arg):
    """
    ...
    :param arg:
    :type arg: list
    :return:
    :rtype: list
    """

    return _getCreateAllArgs([default.getPlatformDataPath()])


def _getCreatePlatformArgs(arg):
    """
    ...
    :param arg:
    :type arg: list
    :return:
    :rtype: list
    """

    return _getCreateArgs([*arg, default.getPlatformDataPath()])


def _getNamespaceArgs(arg):
    """
    ...
    :param arg:
    :type arg: list
    :return:
    :rtype: tuple
    """

    parser, namespace = _parseArgs(arg[1:], _ArgNamespace())
    args = _getArgs(namespace.args)

    if common.isNull(args):
        parser.print_help()
        parser.exit()
    else:
        args = namespace.getArgs(args)

    return args, namespace


def _createArgParser():
    """
    ...
    :return:
    :rtype: ArgumentParser
    """

    parser = argparse.ArgumentParser(allow_abbrev=False)
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("-p", action="store_true")
    group.add_argument("--prompt", nargs=1)
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("-f", "--force", action="store_true")
    group.add_argument("-r", "--remove", action="store_true")
    parser.add_argument("args", nargs=argparse.REMAINDER)
    return parser


def _parseArgs(arg, namespace=None):
    """
    ...
    :param arg:
    :type arg: list
    :param namespace:
    :type namespace: namespace
    :return:
    :rtype: tuple
    """

    parser = _createArgParser()

    return parser, parser.parse_args(args=arg, namespace=namespace)


def main(arg):
    """
    ...
    :param arg:
    :type arg: list
    :return:
    """

    createArgs, callArgs = _getNamespaceArgs(arg)

    [_ for _ in starmap(_create, createArgs)]

    if callArgs.doPrompt():
        common.prompt(callArgs.getPrompt())


# determine call method...
if common.isScript():
    # run script...
    main(sys.argv)
