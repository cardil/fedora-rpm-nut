%define initdir /etc/rc.d/init.d
%define cgidir  /var/www/nut-cgi-bin
%define modeldir /sbin
Summary: Network UPS Tools
Name: nut
Version: 0.45.4
Release: 4
Group: Applications/System
Source: http://www.exploits.org/nut/release/%{name}-%{version}.tar.gz
Source1: ups.init
Source2: ups.sysconfig
Patch0: nut-0.45.3-buildroot.patch
Patch1: nut-0.45.2-config.patch
Patch2: nut-0.45.0-conffiles.patch
License: GPL
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Requires: nut-client
Prereq: fileutils /sbin/chkconfig /sbin/service
BuildPrereq: gd-devel, freetype-devel, netpbm-devel, libpng-devel

%description
These programs are part of a developing project to monitor the assortment 
of UPSes that are found out there in the field. Many models have serial 
serial ports of some kind that allow some form of state checking. This
capability has been harnessed where possible to allow for safe shutdowns, 
live status tracking on web pages, and more.

%package client
Group: Applications/System
Summary: Network UPS Tools client monitoring utilities
Prereq: chkconfig

%description client
This package includes the client utilities that are required to monitor a
ups that the client host has access to, but where the UPS is physically
attached to a different computer on the network.

%package cgi
Group: Applications/System
Summary: CGI utilities for the Network UPS Tools
Requires: webserver

%description cgi
This package includes CGI programs for accessing UPS status via a web
browser.
 
%prep
%setup -q
# remove chown /var/lib/state so that we don't have to build rpms as root.
%patch0 -p1 -b .buildroot
%patch1 -p1 -b .config
%patch2 -p1 -b .conf

%build
%configure \
    --with-user=nobody \
    --with-group=nobody \
    --with-statepath=%{_localstatedir}/lib/ups \
    --sysconfdir=%{_sysconfdir}/ups \
    --with-cgipath=%{cgidir} \
    --with-modelpath=%{modeldir} \
    --with-linux-hiddev=/usr/include/linux/hiddev.h

make
make -C models hidups

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{modeldir}
make install install-cgi INSTALLROOT=%{buildroot}
install -m 755 models/hidups %{buildroot}%{modeldir}/hidups

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -m 755 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/ups

mkdir -p %{buildroot}%{_localstatedir}/lib/ups

# install SYSV init stuff
mkdir -p %{buildroot}%{initdir}
install -m 755 %{SOURCE1} %{buildroot}%{initdir}/ups

%post client
/sbin/chkconfig --add ups

%preun client
if [ "$1" = "0" ]; then
    /sbin/service ups stop > /dev/null 2>&1
    /sbin/chkconfig --del ups
fi

%postun client
if [ "$1" -ge "1" ]; then
    /sbin/service ups condrestart > /dev/null 2>&1
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING CREDITS CHANGES README docs
%config(noreplace) %attr(644,root,root) %{_sysconfdir}/sysconfig/ups
%{modeldir}/*
%{_sbindir}/upsd
%{_bindir}/upslog
%{_mandir}/man8/*

%files client
%defattr(-,root,root)
%attr(755,root,root) %{initdir}/ups
%config(noreplace) %{_sysconfdir}/ups/hosts.conf
%config(noreplace) %{_sysconfdir}/ups/multimon.conf
%config(noreplace) %attr(600,root,root) %{_sysconfdir}/ups/upsd.conf
%config(noreplace) %attr(600,root,root) %{_sysconfdir}/ups/upsd.users
%config(noreplace) %attr(600,root,root) %{_sysconfdir}/ups/upsmon.conf
%config(noreplace) %attr(600,root,root) %{_sysconfdir}/ups/upsset.conf
%config(noreplace) %attr(600,root,root) %{_sysconfdir}/ups/upssched.conf
%dir %attr(755,nobody,nobody) %{_localstatedir}/lib/ups
%{_bindir}/upsc
%{_bindir}/upscmd
%{_bindir}/upsct
%{_bindir}/upsct2
%{_sbindir}/upsmon
%{_sbindir}/upssched
%{_sbindir}/upssched-cmd
%{_mandir}/man5/*

%files cgi
%defattr(-,root,root)
%{cgidir}/*

%changelog
* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jun 02 2002 Than Ngo <than@redhat.com> 0.45.4-3
- fix forced shutdown (bug #65824, #60516)
- enable hidups driver
- add missing manages (bug #65188)

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Feb 26 2002 Than Ngo <than@redhat.com> 0.45.4-1
- update to 0.45.4

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Dec 14 2001 Than Ngo <than@redhat.com> 0.45.3-1
- update to 0.45.2
- fix bug #57417

* Mon Nov 27 2001 Than Ngo <than@redhat.com> 0.45.2-1
- update to 0.45.2
- clean up some patch files for 0.45.2

* Tue Jul 24 2001 Than Ngo <than@redhat.com> 0.45.0-3
- fix build dependencies (bug #49858)

* Fri Jul  6 2001 Than Ngo <than@redhat.com> 0.45.0-2
- rebuild

* Wed Jun 13 2001 Than Ngo <than@redhat.com>
- update to 0.45.0
- add some patches from alane@geeksrus.net (bug #44361, #44363)

* Sun Apr 22 2001 Than Ngo <than@redhat.com>
- add all available UPS drivers (Bug #36937)

* Fri Apr 13 2001 Than Ngo <than@redhat.com>
- update to 0.44.3 (Bug #35255)

* Fri Feb  9 2001 Than Ngo <than@redhat.com>
- fixed typo (Bug #26535)

* Tue Feb  6 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Fix some of the i18n
- make it exit cleanly if not configured

* Fri Jan 26 2001 Than Ngo <than@redhat.com>
- initscript internationalisation

* Thu Jan 11 2001 Than Ngo <than@redhat.com>
- fixed init script error (bug #23525)

* Sat Oct 21 2000 Than Ngo <than@redhat.com>
- update to 0.44.1

* Tue Aug 01 2000 Than Ngo <than@redhat.de>
- rebuilt with Michael changes

* Mon Jul 31 2000 Michael Stefaniuc <mstefani@redhat.com>
- changed /etc/sysconfig/ups to adress the changes in 0.44.0
- moved /etc/sysconfig/ups to the server package
- changed the initscript
- small config file patch

* Fri Jul 28 2000 Than Ngo <than@redhat.de>
- fixed initscripts so that condrestart doesn't return 1 when the test fails

* Mon Jul 24 2000 Than Ngo <than@redhat.de>
- nut CGIs is disable as default (Bug #14282)

* Tue Jul 18 2000 Than Ngo <than@redhat.de>
- update to 0.44.0
- inits back to rc.d/init.d, using service to fire them up

* Wed Jul 12 2000 Than Ngo <than@redhat.de>
- fix initscript and specfile, it should work with 6.x and 7.x
- add --with-statepath and --sysconfdir to %configure (thanks Michael)

* Sat Jul 08 2000 Than Ngo <than@redhat.de>
- add Prereq: /etc/init.d

* Tue Jun 27 2000 Than Ngo <than@redhat.de>
- don't prereq, only require initscripts

* Mon Jun 26 2000 Than Ngo <than@redhat.de>
- /etc/rc.d/init.d -> /etc/init.d
- prereq initscripts >= 5.20

* Fri Jun 16 2000 Bill Nottingham <notting@redhat.com>
- don't run by default

* Mon Jun 12 2000 Preston Brown <pbrown@redhat.com>
- adopted for Winston.  Use our new path macros.
- change nocgi pkg to a cgi pkg (inclusive rather than exclusive).
- new init script

* Sat May 06 2000 <bo-rpm@vircio.com> (0.43.2-1)
- Updated Package to new release

* Thu Jan 20 2000 <bo-rpm@vircio.com> (0.42.2-1)
- Updated package to new release
- Dropped bestups patch since that is fixed in 0.42.2

* Sat Dec 18 1999 <bo-rpm@vircio.com> (0.42.1-4)
- Package now uses chkconfig

* Sat Dec 18 1999 <bo-rpm@vircio.com> (0.42.1-3)
- applied an improved patch to deal with the 
  bestups string length issue.

* Sat Dec 11 1999 <bo-rpm@vircio.com> (0.42.1-1)
- fixed string length in bestups.c line 279.

* Sat Dec 11 1999 <bo-rpm@vircio.com> (0.42.1-1)
- upgraded package to 0.42.1 from 0.42.0

* Mon Dec 6 1999 <bo-rpm@vircio.com> (0.42.0-8)
- added requirement of nut-client for nut.

* Mon Dec 6 1999 <bo-rpm@vircio.com> (0.42.0-7)
- removed overlapping files between the nut and nut-client rpms

* Mon Nov 23 1999 <bo-rpm@vircio.com> (0.42.0-6)
- stop ups before uninstalling

* Mon Nov 23 1999 <bo-rpm@vircio.com> (0.42.0-5)
- build against gd 1.6.3

* Thu Nov 03 1999 <bo-rpm@vircio.com> (0.42.0-4)
- Initial build of nut (well almost).
- Removed chmod from the make file so that the package
  does not have to be built as root.....
