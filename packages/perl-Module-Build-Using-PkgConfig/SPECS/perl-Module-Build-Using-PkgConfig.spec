Name:           perl-Module-Build-Using-PkgConfig
Version:        0.03
Release:        1%{?dist}
Summary:        Extend Module::Build to easily use platform libraries provided by pkg-config
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/Module-Build-Using-PkgConfig/
Source0:        https://cpan.metacpan.org/authors/id/P/PE/PEVANS/Module-Build-Using-PkgConfig-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(:VERSION) >= 5.10
BuildRequires:  perl(Module::Build) >= 0.4004
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time
BuildRequires:  perl(base)
BuildRequires:  perl(ExtUtils::PkgConfig)
# Tests
BuildRequires:  perl(Test::More) >= 0.88
# Optional tests
BuildRequires:  perl(Test::Pod) >= 1.00
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This subclass of Module::Build provides some handy methods to assist the
Build.PL script of XS-based module distributions that make use of platform
libraries managed by pkg-config.

%prep
%setup -q -n Module-Build-Using-PkgConfig-%{version}

%build
perl Build.PL --installdirs=vendor
./Build

%install
./Build install --destdir=$RPM_BUILD_ROOT --create_packlist=0
%{_fixperms} $RPM_BUILD_ROOT/*

%check
./Build test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Wed Jul 24 2019 Jitka Plesnikova <jplesnik@redhat.com> 0.03-1
- Specfile autogenerated by cpanspec 1.78.
