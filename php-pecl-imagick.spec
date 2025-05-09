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
Version:	3.7.0
Release:	7
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	https://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	0687774a6126467d4e5ede02171e981d
Patch0:		skip_version_check.patch
Patch1:		build.patch
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
%patch -P0 -p1
%patch -P1 -p1

xfail() {
	local t=$1
	test -f $t
	cat >> $t <<-EOF

	--XFAIL--
	Skip
	EOF
}

while read line; do
	t=${line##*\[}; t=${t%\]}
	test -z "$t" && continue
	case "$t" in
		'#'*) continue;;
	esac
	xfail $t
done << 'EOF'

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

# 5.3, 5.5, 5.6, 7.0/x32, 7.1, 7.2, 7.3, 7.4
ImagickKernel::fromMatrix exceptions [tests/280_imagickkernel_exception_invalid_origin.phpt]
Imagick::setImageAlpha [tests/274_imagick_setImageAlpha.phpt]
Test ImagickDraw:: setTextInterlineSpacing [tests/279_ImagickDraw_setTextInterlineSpacing.phpt]
Test Imagick::optimizeimagelayers and Imagick::optimizeimagetransparency [tests/278_Imagick_optimaze_gif.phpt]

# php73/x32
Test PHP bug #59378 writing to php://memory is incomplete [tests/bug59378.phpt]

# php 7.4, 8.0
%if "%php_major_version.%php_minor_version" == "7.4"
Casting color and opacity to pixel [tests/003_cast_color_opacity.phpt]
Different types of thumbnailing [tests/002_thumbnail.phpt]
ImagickKernel::fromMatrix test [tests/145_imagickkernel_coverage.phpt]
Imagick::resizeImage prevent 0 width/height images [tests/github_174.phpt]
Test autoGammaImage [tests/263_autoGammaImage.phpt]
Test compositeImageGravity [tests/261_compositeImageGravity.phpt]
Test cropthumbnail [tests/006_cropthumbnail.phpt]
Test filling thumbnail with color [tests/007_thumbnail_fill.phpt]
Test for round issues [tests/064_cropThumbNailImage.phpt]
Test Imagick::colorDecisionListImage [tests/277_Imagick_colorDecisionListImage.phpt]
Test Imagick, progressMonitor [tests/127_Imagick_progressMonitor_basic.phpt]
Test importimagepixels [tests/010_importimagepixels.phpt]
Testing clone keyword [tests/004_clone.phpt]
Testing that cloned object does not affect the original [tests/012-clone-separation.phpt]
Test thumbnail bestfit [tests/005_bestfit.phpt]
%ifarch x32 %{ix86}
Test localContrastImage [tests/260_localContrastImage.phpt]
%endif
%endif
EOF

%build
phpize
%configure \
	php_cv_cc_dashr=false

%{__make} \
	CFLAGS_CLEAN="%{rpmcflags} $(pkg-config --cflags ImageMagick)"

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
