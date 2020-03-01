#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import control.log as log

from smartcard.util import toHexString, PACK
from model.apdu import *
from model.library.uicc_sel_resp import uicc_sel_resp
from model.library.fcp import EF_FILE_TYPE
from model.library.convert import convert_bcd_to_string
from control.constants import ERROR, PIN_TYPE, UICC_FILE, UICC_SELECT_TYPE
from model.library.fcp import search_fcp_content, TLV_TAG


class uicc:
    def __init__(self, arg_connection):
        self.__connection = arg_connection

        self.initialed = False
        # check pin status
        self.__pin_verified = False
        self.__adm_verified = False
        self.__pin_enabled = False

        uicc_resp = self.select(UICC_FILE.MF)
        self.__pin_enabled = uicc_resp.pin

        self.__iccid = None
        uicc_resp:uicc_sel_resp = self.select(UICC_FILE.ICCID)
        read_resp = self.read_binary(uicc_resp)
        if read_resp != None:
            self.__iccid = convert_bcd_to_string(read_resp)
            log.info(self.__class__.__name__, "ICCID: " + self.__iccid)

        # select AID for '7FFF'
        self.__aid = None
        self.__aid = self.__init_aid()
        
        if self.__aid != None and self.__iccid != None:
            self.initialed = True

    def __init_aid(self):
        read_resp: uicc_sel_resp = self.select(UICC_FILE.DIR)
        if read_resp.sw1 == 0x90:
            dir_record = read_record(1, read_resp.length)
            response, sw1, sw2 = self.__transmit(dir_record)
            if sw1 == 0x90:
                aid_content = search_fcp_content(
                    response, TLV_TAG.APPLICATION_IDENTIFIER)
                aid = toHexString(aid_content[2:], format=PACK)
                select_aid_apdu = select(aid, arg_type= UICC_SELECT_TYPE.DF_NAME)
                response, sw1, sw2 = self.__transmit(select_aid_apdu)
                return aid

        return None

    @property
    def iccid(self):
        return self.__iccid

    @property
    def pin_verified(self):
        return self.__pin_verified

    @property
    def pin_enabled(self):
        return self.__pin_enabled

    @property
    def adm_verified(self):
        return self.__adm_verified

    def __transmit(self, arg_apdu_cmd):
        log.debug(self.__class__.__name__,
                  "TX> %s" % (toHexString(arg_apdu_cmd)))
        response, sw1, sw2 = self.__connection.transmit(arg_apdu_cmd)
        log.debug(self.__class__.__name__,
                  "RX< %s, %02X %02X" % (toHexString(response), sw1, sw2))
        return (response, sw1, sw2)

    def atr(self):
        return self.__connection.getATR()

    def send(self, arg_apdu_cmd):
        return self.__transmit(arg_apdu_cmd)

    def select(self, arg_file_id, arg_type = UICC_SELECT_TYPE.FILE_ID):
        resp = sw1 = sw2 = None

        apdu = select(arg_file_id, arg_type = arg_type)
        if apdu != None:
            resp, sw1, sw2 = self.__transmit(apdu)

            if sw1 == 0x61:
                apdu = get_response(sw2)
                resp, sw1, sw2 = self.__transmit(apdu)

        return uicc_sel_resp(resp, sw1, sw2)

    def read_record(self, arg_file_id, arg_idx):
        pass

    def update_binary(self, arg_content):
        apdu = update_binary(arg_content)
        if apdu != None:
            resp, sw1, sw2 = self.__transmit(apdu)

            if sw1 == 0x90:
                return ERROR.NONE

        return ERROR.UNKNOWN

    def read_binary(self, arg_uicc_resp:uicc_sel_resp):
        if arg_uicc_resp.sw1 == 0x90 and arg_uicc_resp.ef_type == EF_FILE_TYPE.TRANSPARENT:
            apdu = read_binary(arg_uicc_resp.length)
            if apdu != None:
                resp, sw1, sw2 = self.__transmit(apdu)

                if sw1 == 0x90:
                    return resp
        return None

    def verify_pin(self, arg_type, arg_code):
        ret_result = ERROR.NONE
        ret_reamings = None
        apdu = verify_pin(arg_type, arg_code)
        resp, sw1, sw2 = self.__transmit(apdu)

        if sw1 == 0x90:
            if arg_type == PIN_TYPE.PIN1:
                self.__pin_verified = True
            elif arg_type == PIN_TYPE.ADM1:
                self.__adm_verified = True

        if sw1 == 0x63:
            ret_reamings = sw2 & 0x0F
            if ret_reamings == 0:
                ret_result = ERROR.UICC_BLOCKED
            else:
                ret_result = ERROR.INCORRECT_PIN

        return (ret_result, ret_reamings)
