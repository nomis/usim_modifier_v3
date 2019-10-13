#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from control.components import components
from control.constants import LAYOUT, STATE
import control.log as log


class error():
    def __init__(self):
        pass

    def execute(self, arg_components: components, arg_arguments):
        log.debug(self.__class__.__name__, "execute")

        layout = arg_components.viewer.get_layout(
            LAYOUT.ERROR, arg_string=arg_arguments)

        print(layout)

        return (STATE.EXIT, None)
