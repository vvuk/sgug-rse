Name:           perl-IO-Pager
Version:        0.42
Release:        1%{?dist}
Summary:        Select a pager and pipe text to it if destination is a TTY
# The license is something home-made or "the same terms as Perl itself".
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/IO-Pager
Source0:        https://cpan.metacpan.org/authors/id/J/JP/JPIERCE/IO-Pager-%{version}.tgz
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  sed
# Run-time:
BuildRequires:  perl(:VERSION) >= 5.8
BuildRequires:  perl(base)
BuildRequires:  perl(bytes)
# Data::Dumper not used
BuildRequires:  perl(Env)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Which)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(overload)
BuildRequires:  perl(PerlIO)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(SelectSaver)
BuildRequires:  perl(strict)
BuildRequires:  perl(Symbol)
# Term::Pager 1.5 not packaged becuase of a bad license, CPAN RT#130460
BuildRequires:  perl(Tie::Handle)
# Tests:
BuildRequires:  perl(bignum)
BuildRequires:  perl(blib)
BuildRequires:  perl(Config)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Test::More) >= 0.88
BuildRequires:  perl(utf8)
BuildRequires:  perl(warnings)
# Optional tests
# perl(PerlIO::Util) - not used
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(File::Which)
Requires:       perl(IO::Handle)
Requires:       perl(POSIX)

%description
IO::Pager is used to locate an available pager and programmatically decide
whether or not to pipe a file handle's output to the pager.

Please note that IO::Pager::Perl was removed due to a dependency on
Term::Pager that has a non-free license (CPAN RT#130460).

%prep
%setup -q -n IO-Pager-%{version}
# Remove dependeny on Term::Pager. Term::Pager cannot be packaged becuase of
# a bad license, CPAN RT#130460.
rm lib/IO/Pager/Perl.pm
perl -i -pe 'print $_ unless m{\Alib/IO/Pager/Perl.pm\b}' MANIFEST

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc CHANGES README TODO
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Fri Sep 06 2019 Petr Pisar <ppisar@redhat.com> - 0.42-1
- 0.42 bump
- IO::Pager::Perl was removed due to a dependency on Term::Pager that has
  a non-free license (CPAN RT#130460)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.40-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.40-3
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Oct 11 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.40-1
- 0.40 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.39-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.39-5
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.39-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.39-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.39-2
- Perl 5.26 rebuild

* Mon May 15 2017 Petr Pisar <ppisar@redhat.com> - 0.39-1
- 0.39 bump

* Fri May 12 2017 Petr Pisar <ppisar@redhat.com> - 0.38-1
- 0.38 bump

* Wed Apr 26 2017 Petr Pisar <ppisar@redhat.com> - 0.37-1
- 0.37 bump

* Tue Mar 14 2017 Petr Pisar <ppisar@redhat.com> 0.36-1
- Specfile autogenerated by cpanspec 1.78.