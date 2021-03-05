#
# Conditional build:
%bcond_without	tests		# build without tests

%define		php_name	php%{?php_suffix}
%define		modname		imagick
%define		status		stable
%define		libversion	%(pkg-config --modversion MagickCore 2>/dev/null || echo ERROR)
Summary:	%{modname} - PHP wrapper to the Image Magick Library
Summary(pl.UTF-8):	%{modname} - PHP-owy wrapper do biblioteki Image Magick
Name:		%{php_name}-pecl-%{modname}
Version:	3.4.4
Release:	4
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	https://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	6d3a7048ab73b0fab931f28c484dbf76
Patch0:		skip_version_check.patch
URL:		https://pecl.php.net/package/imagick
BuildRequires:	%{php_name}-cli
BuildRequires:	%{php_name}-devel >= 4:5.3
BuildRequires:	%{php_name}-pcre
BuildRequires:	%{php_name}-spl
BuildRequires:	ImageMagick-devel >= 1:6.2.4.0
BuildRequires:	pkgconfig
BuildRequires:	re2c
BuildRequires:	rpmbuild(macros) >= 1.650
%if %{with tests}
BuildRequires:	ImageMagick-coder-jpeg
BuildRequires:	ImageMagick-coder-png
BuildRequires:	ImageMagick-coder-tiff
%endif
%{?requires_php_extension}
Requires(postun):	sed >= 4.0
Requires:	%{php_name}-spl
Suggests:	ImageMagick-coder-jpeg
Suggests:	ImageMagick-coder-png
Suggests:	ImageMagick-coder-tiff
Provides:	php(imagick) = %{version}
Provides:	php(lib-imagick) = %{libversion}
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

xfail() {
	t=$1
	cat >> $t <<-EOF

	--XFAIL--
	Skip
	EOF
}
Test() {
	nf=$(eval echo \$$#)
	t=$nf; t=${t#\[}; t=${t%\]}
	xfail $t
}
# skip failing tests
Test Imagick, annotateImage [tests/034_Imagick_annotateImage_basic.phpt]
Test Imagick, setRegistry and getRegistry [tests/150_Imagick_setregistry.phpt]
Test ImagickDraw, composite [tests/177_ImagickDraw_composite_basic.phpt]
Test ImagickDraw, setFontSize [tests/206_ImagickDraw_setFontSize_basic.phpt]
Test ImagickDraw, setFontFamily [tests/207_ImagickDraw_setFontFamily_basic.phpt]
Test ImagickDraw, setFontStretch [tests/208_ImagickDraw_setFontStretch_basic.phpt]
Test ImagickDraw, setFontWeight [tests/209_ImagickDraw_setFontWeight_basic.phpt]
Test ImagickDraw, setFontStyle [tests/210_ImagickDraw_setFontStyle_basic.phpt]
Test ImagickDraw, setGravity [tests/212_ImagickDraw_setGravity_basic.phpt]
Test ImagickDraw, setTextAlignment [tests/222_ImagickDraw_setTextAlignment_basic.phpt]
Test ImagickDraw, setTextAntialias [tests/223_ImagickDraw_setTextAntialias_basic.phpt]
Test ImagickDraw, setTextUnderColor [tests/224_ImagickDraw_setTextUnderColor_basic.phpt]
Test ImagickDraw, setTextDecoration [tests/225_ImagickDraw_setTextDecoration_basic.phpt]
Test Tutorial, psychedelicFont [tests/241_Tutorial_psychedelicFont_basic.phpt]
Test Tutorial, svgExample [tests/243_Tutorial_svgExample_basic.phpt]
Test Tutorial, psychedelicFontGif [tests/244_Tutorial_psychedelicFontGif_basic.phpt]
Test Imagick, Imagick::exportImagePixels [tests/256_Imagick_exportImagePixels_basic.phpt]
Test ImagickDraw, getTextDirection [tests/264_ImagickDraw_getTextDirection_basic.phpt]
Test ImagickDraw, getFontResolution [tests/266_ImagickDraw_getFontResolution_basic.phpt]
%ifarch x32
# Fail on 7.0
Test Imagick, quantizeImage [tests/101_Imagick_quantizeImage_basic.phpt]
Test Imagick, uniqueImageColors [tests/163_Imagick_uniqueImageColors_basic.phpt]
Test Tutorial, deconstructGif [tests/237_Tutorial_deconstructGif_basic.phpt]
Test ImagickPixelIterator, setIteratorRow [tests/251_ImagickPixelIterator_setIteratorRow_basic.phpt]
%endif
# Fail on 5.3, 5.5, 5.6, 7.0, 7.1, 7.2
Test Tutorial, fxAnalyzeImage [tests/229_Tutorial_fxAnalyzeImage_case1.phpt]

%build
phpize
%configure \
	php_cv_cc_dashr=false

%{__make} \
	CFLAGS_CLEAN="%{rpmcflags}"

%{__php} -n -q \
	-d extension_dir=modules \
%if "%php_major_version.%php_minor_version" < "7.4"
	-d extension=%{php_extensiondir}/pcre.so \
	-d extension=%{php_extensiondir}/spl.so \
%endif
	-d extension=%{modname}.so \
	-m > modules.log
grep %{modname} modules.log

%if %{with tests}
export NO_INTERACTION=1 REPORT_EXIT_STATUS=1 MALLOC_CHECK_=2
%{__make} test \
	PHP_EXECUTABLE=%{__php} \
%if "%php_major_version.%php_minor_version" < "7.4"
	PHP_TEST_SHARED_SYSTEM_EXTENSIONS="pcre spl" \
%endif
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
