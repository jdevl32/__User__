#!/usr/bin/env python3
# create.py

"""
...
"""

import argparse
import getopt
import os
# import platform
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

    # def __init__(self):
    #     self._prompt = False

    # @property
    # def _noPromptText(self):
    #     return common.isNull(self.prompt)

    # @property
    def doPrompt(self):
        """
        ...
        :return:
        :rtype: bool
        """

        # return self._prompt
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

    # @property
    def getPrompt(self):
        """
        ...
        :return:
        :rtype: str
        """

        _prompt = self.prompt
        return _prompt if common.isNull(_prompt) else _prompt[0]

    # def removeOnly(self):
    #     """
    #     ...
    #     :return:
    #     :rtype: bool
    #     """
    #
    #     return self.r or self.remove


def _create_01(basePath, profileDirName, targetDirName, removeOnly=False):
    """
    ...
    :param basePath:
    :type basePath: str
    :param profileDirName:
    :type profileDirName: str
    :param targetDirName:
    :type targetDirName: str
    :param removeOnly:
    :type removeOnly: bool
    :return:
    """

    baseOSPath = Constant.EMPTY
    targetOSName = Constant.EMPTY
    targetOSPath = os.path.join(baseOSPath, targetOSName)
    linkOSName = Constant.EMPTY
    linkOSPath = os.path.join(baseOSPath, linkOSName)
    # todo: extract computer-name from ???
    computerName = Constant.EMPTY
    computerPath = computerName
    targetProfilePath = Constant.EMPTY

    delimiter = os.sep
    list = os.path.join(basePath, targetDirName).strip(delimiter).split(delimiter)

    delimiter = list[0].upper()

    if os.path.splitdrive(basePath)[0].upper() == delimiter:
        list[0] = "[{drive} Drive]".format(drive=delimiter.strip(Constant.COLON))

    list.reverse()

    delimiter = Constant.PLUS_SIGN
    linkProfilePath = delimiter.join(list)
    linkPath = os.path.join(os.path.expanduser(Default.USER_PROFILE_DIR_EXP), profileDirName, linkProfilePath)
    tds = "{} ".format(Constant.COLON)

    if os.path.lexists(linkPath):
        common.trace("Remove", value=linkPath, tds=tds)

        os.remove(linkPath)
    elif removeOnly:
        common.trace\
            (
                "Path"
                ,
                descriptor=common.formatTraceString(linkPath)
                ,
                value="does not exist (cannot remove)!"
                ,
                tds=" "
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


def _create_02(rootPath, profileDirName, targetDirName, removeOnly=False):
    """
    ...
    :param rootPath:
    :type rootPath: str
    :param profileDirName:
    :type profileDirName: str
    :param targetDirName:
    :type targetDirName: str
    :param removeOnly:
    :type removeOnly: bool
    :return:
    """

    _p = os.path.join(os.path.expanduser(Default.USER_PROFILE_DIR_EXP), profileDirName)
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
    linkPath = os.path.join(_p, linkProfilePath)
    tds = "{} ".format(Constant.COLON)

    if os.path.lexists(linkPath):
        common.trace("Remove", value=linkPath, tds=tds)

        os.remove(linkPath)
    elif removeOnly:
        common.trace\
            (
                # "Path"
                tag=None
                ,
                descriptor=common.formatTraceString(linkPath)
                ,
                value="does not exist (cannot remove)!"
                # ,
                # tds=" "
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
                # "Path"
                tag=None
                ,
                descriptor=common.formatTraceString(linkPath)
                ,
                value="does not exist (cannot remove)!"
                # ,
                # tds=" "
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


def _getNamespaceArgs_00(arg):
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
        args = [(*argt, namespace.removeOnly()) for argt in args]

    return args, namespace


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


def _getOptions_00(arg):
    option = \
        {
            # ("a", "-all"): {"index": -1, "value": None}
            ("a", "-all"): {_INDEX: None}
            ,
            ("p", "-prompt"): {_INDEX: None, _VALUE: None}
        }

    # for switch, on in option.items():
    # pass
    for key in option.keys():
        for item in key:
            switch = "-{}".format(item)

            if switch in arg:
                index = arg.index(switch, 1)
                option[key][_INDEX] = index

                if _VALUE in option[key]:
                    option[key][_VALUE] = arg[1 + index]

                break

    return option


def _getOptions_01(arg):
    option = \
        {
            # ("a", "-all"): {"index": -1, "value": None}
            ("a", "-all"): {_INDEX: None}
            ,
            ("p", "-prompt"): {_INDEX: None, _VALUE: None}
        }

    # for switch, on in option.items():
    # pass
    for key in option.keys():
        for item in key:
            switch = "-{}".format(item)

            if switch in arg:
                index = arg.index(switch, 1)
                option[key][_INDEX] = index

                if _VALUE in option[key]:
                    option[key][_VALUE] = arg[1 + index]

                break

    return option


def _createArgParser_00():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    # parser.add_argument("-p", "--prompt", nargs="?", const=argparse.SUPPRESS, default=argparse.SUPPRESS)
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("-p", action="store_true")
    group.add_argument("--prompt", nargs=1)#, const=argparse.SUPPRESS, default=argparse.SUPPRESS)
    # group.add_argument("root", nargs=1)
    # group.add_argument("args", nargs=3)
    # parser.add_argument("dirs", nargs=2, default=argparse.SUPPRESS)
    # group = parser.add_argument_group("dir", argument_default=argparse.SUPPRESS)#, nargs=2, default=argparse.SUPPRESS)
    # group.add_argument("a", nargs="?", default=argparse.SUPPRESS)
    # group.add_argument("b", nargs="?", default=argparse.SUPPRESS)
    parser.add_argument("dirNames", nargs="?", default=argparse.SUPPRESS, metavar="dirName1 dirName2")
    parser.add_argument("root", nargs=1)  # , required=True)
    return parser


# todo: remove (does not work)
def _createArgParser_01():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("-p", action="store_true")
    group.add_argument("--prompt", nargs=1)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("a1", nargs=1)
    group.add_argument("a3", nargs=3)
    return parser


def _createArgParser_02():
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
    group.add_argument("-r", action="store_true")
    group.add_argument("--remove", action="store_true")
    parser.add_argument("args", nargs=argparse.REMAINDER)
    return parser


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


def _getOpt_00(arg):
    return getopt.getopt(arg, "p", ["prompt="])


def _tryGetArgs_00(arg):
    """
    ...
    :param arg:
    :type arg: list
    :return:
    :rtype: tuple
    """

    # todo: (probably not) refactor (inline using starmap or * unpacking)
    parser, namespace = _parseArgs(arg[1:], _ArgNamespace())

    # return _tryGetCreateArgs_00(parser, namespace), namespace

    try:
        # createArgs = _getArgs(namespace.args)
        return _getArgs(namespace.args), namespace
    except KeyError:
        # parser.error("what now?!?!")
        parser.print_help()
        parser.exit()
        # parser.error(message=None)

    # return createArgs
    return None, namespace


# todo: ??? probably not needed (inline above) ???
def _tryGetCreateArgs_00(parser, namespace):
    try:
        return _getArgs(namespace.args)
    except KeyError:
        parser.print_help()
        parser.exit()

    return None


def main_00(arg):
    """
    ...
    :param arg:
    :type arg: list
    :return:
    """

    # common._pprint(_getOpt_00(arg[1:]))
    # args = _parseArgs(arg[1:])
    args = _ArgNamespace()
    _parseArgs(arg[1:], args)
    # common._pprint(args)

    # 1:1: - -a:001:4:1: <root>
    # 1:2: -o-a:011:6:3: <opt> <root>
    # 2:3:p-o-a:111:7:7: <opt> <prompt> <root>
    # 3:3: - - :000:0:0: <dir1> <dir2> <root>
    # 3:4: -o- :010:2:2: <opt> <dir1> <dir2> <root>
    # 4:5:p-o- :110:3:6: <opt> <prompt> <dir1> <dir2> <root>

    # -p
    #   $   -p      <p>     <d1>    <d2>    <r>     -p      <p>     n   +   -

    #   $   -p      .       <d1>    <d2>    <r>     .       .       5   1   -4
    #   $   -p      <p>     <d1>    <d2>    <r>     .       .       6   1   -5
    #   $   .       .       <d1>    <d2>    <r>     -p      .       5   4   -1
    #   $   .       .       <d1>    <d2>    <r>     -p      <p>     6   4   -2
    #   $   -p      .       .       .       <r>     .       .       3   1   -2
    #   $   -p      <p>     .       .       <r>     .       .       4   1   -3
    #   $   .       .       .       .       <r>     -p      .       3   2   -1
    #   $   .       .       .       .       <r>     -p      <p>     4   2   -2

    # valid + index:  1(5), 1(6), 4(5), 4(6)

    # common._pprint(arg)

    # switch = dict(a="-all", p="-prompt")
    # switch = \
    #     {
    #         "a" : ["-all", False]
    #         ,
    #         "p" : ["-prompt", False]
    #     }
    #
    # for id, state in switch:
    #     pass

    # option = _getOptions_00(arg)
    # common._pprint(option)

    # _create(arg[3], arg[1], arg[2])
    # _create(arg[-1], arg[-3], arg[-2])
    # _getCreateAllArgs(arg[-1])

    # __prompt__ = _PROMPT_SWITCH in arg
    # __prompt__ = args.p or not common.isNull(args.prompt)
    __prompt__ = args.doPrompt()
    prompt = __prompt__
    # index = 1 + (arg.index(_PROMPT_SWITCH, 1) if prompt else 0)
    # __arg__ = arg[index:]
    __arg__ = args.args

    # [_create(*t) for t in a]
    [_ for _ in starmap(_create, _getArgs(__arg__))]
    # for _ in starmap(_create, _getArgs(arg[index:])):
    #     pass

    if prompt:
        common.prompt(args.getPrompt())


def main_01(arg):
    """
    ...
    :param arg:
    :type arg: list
    :return:
    """

    createArgs, callArgs = _tryGetArgs_00(arg)

    [_ for _ in starmap(_create, createArgs)]

    if callArgs.doPrompt():
        common.prompt(callArgs.getPrompt())


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
