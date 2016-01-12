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

import base64
import os

import cairosvg
import jinja2


class SnowCampTemplate(object):
    def __init__(self, template='./snowcamp2016.svg'):
        template_path, template_name = os.path.split(template)
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_path))
        self.template = env.get_template(template_name)

    def badge(self, firstname, surname, qr_file):
        return SnowCampBadge(self.template, firstname, surname, qr_file)


class SnowCampBadge(object):
    def __init__(self, template, firstname, lastname, qr_file):
        self.template = template
        self.firstname = firstname
        self.lastname = lastname
        self.qr_file = qr_file
        with open(self.qr_file, "rb") as qr:
            qr_base64 = base64.b64encode(qr.read())
        self.badge = self.template.render(firstname=self.firstname,
                                          lastname=self.lastname,
                                          qr_base64=qr_base64).encode('utf-8')

    def save(self, filename=None):
        if filename is None:
            filename = '%(firstname)s_%(lastname)s.svg' % {
                'firstname': self.firstname,
                'lastname': self.lastname}
        with open(filename, 'w+') as fp:
            fp.write(self.badge)

    @classmethod
    def exportPDF(cls, filename):
        filepath, ext = os.path.splitext(filename)
        # TODO(sbauza): Modify that for knowing if it's a SVG file
        if ext != ".svg":
            # okay, it's not good to check the type by looking at the extension
            # but it's a quick workaround...
            raise Exception("%s is not a SVG file" % filename)
        dest = filepath + '.pdf'
        cairosvg.svg2pdf(url=filename, write_to=dest)
