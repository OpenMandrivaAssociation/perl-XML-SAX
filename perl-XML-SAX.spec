%define upstream_name	 XML-SAX
%define upstream_version 0.99

# skipping requires on perl modules not in perl-base but in perl pkg
# those requires are only used by PurePerl module, whereas we often use perl-XML-LibXML
# this is useful to ensure urpmi only need perl-base, not perl
%if %{_use_internal_dependency_generator}
%define __noautoreq 'perl\\(File::Temp\\)|perl\\(Encode\\)'
%else
%define _requires_exceptions perl(File::Temp)\\|perl(Encode)
%endif

Name:		perl-%{upstream_name}
Version:	%perl_convert_version %{upstream_version}
Release:	2

Summary:	Simple API for XML
License:	GPL+ or Artistic
Group:		Development/Perl
Url:		http://search.cpan.org/dist/%{upstream_name}
Source0:	ftp://ftp.perl.org/pub/CPAN/modules/by-module/XML/%{upstream_name}-%{upstream_version}.tar.bz2

BuildRequires:	perl-devel
BuildRequires:	perl(XML::NamespaceSupport)
Provides:	perl(XML::SAX::PurePerl::DTDDecls)
Provides:	perl(XML::SAX::PurePerl::DocType)
Provides:	perl(XML::SAX::PurePerl::EncodingDetect)
Provides:	perl(XML::SAX::PurePerl::XMLDecl)
BuildArch:	noarch

%description
XML::SAX consists of several framework classes for using and building
Perl SAX2 XML parsers, filters, and drivers. It is designed around the
need to be able to "plug in" different SAX parsers to an application
without requiring programmer intervention. Those of you familiar with
the DBI will be right at home. Some of the designs come from the Java
JAXP specification (SAX part), only without the javaness.

%prep
%setup -q -n %{upstream_name}-%{upstream_version}
chmod 644 Changes LICENSE README

%build
%__perl Makefile.PL INSTALLDIRS=vendor <<EOF
N
EOF
%make

%check
make test

%install
%makeinstall_std PERL="perl -I%{buildroot}%{perl_vendorlib}/"
touch %{buildroot}%{perl_vendorlib}/XML/SAX/ParserDetails.ini

rm -f %{buildroot}%{perl_vendorlib}/XML/SAX/placeholder.pl

%post
perl -MXML::SAX -e \
  'XML::SAX->add_parser(q(XML::SAX::PurePerl))->save_parsers()' 2>/dev/null

%preun
if [ $1 -eq 0 ]; then
  perl -MXML::SAX -e \
    'XML::SAX->remove_parser(q(XML::SAX::PurePerl))->save_parsers()'
fi

%files
%doc Changes LICENSE README
%{perl_vendorlib}/XML
%{_mandir}/man3/XML::*.3*

%changelog
* Fri May 25 2012 Crispin Boylan <crisb@mandriva.org> 0.990.0-1
+ Revision: 800715
- New release

* Sun Jan 22 2012 Oden Eriksson <oeriksson@mandriva.com> 0.960.0-5
+ Revision: 765850
- rebuilt for perl-5.14.2

* Sat Jan 21 2012 Oden Eriksson <oeriksson@mandriva.com> 0.960.0-4
+ Revision: 764375
- rebuilt for perl-5.14.x

* Fri Jan 20 2012 Oden Eriksson <oeriksson@mandriva.com> 0.960.0-3
+ Revision: 763118
- rebuild

* Thu May 05 2011 Funda Wang <fwang@mandriva.org> 0.960.0-2
+ Revision: 669247
- cleanup spec file

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

* Mon Aug 03 2009 Jérôme Quelin <jquelin@mandriva.org> 0.960.0-1mdv2011.0
+ Revision: 408256
- rebuild using %%perl_convert_version

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0.96-2mdv2009.1
+ Revision: 351667
- rebuild

* Sun Aug 10 2008 Guillaume Rousse <guillomovitch@mandriva.org> 0.96-1mdv2009.0
+ Revision: 270402
- update to new version 0.96

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 0.16-3mdv2009.0
+ Revision: 224652
- rebuild

* Fri Jan 11 2008 Pixel <pixel@mandriva.com> 0.16-2mdv2008.1
+ Revision: 147995
- skipping requires on perl modules not in perl-base but in perl pkg,
  (those requires are only used by PurePerl module, whereas we often use
  perl-XML-LibXML). this is useful to ensure urpmi only need perl-base, not perl

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Jul 01 2007 Guillaume Rousse <guillomovitch@mandriva.org> 0.16-1mdv2008.0
+ Revision: 46717
- update to new version 0.16

* Wed May 02 2007 Olivier Thauvin <nanardon@mandriva.org> 0.15-1mdv2008.0
+ Revision: 20681
- 0.15

