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

from oslo_config import cfg
import requests
import yaml

CONF = cfg.CONF

api_opts = [
    cfg.StrOpt('api_key',
               default='mykey',
               secret=True,
               help='Secret key'),
    cfg.StrOpt('email',
               default='myemail@foo.com',
               secret=True,
               help='Login'),
    cfg.StrOpt('password',
               default='mysupersecret',
               secret=True,
               help='Password'),
]


CONF.register_opts(api_opts, 'yurplan')


YURPLAN_ENDPOINT = 'http://yurplan.com/api.php'


class YurplanAPI(object):
    def __init__(self):
        self.token = None
        self.auth()

    def auth(self):
        creds = {'email': CONF.yurplan.email,
                 'password': CONF.yurplan.password}
        r = requests.post(YURPLAN_ENDPOINT + '/auth',
                          params={'key': CONF.yurplan.api_key},
                          json=creds)
        if r.ok:
            self.token = r.json()['data']['token']

    def tickets(self, id='6343'):
        if not self.token:
            raise Exception("not authorized")
        r = requests.get(YURPLAN_ENDPOINT + '/events/%s/tickets' % id,
                         params={'key': CONF.yurplan.api_key,
                                 'token': self.token})
        if r.ok:
            return r.json()['data']['tickets']

    def ticket(self, ticket, id='6343'):
        if not self.token:
            raise Exception("not authorized")
        r = requests.get(
            YURPLAN_ENDPOINT + '/events/%(i)s/tickets/%(t)s/show' % {
                'i': id, 't': ticket},
            params={'key': CONF.yurplan.api_key, 'token': self.token,
                    'filter': 'scanv2'})
        if r.ok:
            return r.json()['data']

    def get_badge_info(self, conference_file):
        """Obtain list of badges from the different ticket types.

        :param exception_list: Dict w/ key == token and value == expected type
        """
        with open(conference_file, 'r') as conf_stream:
            try:
                conf_details = yaml.load(conf_stream)
            except yaml.YAMLError:
                raise Exception(
                    "%s is not a correct YAML file" % conference_file)

        conf_id = conf_details.get('conference', {}).get('id')
        speaker_ids = conf_details.get('participants', {}).get('speaker_ids')
        sponsor_ids = conf_details.get('participants', {}).get('sponsor_ids')
        staff_ids = conf_details.get('participants', {}).get('staff_ids')
        attendee_ids = conf_details.get('participants', {}).get('attendee_ids')
        corrections = conf_details.get('corrections') or {}
        exceptions = conf_details.get('exceptions') or {}

        tickets = self.tickets(conf_id)
        conf_tickets = []
        for ticket in tickets:
            if int(ticket['type']['id']) in attendee_ids:
                ticket['_type'] = 'ATTENDEE'
            if int(ticket['type']['id']) in speaker_ids:
                ticket['_type'] = 'SPEAKER'
            if int(ticket['type']['id']) in sponsor_ids:
                ticket['_type'] = 'SPONSOR'
            if int(ticket['type']['id']) in staff_ids:
                ticket['_type'] = 'STAFF'
            if ticket['token'] in exceptions.keys():
                ticket['_type'] = exceptions.get(ticket['token'],
                                                 ticket.get('_type',
                                                            'ATTENDEE'))
            if ticket.get('_type'):
                if ticket['token'] in corrections:
                    (firstname, lastname) = corrections[ticket['token']]
                    ticket['firstname'] = firstname
                    ticket['lastname'] = lastname
                conf_tickets.append(ticket)

        return [{'firstname': t['firstname'],
                 'lastname': t['lastname'],
                 'token': t['token'],
                 'type': t['_type']}
                for t in conf_tickets]
