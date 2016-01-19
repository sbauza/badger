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

import sys

from oslo_config import cfg

from badger import badge
from badger import barcode
from badger.yurplan import api

CONF = cfg.CONF
cli_opts = [
    cfg.StrOpt('badge_template', default='snowcamp2016.svg.jinja2',
               help='SVG template for badges'),
]

CONF.register_cli_opts(cli_opts)


def main():
    CONF(sys.argv[1:], project='badger', prog='main')
    template_file = CONF.find_file(CONF.badge_template)
    if not template_file:
        raise Exception('file not found')
    # TODO(sbauza): I really need to move that one in an opt...
    exceptions = {
        # Remy Sanlaville
        '63431120112828696': 'STAFF',
        # Clement Bouillier
        '6343112016581271': 'SPEAKER',
        # Jean Helou
        '6343112013847003': 'SPEAKER',
        }
    corrections = {
        '634311201230215': ('Patrice', 'Laporte'),
        '634311201397200': ('Pierre-Yves', 'Boyer'),
        '63431120123069863': ('', ''),
        '63431232223199949': ('', ''),
        '63431230923287652': ('', ''),
        '63431231023356343': ('', ''),
    }
    yurplan_api = api.YurplanAPI()
    conf_people = yurplan_api.get_badge_info(exceptions=exceptions,
                                             corrections=corrections)
    template = badge.SnowCampTemplate(template=template_file)
    for person in conf_people:
        filename = 'temp/qr_temp.png'
        barcode.BarCode(person['token']).save(filename)
        badge.SnowCampBadge(firstname=person['firstname'],
                            lastname=person['lastname'],
                            token=person['token'],
                            ticket_type=person['type'],
                            qr=filename, template=template).save()

if __name__ == 'main':
    sys.exit(main())
