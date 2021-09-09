# hack for sgug -- pretend to be fedora so we take the right paths
%global fedora 1

%{!?luaver: %global luaver %(lua -e "print(string.sub(_VERSION, 5))" || echo 0)}
%global luapkgdir %{_datadir}/lua/%{luaver}
%global lualibdir %{_libdir}/lua/%{luaver}
%global luaincdir %{_includedir}/lua-%{luaver}

%global luacompatver 5.1
%global luacompatpkgdir %{_datadir}/lua/%{luacompatver}
%global luacompatlibdir %{_libdir}/lua/%{luacompatver}
%global luacompatincdir %{_includedir}/lua-%{luacompatver}

%if 0%{?fedora} || 0%{?rhel} > 7
%global lualib lua-%{luacompatver}
%else
%global lualib lua
%endif

%global luapkgname compat53

Name:           lua-%{luapkgname}
Version:        0.7
Release:        3%{?dist}
Summary:        Compatibility module providing Lua-5.3-style APIs for Lua %{luacompatver}

License:        MIT
URL:            https://github.com/keplerproject/lua-compat-5.3
Source0:        https://github.com/keplerproject/lua-compat-5.3/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  pkgconfig
%if 0%{?fedora} || 0%{?rhel} > 7
BuildRequires:  compat-lua-devel >= %{luacompatver}
%else
BuildRequires:  lua-devel >= %{luaver}
%endif

%if 0%{?rhel} == 7
Requires:       lua >= %{luaver}
%endif

%description
This is a small module that aims to make it easier to write code in a
Lua-5.3-style that is compatible with Lua 5.1, Lua 5.2, and Lua 5.3. This does
not make Lua 5.2 (or even Lua 5.1) entirely compatible with Lua 5.3, but it
brings the API closer to that of Lua 5.3.

%if 0%{?fedora} || 0%{?rhel} > 7
%package -n lua%{luacompatver}-%{luapkgname}
Summary:        Compatibility module providing Lua-5.3-style APIs for Lua %{luacompatver}
Requires:       lua(abi) = %{luacompatver}

%description -n lua%{luacompatver}-%{luapkgname}
This is a small module that aims to make it easier to write code in a
Lua-5.3-style that is compatible with Lua 5.1, Lua 5.2, and Lua 5.3. This does
not make Lua 5.2 (or even Lua 5.1) entirely compatible with Lua 5.3, but it
brings the API closer to that of Lua 5.3.
%endif

%prep
%setup -q -n lua-compat-5.3-%{version}

%build
CFLAGS="%{?optflags} -fPIC $(pkg-config --cflags %{lualib})"
LDFLAGS="%{?build_ldflags} $(pkg-config --libs %{lualib})"

gcc $CFLAGS -c lutf8lib.c -o lutf8lib.o
gcc $CFLAGS -c lstrlib.c -o lstrlib.o
gcc $CFLAGS -c ltablib.c -o ltablib.o
gcc -shared $LDFLAGS -o utf8.so lutf8lib.o
gcc -shared $LDFLAGS -o string.so lstrlib.o
gcc -shared $LDFLAGS -o table.so ltablib.o

%install
%if 0%{?fedora} || 0%{?rhel} > 7
PKGDIR=%{buildroot}/%{luacompatpkgdir}
LIBDIR=%{buildroot}/%{luacompatlibdir}
%else
PKGDIR=%{buildroot}/%{luapkgdir}
LIBDIR=%{buildroot}/%{lualibdir}
# NOTE: epel7 install command doesn't propely create dir when combining -D -t
mkdir -p "$PKGDIR/%{luapkgname}"
mkdir -p "$LIBDIR/%{luapkgname}"
%endif

install -d -m 0755 "$PKGDIR/%{luapkgname}"
install -d -m 0755 "$LIBDIR/%{luapkgname}"
install -p -m 0644 %{luapkgname}/{init,module}.lua -t "$PKGDIR/%{luapkgname}/"
install -p -m 0755 {utf8,string,table}.so -t "$LIBDIR/%{luapkgname}/"

%if 0%{?rhel} == 7
install -d -m 0755 %{buildroot}%{luaincdir}/c-api
install -m 0644 -p -t %{buildroot}%{luaincdir}/c-api c-api/*
install -m 0644 lprefix.h %{buildroot}%{luaincdir}/lprefix.h
%endif

%if 0%{?fedora} || 0%{?rhel} > 7
install -d -m 0755 %{buildroot}%{luacompatincdir}/c-api
install -m 0644 -p -t %{buildroot}%{luacompatincdir}/c-api c-api/*
install -m 0644 lprefix.h %{buildroot}%{luacompatincdir}/lprefix.h
%endif

%if 0%{?rhel} == 7
%files
%license LICENSE
%doc README.md
%{luapkgdir}/%{luapkgname}
%{lualibdir}/%{luapkgname}
%{luaincdir}
%endif

%if 0%{?fedora} || 0%{?rhel} > 7
%files -n lua%{luacompatver}-%{luapkgname}
%license LICENSE
%doc README.md
%{luacompatpkgdir}/%{luapkgname}
%{luacompatlibdir}/%{luapkgname}
%{luacompatincdir}
%endif

%changelog
* Mon Sep 16 2019 Andreas Schneider <asn@redhat.com> - 0.7-3
- Also package the c-api

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Apr 03 2019 Tomas Krizek <tomas.krizek@nic.cz> - 0.7-1
- Initial package for Fedora 28+ and EPEL 7
