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

_COLORS = {
    'STAFF': "#ee0000",
    'SPONSOR': "#00ee00",
    'SPEAKER': "#00b3ff",
    'ATTENDEE': "#e0e0e0"}


class SnowCampTemplate(object):
    def __init__(self, template='snowcamp2016.svg.jinja2'):
        template_path, template_name = os.path.split(template)
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_path))
        self.template = env.get_template(template_name)

    def render(self, *args, **kwargs):
        return self.template.render(*args, **kwargs)


class SnowCampBadge(object):

    @staticmethod
    def _handle_qr(qr):
        # we suppose a filename
        if isinstance(qr, str) and os.path.exists(qr):
            with open(qr, "rb") as qr_fd:
                return "data:image/png;base64," + base64.b64encode(
                    qr_fd.read())

    def __init__(self, firstname, lastname, qr, token, ticket_type='ATTENDEE',
                 template=None):
        self.template = (template if template is not None
                         else SnowCampTemplate())
        self.firstname = firstname.title()
        self.lastname = lastname.title()
        self.qr = self._handle_qr(qr)
        self.token = token
        self.type = ticket_type.upper()

        self.badge = self.template.render(firstname=self.firstname,
                                          lastname=self.lastname,
                                          type=self.type,
                                          qr=self.qr,
                                          color=_COLORS.get(self.type)
                                          ).encode('utf-8')

    def save(self, filename=None, output='pdf'):
        if filename is None:
            filename = '%(firstname)s_%(lastname)s_%(token)s.svg' % {
                'firstname': self.firstname,
                'lastname': self.lastname,
                'token': self.token}
        with open(filename, 'w+') as fp:
            fp.write(self.badge)
        if output == 'pdf':
            self.exportPDF(filename)

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
