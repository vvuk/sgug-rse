%global _buildshell /usr/sgug/bin/bash

%global lua_53_version 5.3
%global lua_53_incdir %{_includedir}/lua-%{lua_53_version}
%global lua_53_libdir %{_libdir}/lua/%{lua_53_version}
%global lua_53_pkgdir %{_datadir}/lua/%{lua_53_version}
%global lua_53_builddir obj-lua53

%global lua_51_version 5.1
%global lua_51_incdir %{_includedir}/lua-%{lua_51_version}
%global lua_51_libdir %{_libdir}/lua/%{lua_51_version}
%global lua_51_pkgdir %{_datadir}/lua/%{lua_51_version}
%global lua_51_builddir obj-lua51

%global real_version 1.36.0
%global extra_version 0

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  libuv-devel
BuildRequires:  lua >= %{lua_53_version}
BuildRequires:  lua-devel >= %{lua_53_version}
BuildRequires:  compat-lua >= %{lua_51_version}
BuildRequires:  compat-lua-devel >= %{lua_51_version}
BuildRequires:  lua5.1-compat53

Name:           lua-luv
Version:        %{real_version}.%{extra_version}
Release:        0%{?dist}

License:        ASL 2.0
Summary:        Bare libuv bindings for lua
Url:            https://github.com/luvit/luv

Requires:       lua(abi) = %{lua_53_version}

Source0:        https://github.com/luvit/luv/archive/%{real_version}-%{extra_version}/luv-%{version}.tar.gz

%if 0%{?el8}
# libuv-devel is from the CentOS Devel repo, only available on
# aarch64, ppc64le, and x86_64:
# https://mirrors.edge.kernel.org/centos/8-stream/Devel/
# bz# 1829151
ExcludeArch:    s390x
%endif

%description
This library makes libuv available to lua scripts. It was made
for the luvit project but should usable from nearly any lua
project.

The library can be used by multiple threads at once. Each thread
is assumed to load the library from a different lua_State. Luv
will create a unique uv_loop_t for each state. You can't share uv
handles between states/loops.

The best docs currently are the libuv docs themselves. Hopefully
soon we'll have a copy locally tailored for lua.

%package devel
Summary:        Development files for lua-luv
Requires:       lua-luv%{?_isa} = %{version}-%{release}

%description devel
Files required for lua-luv development

%package -n lua5.1-luv
Summary:        Bare libuv bindings for lua 5.1
Requires:       lua(abi) = %{lua_51_version}

%description -n lua5.1-luv
This library makes libuv available to lua scripts. It was made
for the luvit project but should usable from nearly any lua
project.

The library can be used by multiple threads at once. Each thread
is assumed to load the library from a different lua_State. Luv
will create a unique uv_loop_t for each state. You can't share uv
handles between states/loops.

The best docs currently are the libuv docs themselves. Hopefully
soon we'll have a copy locally tailored for lua.

%package -n lua5.1-luv-devel
Summary:        Development files for lua5.1-luv
Requires:       lua5.1-luv%{?_isa} = %{version}-%{release}

%description -n lua5.1-luv-devel
Files required for lua5.1-luv development

%prep
%autosetup -p1 -n luv-%{real_version}-%{extra_version}

# Remove bundled dependencies
rm -rf deps

# Remove network sensitive tests gh#luvit/luv#340
rm -f tests/test-dns.lua

%build
# lua
mkdir %{lua_53_builddir}

pushd %{lua_53_builddir}
%cmake .. \
    -DWITH_SHARED_LIBUV=ON \
    -DBUILD_MODULE=ON \
    -DBUILD_SHARED_LIBS=ON \
    -DWITH_LUA_ENGINE=Lua \
    -DLUA_BUILD_TYPE=System \
    -DINSTALL_LIB_DIR=%{_libdir}

%make_build
popd

# lua-compat
mkdir %{lua_51_builddir}

pushd %{lua_51_builddir}
%cmake .. \
    -DWITH_SHARED_LIBUV=ON \
    -DBUILD_MODULE=ON \
    -DBUILD_SHARED_LIBS=ON \
    -DWITH_LUA_ENGINE=Lua \
    -DLUA_BUILD_TYPE=System \
    -DINSTALL_LIB_DIR=%{_libdir} \
    -DLUA_COMPAT53_DIR=%{lua_51_incdir} \
    -DLUA_INCLUDE_DIR=%{lua_51_incdir} \
    -DLUA_LIBRARY=%{_libdir}/liblua-%{lua_51_version}.so

%make_build
popd

%install
# lua-5.3
install -d -m 0755 %{buildroot}%{lua_53_libdir}
install -m 0755 -p %{lua_53_builddir}/luv.so %{buildroot}%{lua_53_libdir}/luv.so

install -d -m 0755 %{buildroot}%{lua_53_incdir}/luv
for f in lhandle.h lreq.h luv.h util.h; do
    install -m 0644 -p src/$f %{buildroot}%{lua_53_incdir}/luv/$f
done

# lua-5.1
install -d -m 0755 %{buildroot}%{lua_51_libdir}
install -m 0755 -p %{lua_51_builddir}/luv.so %{buildroot}%{lua_51_libdir}/luv.so

install -d -m 0755 %{buildroot}%{lua_51_incdir}/luv
for f in lhandle.h lreq.h luv.h util.h; do
    install -m 0644 -p src/$f %{buildroot}%{lua_51_incdir}/luv/$f
done

%check
# lua-5.1
ln -sf %{lua_51_builddir}/luv.so luv.so
lua-5.1 tests/run.lua
rm luv.so

%files
%doc README.md
%license LICENSE.txt
%{lua_libdir}/luv.so

%files devel
%dir %{lua_53_incdir}
%dir %{lua_53_incdir}/luv/
%{lua_53_incdir}/luv/lhandle.h
%{lua_53_incdir}/luv/lreq.h
%{lua_53_incdir}/luv/luv.h
%{lua_53_incdir}/luv/util.h

%files -n lua5.1-luv
%doc README.md
%license LICENSE.txt
%{lua_51_libdir}/luv.so

%files -n lua5.1-luv-devel
%dir %{lua_51_incdir}
%dir %{lua_51_incdir}/luv/
%{lua_51_incdir}/luv/lhandle.h
%{lua_51_incdir}/luv/lreq.h
%{lua_51_incdir}/luv/luv.h
%{lua_51_incdir}/luv/util.h

%changelog
* Tue Apr 28 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 1.36.0.0-1
- Update to version 1.36.0-0
- Support building on EPEL 8

* Sat Feb 29 2020 Andreas Schneider <asn@redhat.com> - 1.34.2.1-1
-  Update to version 1.34.2-1
  - https://github.com/luvit/luv/releases/tag/1.34.2-0
  - https://github.com/luvit/luv/releases/tag/1.34.2-1

* Tue Jan 21 2020 Andreas Schneider <asn@redhat.com> - 1.34.1.1-0
- Update to version 1.34.1-1

* Tue Oct 29 2019 Andreas Schneider <asn@redhat.com> - 1.32.0.0-0
- Update to version 1.32.0-0

* Tue Oct 01 2019 Andreas Schneider <asn@redhat.com> - 1.30.1.1-5
- Fixed versioning

* Tue Oct 01 2019 Andreas Schneider <asn@redhat.com> - 1.30.1-4.1
- Update to version 1.30.1-1
- Removed luv-1.30-include_lua_header.patch
- Added missing Requires for devel packages
- Fixed source URL
- Fixed license
- Preserved timestamps

* Mon Sep 30 2019 Andreas Schneider <asn@redhat.com> - 1.30.1-3
- Fixed BR for lua 5.3

* Mon Sep 30 2019 Andreas Schneider <asn@redhat.com> - 1.30.1-2
- Added BR for gcc
- Renamed lua globals

* Tue Sep 24 2019 Andreas Schneider <asn@redhat.com> - 1.30.1-1
- Initial version 1.30.1-0
