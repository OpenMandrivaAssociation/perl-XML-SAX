%define	modname	XML-SAX
%define	modver	0.99

# skipping requires on perl modules not in perl-base but in perl pkg
# those requires are only used by PurePerl module, whereas we often use perl-XML-LibXML
# this is useful to ensure urpmi only need perl-base, not perl
%if %{_use_internal_dependency_generator}
%define __noautoreq 'perl\\(File::Temp\\)|perl\\(Encode\\)'
%else
%define _requires_exceptions perl(File::Temp)\\|perl(Encode)
%endif

Summary:	Simple API for XML
Name:		perl-%{modname}
Version:	%{perl_convert_version %{modver}}
Release:	12
License:	GPLv2+ or Artistic
Group:		Development/Perl
Url:		http://search.cpan.org/dist/%{modname}
Source0:	ftp://ftp.perl.org/pub/CPAN/modules/by-module/XML/%{modname}-%{modver}.tar.bz2
Source1:	ParserDetails.ini
BuildArch:	noarch
BuildRequires:	perl-devel
BuildRequires:	perl(XML::NamespaceSupport)
BuildRequires:	perl(ExtUtils::MakeMaker)
BuildRequires:	perl(File::Temp)
BuildRequires:	perl(XML::SAX::Base) >= 1.50.0
BuildRequires:	perl(JSON::PP)
Provides:	perl(XML::SAX::PurePerl::DTDDecls)
Provides:	perl(XML::SAX::PurePerl::DocType)
Provides:	perl(XML::SAX::PurePerl::EncodingDetect)
Provides:	perl(XML::SAX::PurePerl::XMLDecl)

%description
XML::SAX consists of several framework classes for using and building
Perl SAX2 XML parsers, filters, and drivers. It is designed around the
need to be able to "plug in" different SAX parsers to an application
without requiring programmer intervention. Those of you familiar with
the DBI will be right at home. Some of the designs come from the Java
JAXP specification (SAX part), only without the javaness.

%prep
%setup -qn %{modname}-%{modver}

%build
perl Makefile.PL INSTALLDIRS=vendor <<EOF
N
EOF
%make

%check
make test

%install
# make install uses XML::SAX -- look in %{buildroot} before anything else
export PERL5LIB=%{buildroot}%{perl_vendorlib}:%{perl_vendorlib}
%makeinstall_std
install -m644 %{SOURCE1} -D %{buildroot}%{perl_vendorlib}/XML/SAX/ParserDetails.ini

%files
%doc Changes LICENSE README
%{perl_vendorlib}/XML
%{_mandir}/man3/XML::*.3*

