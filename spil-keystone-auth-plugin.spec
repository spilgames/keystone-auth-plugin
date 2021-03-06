#%define short_name swprobe
%define version 0.2.0
%define release SPI1
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary: Middleware for authenticating connecting keystone to an external service
Name: spil-keystone-auth-plugin
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.gz
License: Apache Software License 2.0
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Packager: Robert van Leeuwen <robert.vanleeuwen@spilgames.com>
Url: https://github.com/spilgames/keystone-auth-plugin
Requires: python
BuildRequires: python python-setuptools

%description
Middleware for authenticating connecting keystone to an external service

%prep
%setup -n %{name}-%{version}

%build
python setup.py build

%install
python setup.py install --root=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)

/usr/lib/python2.7/site-packages/spil_keystone_auth_plugin
/usr/lib/python2.7/site-packages/spil_keystone_auth_plugin-%{version}-py2.7.egg-info
