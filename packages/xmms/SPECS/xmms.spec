Name:           xmms
Version:        1.2.11
Release:        37.20071117cvs%{?dist}
Epoch:          1
Summary:        The X MultiMedia System, a media player

License:        GPLv2+
URL:            http://legacy.xmms2.org/
# http://www.xmms.org/download.php, to recreate the tarball:
# $ wget http://legacy.xmms2.org/xmms-1.2.11.tar.bz2
# $ tar jx --exclude "mpg123*" -f xmms-1.2.11.tar.bz2
# $ tar jcf xmms-1.2.11.patched.tar.bz2 xmms-1.2.11
Source0:        %{name}-%{version}-20071117cvs.patched.tar.bz2
Source1:        xmms.sh
Source2:        xmms.xpm
# MP3 decode support is now natively supported in Fedora (again).
# If the CVS code for xmms still existed, we'd just make a new source0
# But it doesn't. So I copied the Input/mpg123 files from xmms-1.2.11.
Source3:	xmms-1.2.11-mpg123.tar.bz2
Source4:        xmms.desktop
# http://cvs.xmms.org/cvsweb.cgi/xmms/General/joystick/joy.c.diff?r1=1.8&r2=1.9
Patch1:         %{name}-1.2.6-audio.patch
Patch2:         %{name}-1.2.6-lazy.patch
Patch3:         %{name}-1.2.8-default-skin.patch
Patch5:         %{name}-1.2.11-arts.patch
Patch6:         %{name}-1.2.11-alsalib.patch
Patch7:         %{name}-cd-mountpoint.patch
Patch8:         %{name}-1.2.11-multilib.patch
Patch9:		%{name}-play.patch
Patch11:        %{name}-1.2.10-gcc4.patch
# From xmms-crossfade-0.3.14/patches/ adapted from 1.2.10 to 1.2.11
Patch12:        %{name}-1.2.11-is_quitting.patch
Patch14:	%{name}-1.2.10-configfile-safe-write.patch
Patch15:	%{name}-1.2.10-reposition.patch
Patch16:	%{name}-1.2.11-dso.patch
Patch17:	xmms-1.2.10-ubuntu-CVE-2007-0653.patch
Patch18:	xmms-alsa-fix-loop.patch
Patch19:	xmms-1.2.11-mikmod-fix.patch
Patch20:	xmms-1.2.11-a-b.patch

# This plugin is gone. Esound is gone. 2001 is gone.
Provides:	xmms-esd = %{epoch}:%{version}-%{release}
Obsoletes:	xmms-esd < 1:18.20071117cvs

BuildRequires:  gcc
BuildRequires:  gtk+-devel
#BuildRequires:  arts-devel
#BuildRequires:  alsa-lib-devel
BuildRequires:  libogg-devel
BuildRequires:  libvorbis-devel
BuildRequires:  mikmod-devel
BuildRequires:  gettext-devel
BuildRequires:  zlib-devel
#BuildRequires:  libGL-devel
#BuildRequires:  libXt-devel
BuildRequires:  libSM-devel
BuildRequires:  libXxf86vm-devel
BuildRequires:  desktop-file-utils

Requires:       unzip libcanberra-gtk2 gtk2
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

# Skin packages can require this from xmms and all GUI compatible players
Provides:       xmms-gui

%description
XMMS is a multimedia (Ogg Vorbis, CDs) player for the X Window System
with an interface similar to Winamp's.  XMMS supports playlists and
streaming content and has a configurable interface.

%package        libs
Summary:        XMMS engine and core plugins
# mp3 is back
Provides:       xmms-mp3 = %{version}-%{release}
Obsoletes:      xmms-mp3 < 1.2.11-8
Provides:	bundled(libmpg123)

%description    libs
The X MultiMedia System player engine and core plugins.

%package        devel
Summary:        Files required for XMMS plug-in development
Requires:       %{name}-libs = %{epoch}:%{version}-%{release}
Requires:       gtk+-devel
Requires:       pkgconfig 

%description    devel
Files needed for building plug-ins for the X MultiMedia System.


%prep
%setup -q -n %{name}-%{version}-20071117cvs -a 3
# Set default output plugin to ALSA
%patch1 -p1 -b .audio
# Use RTLD_LAZY, not RTLD_NOW
%patch2 -p1 -b .lazy
# Change the default skin
%patch3 -p1 -b .default-skin
# Link arts dynamically and detect its presence for choosing output plugin
%patch5 -p1 -b .arts
# Don't link *everything* against alsa-lib
%patch6 -p1 -b .alsalib
# Use something that's more likely to work as the default cdrom mountpoint
%patch7 -p0 -b .cd-mountpoint
# Avoid multilib devel conflicts
%patch8 -p1 -b .multidevel
# Fix for crossfade >= 0.3.14 to work properly
%patch12 -p1 -b .crossfade
# Randomize playlists better
%patch14 -p1
%patch15 -p1
%patch9 -p1 -b .playonclick
%patch16 -p1 -b .dso
%patch17 -p1 -b .CVE-2007-0653
%patch18 -p1 -b .fix-loop
%patch19 -p1 -b .mikmod-fix
%patch20 -p1 -b .ab
perl -pi -e "s|#include <kde/artsc/artsc.h>||g" %{_builddir}/xmms-1.2.11-20071117cvs/xmms/main.c
# Avoid standard rpaths on lib64 archs, --disable-rpath doesn't do it
sed -i -e 's|"/lib /usr/lib"|"/%{_lib} %{_libdir}"|' configure

for f in AUTHORS ChangeLog README ; do
    iconv -f iso-8859-1 -t utf-8 > $f.utf8 $f ; mv $f.utf8 $f
done

%build
%configure \
    --disable-dependency-tracking \
    --enable-kanji \
    --enable-texthack \
    --disable-ipv6 \
    --with-pic \
    --enable-esd \
    --disable-static
# causes problems with dso linking
#find . -name Makefile | xargs sed -i -e s/-lpthread//g # old libtool, x86_64
make
# smp_flags removed due to build issues

%install
make install DESTDIR=%{buildroot}
install -dm 755 %{buildroot}%{_datadir}/xmms/Skins
find %{buildroot} -name "*.la" | xargs rm -f

# Fix translation directory
mv %{buildroot}/%{_datadir}/locale/sr@Latn %{buildroot}/%{_datadir}/locale/sr@latin

# On FC5 x86_64, some get created even though we pass --disable-static
rm -f %{buildroot}%{_libdir}/xmms/*/*.a

# https://bugzilla.redhat.com/213172
for bin in xmms wmxmms ; do
    install -Dpm 755 %{buildroot}%{_bindir}/$bin \
        %{buildroot}%{_libexecdir}/$bin
    sed -e "s|/usr/libexec/xmms|%{_libexecdir}/$bin|" %{SOURCE1} > \
        %{buildroot}%{_bindir}/$bin
    chmod 755 %{buildroot}%{_bindir}/$bin
done

# Desktop menu entry
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE4}
# Desktop menu icon
install -Dpm 644 %{SOURCE2} \
    %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/xmms.xpm

install -Dpm 644 xmms.pc %{buildroot}%{_libdir}/pkgconfig/xmms.pc

%find_lang %{name}

#%%ldconfig_scriptlets libs

%if 0%{?rhel} && 0%{?rhel} <= 7
%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ]; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    update-desktop-database &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database &>/dev/null || :
%endif

%files -f %{name}.lang
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS ChangeLog FAQ NEWS TODO README README.ab
%{_bindir}/xmms
%{_bindir}/wmxmms
%{_libexecdir}/xmms
%{_libexecdir}/wmxmms
%{_datadir}/applications/xmms.desktop
%{_datadir}/icons/hicolor/*x*/apps/xmms.xpm
%{_datadir}/xmms/
%{_mandir}/man1/*xmms.1*

%files libs
%license COPYING
%{_libdir}/libxmms.so.*
%dir %{_libdir}/xmms/
%{_libdir}/xmms/Effect/
%{_libdir}/xmms/General/
%{_libdir}/xmms/Input/
%dir %{_libdir}/xmms/Output/
#%%{_libdir}/xmms/Output/libALSA.so
%{_libdir}/xmms/Output/libesdout.so
%{_libdir}/xmms/Output/libOSS.so
%{_libdir}/xmms/Output/libdisk_writer.so
%{_libdir}/xmms/Visualization/

%files devel
%{_bindir}/xmms-config
%{_includedir}/xmms/
%{_libdir}/libxmms.so
%{_datadir}/aclocal/xmms.m4
%{_libdir}/pkgconfig/xmms.pc


%changelog
* Tue Dec 29 2020  HAL <notes2@gmx.de> - 1:1.2.11-37.20071117cvs
- builds on Irix 6.5 with sgug-rse gcc 9.2. 

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.11-37.20071117cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.11-36.20071117cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.11-35.20071117cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.11-34.20071117cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:1.2.11-33.20071117cvs
- Remove obsolete scriptlets

* Fri Sep  1 2017 Tom Callaway <spot@fedoraproject.org> - 1:1.2.11-32.20071117cvs
- apply a-b patch from Oden Eriksson (bz1480259)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.11-31.20071117cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.11-30.20071117cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.11-29.20071117cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 16 2017 Tom Callaway <spot@fedoraproject.org> - 1:1.2.11-28.20071117cvs
- Add Provides for bundled libmpg123. xmms doesn't really have a good way to use
  a system copy here, because it is older than dinosaurs.

* Fri Nov 18 2016 Tom Callaway <spot@fedoraproject.org> - 1:1.2.11-27.20071117cvs
- mp3 is back, baby!

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.2.11-26.20071117cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jul 15 2015 Ville Skyttä <ville.skytta@iki.fi> - 1:1.2.11-25.20071117cvs
- Desktop entry: Add more module format associations, fix some warnings
- Mark COPYING as %%license where available

* Wed Jul  8 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1:1.2.11-24.20071117cvs
- Drop obsolete at-spi dependency

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.11-23.20071117cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.11-22.20071117cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.11-21.20071117cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 11 2014 Tom Callaway <spot@fedoraproject.org> - 1:1.2.11-20.20071117cvs
- fix mikmod support (thanks to Ozkan Sezer)
- fix serbian translation dir (thanks to Mike FABIAN)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.11-19.20071117cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Tom Callaway <spot@fedoraproject.org> - 1:1.2.11-18.20071117cvs
- drop esound support (esound is dead dead dead)

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.11-17.20071117cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.11-16.20071117cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 15 2011 Tom Callaway <spot@fedoraproject.org> - 1:1.2.11-15.20071117cvs
- fix alsa plugin loop code to, well, stop looping when the track is done
- fix desktop file to enqueue and play files
- add patch from Ubuntu for CVE-2007-0653

* Thu Jul 14 2011 Tom Callaway <spot@fedoraproject.org> - 1:1.2.11-14.20071117cvs
- fix url (bz 672011)

* Thu Jul 14 2011 Tom Callaway <spot@fedoraproject.org> - 1:1.2.11-13.20071117cvs
- minor spec cleanup and rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.11-12.20071117cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Feb 20 2010 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1:1.2.11-11.20071117cvs
- DSO linking fix

* Wed Dec  9 2009 Matthias Saou <http://freshrpms.net/> 1:1.2.11-10.20071117cvs
- Include xmms.desktop, taken from redhat-audio-player.desktop which is no
  longer provided by any package (it was about time).
- Update scriplets to what I understand is best from ScriptletSnippets page.
  
* Wed Sep 23 2009 Rex Dieter <rdieter@fedoraproject.org> 1:1.2.11-9.20071117cvs
- optimize desktop/icon scriptlets

* Mon Sep 14 2009 Matthias Saou <http://freshrpms.net/> 1:1.2.11-8.20071117cvs
- Update crossfade patch to the latest version (#518176).

* Wed Sep 02 2009 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1:1.2.11-7.20071117cvs
- Fix play on click bug (BZ434692)

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.11-6.20071117cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Apr 12 2009 Matthias Saou <http://freshrpms.net/> 1:1.2.11-5.20071117cvs
- Add "xmms-gui" provides, to be required from xmms-skins package (#470135).

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.2.11-4.20071117cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.11-20071117cvs-3
- Fix multilib patch

* Thu Sep 18 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.11-20071117cvs-2
- Additional requires

* Wed Sep 10 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.11-20071117cvs-1.1
- Reverted license to gplv2+ (oopsy!)

* Tue Sep 02 2008 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1.2.11-20071117cvs-1
- Bump to 1.2.11 devel branch
- Alter license
- Removed unused patches
- Fixed old patches to work with new version

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1:1.2.10-38
- Autorebuild for GCC 4.3

* Mon Feb 18 2008 Jesse Keating <jkeating@redhat.com> - 1.2.10-37
- Rebuild for new mikmod

* Fri Apr 13 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1:1.2.10-36
- add back in the .pc file

* Sun Apr 01 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1:1.2.10-35
- added CVE fix for buffer problem

* Sat Mar 10 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1:1.2.10-34
- built from cvs tarball (amended to remove mp3)

* Fri Jan 19 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1:1.2.10-32
- removed R xmms in libs

* Thu Jan 18 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1:1.2.10-31
- fixes for repositioning on mode change and .xmms file

* Mon Jan  1 2007 Paul F. Johnson <paul@all-the-johnsons.co.uk> 1:1.2.10-30
- new package owner
- added R to libs package
- rebuild

* Mon Nov  6 2006 Ville Skyttä <ville.skytta at iki.fi> - 1:1.2.10-29
- Work around incompatibilities with the Composite X extension (#213172).
- Apply upstream playlist randomization improvements (#188603).

* Mon Aug 28 2006 Ville Skyttä <ville.skytta at iki.fi> - 1:1.2.10-28
- Rebuild.

* Wed Jun 21 2006 Ville Skyttä <ville.skytta at iki.fi> - 1:1.2.10-27
- Split EsounD output plugin into -esd subpackage, don't filter dependencies.
- Make menu entry symlink relative.
- Re-enable parallel make.

* Wed Jun  7 2006 Jeremy Katz <katzj@redhat.com> - 1:1.2.10-26
- don't use parallel make to try to stop the build hang

* Thu May 25 2006 Ville Skyttä <ville.skytta at iki.fi> - 1:1.2.10-25
- Avoid multilib conflicts in -devel, introducing xmms.pc.
- Include license text in -libs.

* Tue May 23 2006 Ville Skyttä <ville.skytta at iki.fi> - 1:1.2.10-24
- Apply upstream fix for joystick plugin crashes.

* Thu Apr  6 2006 Ville Skyttä <ville.skytta at iki.fi> - 1:1.2.10-23
- Split library and plugins to xmms-libs (#184606).
- ALSA is ubiquitous, don't filter dependencies to it.
- Avoid standard rpaths on lib64 archs.
- Tighten versioned -devel dependency to -libs.
- Drop no longer needed Obsoletes.
- Install icon to %%{_datadir}/icons.
- Convert docs to UTF-8.
- Specfile rewrite/cleanup.
- Drop bogus Source0 URL.
- Don't use %%exclude.

* Thu Mar  2 2006 Matthias Saou <http://freshrpms.net/> 1:1.2.10-22
- Remove /usr/lib64/xmms/General/libsong_change.a (fix for FC5 x86_64...).

* Mon Feb 13 2006 Matthias Saou <http://freshrpms.net/> 1:1.2.10-21
- Remove gtk libs from xmms-config output, as they are only really needed for
  static linking, which we no longer support (#182267).
- Disable static in %%configure instead of excluding the built file.
- Add conditional modular X build requirements.

* Mon Feb 13 2006 Matthias Saou <http://freshrpms.net/> 1:1.2.10-20
- Spec file cleanup.
- Include crossfade 0.3.9 patch.
- Remove very old x11amp obsoletes.
- Exclude static libraries, update devel summary and description for it.
- List all plugins directories in order to be aware of breakage if the
  libtool problem ever happens again.
- Fix post/postun scriplets.
- Remove xmms_logo.xpm and xmms_mini.xpm, they should be unused.
- Add libXt-devel to fullfill the "checking for X..." configure check.
- Add gettext-devel to make more configure checks happy.

* Wed Dec 28 2005 Hans de Goede <j.w.r.degoede@hhs.nl>  1:1.2.10-19
- Remove -lpthread from all LDFLAGS as this confuses the old libtool
  used by xmms on x86_64 (FE-bug #175493)
- Add missing modular Xorg BuildReqs, this (re)enables session managment
  support and the openGL plugins.

* Tue Dec 20 2005 Matthias Saou <http://freshrpms.net/> 1:1.2.10-18.1
- Update gcc4 patch to include fix for xmms.org bug #1730, fixes FC5 build.

* Sat May 28 2005 Matthias Saou <http://freshrpms.net/> 1:1.2.10-18
- Build with explicit --with-pic to fix compilation of flac plugin on
  x86_64.

* Thu May  5 2005 Matthias Saou <http://freshrpms.net/> 1:1.2.10-17
- Don't have scriplets fail if update-desktop-database returns an error.

* Sat Apr 30 2005 Ville Skyttä <ville.skytta at iki.fi> - 1:1.2.10-16
- Use /media/cdrecorder as the default CDROM mountpoint for the CD audio
  plugin, it's more likely to work nowadays than /mnt/cdrom.
- Drop no longer needed skins tarball.
- Build with dependency tracking disabled.

* Fri Apr 15 2005 Matthias Saou <http://freshrpms.net/> 1:1.2.10-15
- Change main icon from xpm to png (smaller, more consistent).
- Split off the aRts plugin.
- Split off the skins at last, as noarch (#65614).
- Remove generic INSTALL instructions.
- Remove autoconf and automake build reqs, as they're no longer called.
- Remove unneeded glib2-devel build req.

* Wed Apr  6 2005 Seth Vidal <skvidal at phy.duke.edu> 1:1.2.10-14
- put back conflict

* Wed Apr  6 2005 Seth Vidal <skvidal at phy.duke.edu> 1:1.2.10-13
- clean up spec file a bit.
- remove everything except for the last 2 yrs of changelog entries.
- make things match Fedora Extras Packaging Guidelines more

* Wed Apr  6 2005 Seth Vidal <skvidal at phy.duke.edu> 1:1.2.10-12
- Apply patch from David Hill RH bz: 152138

* Thu Mar 24 2005 David Hill <djh[at]ii.net> 1:1.2.10-12
- Add gcc4 patch

* Wed Jan 05 2005 Colin Walters <walters@redhat.com> 1:1.2.10-11
- Change BR on mikmod to mikmod-devel (138057)

* Tue Nov 23 2004 Colin Walters <walters@redhat.com> 1:1.2.10-10
- Add xmms-alsa-backport.patch (bug 140565, John Haxby)

* Wed Oct 13 2004 Colin Walters <walters@redhat.com> 1:1.2.10-9
- Correct update-desktop-database correction for postun

* Wed Oct 13 2004 Colin Walters <walters@redhat.com> 1:1.2.10-8
- Call update-desktop-database on correct directory

* Mon Oct 04 2004 Colin Walters <walters@redhat.com> 1:1.2.10-7
- PreReq desktop-file-utils 0.9
- Run update-desktop-database

* Sun Aug 15 2004 Tim Waugh <twaugh@redhat.com> 1:1.2.10-6
- Fixed another underquoted m4 definition.

* Thu Jul 15 2004 Tim Waugh <twaugh@redhat.com> 1:1.2.10-5
- Fixed warnings in shipped m4 file.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May 31 2004 Warren Togami <wtogami@redhat.com> 1:1.2.10-3.p
- #124701 -devel req gtk+-devel

* Thu Mar 11 2004 Bill Nottingham <notting@redhat.com> 1:1.2.10-2.p
- update to 1.2.10
- fix buildreqs (#114857)
- switch default output plugin to ALSA

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 23 2004 Than Ngo <than@redhat.com> 1:1.2.9-5.p
- enable arts plugin, it should work with arts-1.2.0-1.5 or newer.

* Sat Feb 14 2004 Than Ngo <than@redhat.com> 1:1.2.9-4.p
- disable xmms-1.2.8-arts.patch

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 28 2004 Bill Nottingham <notting@redhat.com> 1:1.2.9-2.p
- enable ipv6 (#105774)

* Wed Jan 28 2004 Bill Nottingham <notting@redhat.com> 1:1.2.9-1.p
- update to 1.2.9

* Fri Dec 12 2003 Bill Nottingham <notting@redhat.com> 1:1.2.8-4.p
- rebuild, pick up alsa plugin

* Wed Oct 22 2003 Bill Nottingham <notting@redhat.com> 1:1.2.8-3.p
- fix dependency blacklisting (corollary of #100917)

* Mon Oct 13 2003 Than Ngo <than@redhat.com> 1:1.2.8-2.p
- workaround to fix arts crash

* Mon Sep  8 2003 Bill Nottingham <notting@redhat.com> 1:1.2.8-1.p
- update to 1.2.8
- clean out now-upstream stuff (Welsh po file, other patches)
- switch to Håvard's arts plugin, tweak it's default buffer size
- don't explicitly require trademarked skin name (#84554)

* Mon Jun 30 2003 Bill Nottingham <notting@redhat.com> 1:1.2.7-23.p
- add welsh po file (#98244)

* Sun Jun  8 2003 Tim Powers <timp@redhat.com> 1:1.2.7-22.1.p
- built for RHEL

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Jeff Johnson <jbj@redhat.com>
- add explicit epoch's where needed.
