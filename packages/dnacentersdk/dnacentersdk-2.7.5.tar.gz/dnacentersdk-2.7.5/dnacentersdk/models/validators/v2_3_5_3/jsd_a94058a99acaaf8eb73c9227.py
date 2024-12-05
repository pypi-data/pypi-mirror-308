# -*- coding: utf-8 -*-
"""Cisco DNA Center UpdateEnterpriseSSID data model.

Copyright (c) 2019-2021 Cisco Systems.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


import json
from builtins import *

import fastjsonschema

from dnacentersdk.exceptions import MalformedRequest


class JSONSchemaValidatorA94058A99AcaAf8Eb73C9227(object):
    """UpdateEnterpriseSSID request schema definition."""
    def __init__(self):
        super(JSONSchemaValidatorA94058A99AcaAf8Eb73C9227, self).__init__()
        self._validator = fastjsonschema.compile(json.loads(
            '''{
                "$schema": "http://json-schema.org/draft-04/schema#",
                "properties": {
                "basicServiceSetClientIdleTimeout": {
                "type": "integer"
                },
                "clientExclusionTimeout": {
                "type": "integer"
                },
                "enableBasicServiceSetMaxIdle": {
                "type": "boolean"
                },
                "enableBroadcastSSID": {
                "type": "boolean"
                },
                "enableClientExclusion": {
                "type": "boolean"
                },
                "enableDirectedMulticastService": {
                "type": "boolean"
                },
                "enableFastLane": {
                "type": "boolean"
                },
                "enableMACFiltering": {
                "type": "boolean"
                },
                "enableNeighborList": {
                "type": "boolean"
                },
                "enableSessionTimeOut": {
                "type": "boolean"
                },
                "fastTransition": {
                "enum": [
                "Adaptive",
                "Enable",
                "Disable"
                ],
                "type": "string"
                },
                "mfpClientProtection": {
                "enum": [
                "Optional",
                "Disabled",
                "Required"
                ],
                "type": "string"
                },
                "name": {
                "type": "string"
                },
                "nasOptions": {
                "items": {
                "type": "string"
                },
                "type": "array"
                },
                "passphrase": {
                "type": "string"
                },
                "radioPolicy": {
                "enum": [
                "Triple band operation (2.4GHz, 5GHz and 6GHz)",
                "Triple band operation with band select",
                "5GHz only",
                "2.4GHz only",
                "6GHz only"
                ],
                "type": "string"
                },
                "securityLevel": {
                "enum": [
                "WPA2_ENTERPRISE",
                "WPA2_PERSONAL",
                "OPEN",
                "WPA3_ENTERPRISE",
                "WPA3_PERSONAL",
                "WPA2_WPA3_PERSONAL",
                "WPA2_WPA3_ENTERPRISE"
                ],
                "type": "string"
                },
                "sessionTimeOut": {
                "type": "integer"
                },
                "trafficType": {
                "enum": [
                "voicedata",
                "data"
                ],
                "type": "string"
                }
                },
                "type": "object"
                }'''.replace("\n" + ' ' * 16, '')
        ))

    def validate(self, request):
        try:
            self._validator(request)
        except fastjsonschema.exceptions.JsonSchemaException as e:
            raise MalformedRequest(
                '{} is invalid. Reason: {}'.format(request, e.message)
            )
