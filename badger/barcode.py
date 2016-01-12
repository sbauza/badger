#!/usr/bin/env python
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import qrcode
from qrcode.image.pure import PymagingImage


class BarCode(object):
    def __init__(self, data):
        self.data = data
        self.qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            )
        self.qr.add_data(self.data)
        self.qr.make()
        self.img = self.qr.make_image(image_factory=PymagingImage)

    def save(self, filename='test.png'):
        with open(filename, 'wb') as wd:
            self.img.save(wd)
