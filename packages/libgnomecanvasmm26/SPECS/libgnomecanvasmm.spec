Name:           libgnomecanvasmm26
Version:        2.26.0

# yes, this is ugly
%global major_minor_version %(echo "%version" | sed "s|^\\([^\\.]*\\.[^\\.]*\\).*$|\\1|")

Release:        23%{?dist}

Summary:        C++ interface for Gnome libs (a GUI library for X)

License:        LGPLv2+
URL:            http://www.gtkmm.org/
Source0:        http://ftp.gnome.org/pub/GNOME/sources/libgnomecanvasmm/%{major_minor_version}/libgnomecanvasmm-%{version}.tar.bz2

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gtkmm24-devel >= 2.4.0
BuildRequires:  libgnomecanvas-devel >= 2.6.0

%description
This package provides C++ wrappers for libgnomecanvas, for use with gtkmm.

%package devel
Summary:        Headers for developing programs that will use %{name}.
Requires:       %{name} = %{version}-%{release}
Requires:       gtkmm24-devel
Requires:       libgnomecanvas-devel

%description devel
This package contains the headers that programmers will need to
develop applications which will use %{name}.

%prep
%setup -q -n libgnomecanvasmm-%{version}


%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf %buildroot
make DESTDIR=${RPM_BUILD_ROOT} install
find %buildroot -type f -name "*.la" -exec rm -f {} ';'


#%%ldconfig_scriptlets


%files
%defattr(-, root, root, -)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root, -)
%{_includedir}/libgnomecanvasmm-2.6
%{_libdir}/*.so
%{_libdir}/libgnomecanvasmm-2.6
%{_libdir}/pkgconfig/*.pc

%changelog
* Sat Aug 22 2020  HAL <notes2@gmx.de> - 2.26.0-23
- compiles on Irix 6.5 with sgug-rse gcc 9.2.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.26.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.26.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.26.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 20 2018 Nils Philippsen <nils@tiptoe.de> - 2.26.0-20
- require gcc, gcc-c++ for building

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.26.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.26.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.26.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.26.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.26.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.26.0-12
- Rebuilt for GCC 5 C++11 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 10 2012 Nils Philippsen <nils@redhat.com> - 2.26.0-6
- rebuild for gcc 4.7

* Mon Nov 07 2011 Nils Philippsen <nils@redhat.com> - 2.26.0-5
- rebuild (libpng)

* Wed Jul 13 2011 Nils Philippsen <nils@redhat.com> - 2.26.0-4
- drop unknown configure option "--enable-docs"
- scriptlets: use ldconfig directly rather than via shell
- use %%buildroot macro rather than $RPM_BUILD_ROOT
- fix descriptions
- fix source URL

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.26.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr  6 2009 Denis Leroy <denis@poolshark.org> - 2.26.0-1
- Update to upstream 2.26.0

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.23.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Aug 29 2008 Denis Leroy <denis@poolshark.org> - 2.23.1-1
- Update to upstream 2.23.1

* Wed Mar 12 2008 Denis Leroy <denis@dedibox.albator.org> - 2.22.0-1
- Update to upstream 2.22.0

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.20.0-2
- Autorebuild for GCC 4.3

* Mon Sep 17 2007 Denis Leroy <denis@poolshark.org> - 2.20.0-1
- Update to new stable branch 2.20

* Tue Aug 28 2007 Stepan Kasal <skasal@redhat.com> - 2.16.0-3
- Fix typo in description.

* Mon Aug 28 2006 Denis Leroy <denis@poolshark.org> - 2.16.0-2
- FE6 Rebuild

* Mon Aug 21 2006 Denis Leroy <denis@poolshark.org> - 2.16.0-1
- Update to 2.16.0

* Thu Mar 23 2006 Denis Leroy <denis@poolshark.org> - 2.14.0-1
- Update to 2.14.0

* Tue Feb 28 2006 Denis Leroy <denis@poolshark.org> - 2.12.0-3
- Rebuild

* Fri Nov 25 2005 Denis Leroy <denis@poolshark.org> - 2.12.0-2
- Disabled static libraries

* Mon Sep 19 2005 Denis Leroy <denis@poolshark.org> - 2.12.0-1
- Update to 2.12.0

* Thu Apr 28 2005 Denis Leroy <denis@poolshark.org> - 2.10.0-1
- Upgrade to 2.10.0

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Mon Jun 27 2004 Denis Leroy <denis@poolshark.org> - 0:2.6.1-0.fdr.1
- Upgrade to 2.6.1

* Sun Dec 21 2003 Eric Bourque <ericb@computer.org>
- fixed dependency to gtkmm2 instead of gtkmm

* Thu Sep 25 2003 Eric Bourque <ericb@computer.org>
- updated for libgnomecanvasmm-2.0

* Tue Mar 20 2001 Eric Bourque <ericb@computer.org>
- added gnome--.m4 to files devel section

* Sat Mar 10 2001 Herbert Valerio Riedel <hvr@gnu.org>
- improved examples.conf
- fixed example build problems

* Thu May 11 2000 Herbert Valerio Riedel <hvr@gnu.org>
- removed lib/gtkmm from files section
- removed empty obsolete tags

* Sun Jan 30 2000 Karl Einar Nelson <kenelson@sourceforge.net>
- adapted from gtk--.spec
