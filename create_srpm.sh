#!/usr/bin/env bash

# This is a script used to create a source rpm due to the suboptimal creation of rpms by setuptools.
# This srpm may then be fed to a build system such as mock.

rm -rf dist
version=$(python -c "from spil_keystone_auth_plugin import __version__ as version; print version")
sed -i -r "s/^%define version.*/%define version $version/" spil-keystone-auth-plugin.spec
python setup.py sdist
rpmbuild -ts dist/*.tar.gz
