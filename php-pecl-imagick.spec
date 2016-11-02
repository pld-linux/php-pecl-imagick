#
# Conditional build:
%bcond_without	tests		# build without tests

%define		php_name	php%{?php_suffix}
%define		modname		imagick
%define		status		stable
Summary:	%{modname} - PHP wrapper to the Image Magick Library
Summary(pl.UTF-8):	%{modname} - PHP-owy wrapper do biblioteki Image Magick
Name:		%{php_name}-pecl-%{modname}
Version:	3.4.2
Release:	3
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	3f80e35c2434636cdb5df01b221b3ffa
Patch0:		skip_version_check.patch
URL:		http://pecl.php.net/package/imagick/
BuildRequires:	%{php_name}-devel >= 4:5.3
BuildRequires:	ImageMagick-devel >= 1:6.2.4.0
BuildRequires:	rpmbuild(macros) >= 1.650
%if %{with tests}
BuildRequires:	%{php_name}-cli
BuildRequires:	%{php_name}-spl
BuildRequires:	ImageMagick-coder-jpeg
BuildRequires:	ImageMagick-coder-png
BuildRequires:	ImageMagick-coder-tiff
%endif
%{?requires_php_extension}
Requires(triggerpostun):	sed >= 4.0
Requires:	%{php_name}-spl
Suggests:	ImageMagick-coder-jpeg
Suggests:	ImageMagick-coder-png
Suggests:	ImageMagick-coder-tiff
Provides:	php(imagick) = %{version}
Obsoletes:	php-pecl-imagick < 3.1.2-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ImageMagick is a robust collection of tools and libraries to read,
write, and manipulate an image in many image formats (over 68 major
formats) including popular formats like TIFF, JPEG, PNG, PDF, PhotoCD,
and GIF. With ImageMagick you can create images dynamically, making it
suitable for Web applications. You can also resize, rotate, sharpen,
color reduce, or add special effects to an image and save your
completed work in the same or differing image format.

In PECL status of this package is: %{status}.

%description -l pl.UTF-8
ImageMagick to duży zestaw narzędzi i bibliotek do odczytu, zapisu i
modyfikowania obrazków w wielu formatach (ponad 68 głównych), w tym
popularnych, takich jak TIFF, JPEG, PNG, PDF, PhotoCD i GIF. Za pomocą
ImageMagick można dynamicznie tworzyć obrazki, co jest przydatne w
aplikacjach WWW. Można je także przeskalowywać, obracać, wyostrzać,
zmniejszać ilość kolorów - w tym samym lub innym formacie.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-%{version}/* .
%patch0 -p1

%build
phpize
%configure \
	php_cv_cc_dashr=false

%{__make} \
	CFLAGS_CLEAN="%{rpmcflags}"

%if %{with tests}
%{__php} -n -q \
	-d extension_dir=modules \
	-d extension=%{php_extensiondir}/spl.so \
	-d extension=%{modname}.so \
	-m > modules.log
grep %{modname} modules.log

export NO_INTERACTION=1 REPORT_EXIT_STATUS=1 MALLOC_CHECK_=2
%{__make} test \
	PHP_EXECUTABLE=%{__php} \
	PHP_TEST_SHARED_SYSTEM_EXTENSIONS="spl" \
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir},%{_examplesdir}/%{name}-%{version}}
install -p modules/%{modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%triggerpostun -- %{name} < 0.9.11-2.1
%{__sed} -i -e '/^extension[[:space:]]*=[[:space:]]*%{modname}\.so/d' %{php_sysconfdir}/php.ini

%files
%defattr(644,root,root,755)
%doc CREDITS
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
%{_examplesdir}/%{name}-%{version}
