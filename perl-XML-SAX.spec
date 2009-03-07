%define module	XML-SAX
%define name	perl-%{module}
%define version 0.96
%define release %mkrel 2

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Simple API for XML
License:	GPL or Artistic
Group:		Development/Perl
Source:		ftp://ftp.perl.org/pub/CPAN/modules/by-module/XML/%{module}-%{version}.tar.bz2
Url:		http://search.cpan.org/dist/%{module}
%if %{mdkversion} < 1010
Buildrequires:	perl-devel
%endif
BuildRequires:	perl(XML::NamespaceSupport)
Provides:	perl(XML::SAX::PurePerl::DTDDecls)
Provides:	perl(XML::SAX::PurePerl::DocType)
Provides:	perl(XML::SAX::PurePerl::EncodingDetect)
Provides:	perl(XML::SAX::PurePerl::XMLDecl)
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}
# skipping requires on perl modules not in perl-base but in perl pkg
# those requires are only used by PurePerl module, whereas we often use perl-XML-LibXML
# this is useful to ensure urpmi only need perl-base, not perl
%define _requires_exceptions perl(File::Temp)\\|perl(Encode)

%description
XML::SAX consists of several framework classes for using and building
Perl SAX2 XML parsers, filters, and drivers. It is designed around the
need to be able to "plug in" different SAX parsers to an application
without requiring programmer intervention. Those of you familiar with
the DBI will be right at home. Some of the designs come from the Java
JAXP specification (SAX part), only without the javaness.

%prep
%setup -q -n %{module}-%{version}
chmod 644 Changes LICENSE README

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor <<EOF
N
EOF
%make

%check
%{__make} test

%install
rm -rf %{buildroot}
%makeinstall_std PERL="perl -I%{buildroot}%{perl_vendorlib}/"
touch %{buildroot}%{perl_vendorlib}/XML/SAX/ParserDetails.ini

%clean 
rm -rf %{buildroot}

%post
perl -MXML::SAX -e \
  'XML::SAX->add_parser(q(XML::SAX::PurePerl))->save_parsers()' 2>/dev/null

%preun
if [ $1 -eq 0 ]; then
  perl -MXML::SAX -e \
    'XML::SAX->remove_parser(q(XML::SAX::PurePerl))->save_parsers()'
fi

%files
%defattr(-,root,root,-)
%doc Changes LICENSE README
%{perl_vendorlib}/XML
%{_mandir}/man3/XML::*.3*
%ghost %{perl_vendorlib}/XML/SAX/ParserDetails.ini
%exclude %{perl_vendorlib}/XML/SAX/placeholder.pl


