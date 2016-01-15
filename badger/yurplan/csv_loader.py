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

import os
# py2 stdlib csv is not working with unicode
import unicodecsv as csv

class YurplanCSV(object):
    def __init__(self, csvfile):
        if os.path.exists(csvfile):
            with open(csvfile, 'rt') as fd:
                reader = csv.DictReader(fd, delimiter=';')
                self.rows = [row for row in reader]
        else:
            raise Exception("%s not found" % csvfile)

    def tickets(self):
        if not self.rows:
            raise Exception("csv not loaded")
        return [row for row in self.rows if ]

myfile = YurplanCSV('./snowcamp2016.csv')
