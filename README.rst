===============================
badger
===============================

Badges for Snowcamp

Please feel here a long description which must be at least 3 lines wrapped on
80 cols, so that distribution package maintainers can use it in their packages.
Note that this is a hard requirement.

* Free software: Apache license
* Documentation: readthedocs soon
* Source: http://github.com/sbauza/badger
* Bugs: github issues...

Usage
--------

git clone http://github.com/sbauza/badger
cd badger
virtualenv build
source build/bin/activate
pip install -r requirements.txt (an error should be done, it's okay)

<copy etc/badger.conf and edit the creds>
badger --badge_template etc/snowcamp2016.svg.jinja2 --config-file badger.conf.secret
