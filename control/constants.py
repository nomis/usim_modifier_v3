#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import colorama


class PIN_TYPE:
    PIN1 = 0x01
    PIN2 = 0x81
    ADM1 = 0x0A


class ERROR:
    NONE = 0
    CARD_ABSENT = 1
    INVALID_ARGUMENT = 2
    INCORRECT_PIN = 3
    INCORRECT_ADM = 4
    UICC_BLOCKED = 5


class STATE:
    NONE = 'none'
    STARTUP = 'startup'
    INITIAL = 'initial'
    PIN = 'pin'
    ADM = 'adm'
    EXCEPTION = 'exception'
    ERROR = 'error'
    EXIT = 'exit'
    PLUGIN = 'plugin'
    CLI = 'cli'
    HELP = 'help'
    PLUGIN_LIST = 'plugin_list'
    EXECUTE = 'execute'
    DISPATCH = 'dispatch'


class LAYOUT:
    ONELINE = 'oneline'
    EXCEPTION = 'exception'
    STARTUP = 'startup'
    ERROR = 'error'
    PLUGIN_INFO = 'plugin_info'
    CLI_PREFIX = 'cli_prefix'
    PLUGIN_HELP = 'plugin_help'


class UICC_FILE:
    MF = "3F00"
    ICCID = "2FE2"
    ADF = "7FFF"
    IMSI = "6F07"
    AD = "6FAD"
    GID1 = "6F3E"
    GID2 = "6F3F"
    MSISDN = "6F40"
    SPN = "6F46"


class ALIGN:
    LEFT = 0
    CENTER = 1
    RIGHT = 2


class STYLE:
    BRIGHT = colorama.Style.BRIGHT
    DIM = colorama.Style.DIM
    NORMAL = colorama.Style.NORMAL
    RESET_ALL = colorama.Style.RESET_ALL


class COLOR_FORE:
    BLACK = colorama.Fore.BLACK
    RED = colorama.Fore.RED
    GREEN = colorama.Fore.GREEN
    YELLOW = colorama.Fore.YELLOW
    BLUE = colorama.Fore.BLUE
    MAGENTA = colorama.Fore.MAGENTA
    CYAN = colorama.Fore.CYAN
    WHITE = colorama.Fore.WHITE
    RESET = colorama.Fore.RESET


class COLOR_BACK:
    BLACK = colorama.Back.BLACK
    RED = colorama.Back.RED
    GREEN = colorama.Back.GREEN
    YELLOW = colorama.Back.YELLOW
    BLUE = colorama.Back.BLUE
    MAGENTA = colorama.Back.MAGENTA
    CYAN = colorama.Back.CYAN
    WHITE = colorama.Back.WHITE
    RESET = colorama.Back.RESET
