%define		_modname	imagick
%define		_status		beta
Summary:	PHP wrapper to the Image Magick Library
Summary(pl):	PHP-owy wrapper do biblioteki Image Magick
Name:		php-pecl-%{_modname}
Version:	0.9.11
Release:	1
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	c8f78b063eb3fbdef1c8501190983c89
URL:		http://pecl.php.net/package/imagick/
BuildRequires:	ImageMagick-devel >= 1:6.0.0
BuildRequires:	php-devel
Requires:	php-common
Obsoletes:	php-imagick
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/php
%define		extensionsdir	%{_libdir}/php

%description
ImageMagick is a robust collection of tools and libraries to read,
write, and manipulate an image in many image formats (over 68 major
formats) including popular formats like TIFF, JPEG, PNG, PDF, PhotoCD,
and GIF. With ImageMagick you can create images dynamically, making it
suitable for Web applications. You can also resize, rotate, sharpen,
color reduce, or add special effects to an image and save your
completed work in the same or differing image format.

In PECL status of this package is: %{_status}.

%description -l pl
ImageMagick to du¿y zestaw narzêdzi i bibliotek do odczytu, zapisu i
modyfikowania obrazków w wielu formatach (ponad 68 g³ównych), w tym
popularnych, takich jak TIFF, JPEG, PNG, PDF, PhotoCD i GIF. Za pomoc±
ImageMagick mo¿na dynamicznie tworzyæ obrazki, co jest przydatne w
aplikacjach WWW. Mo¿na je tak¿e przeskalowywaæ, obracaæ, wyostrzaæ,
zmniejszaæ ilo¶æ kolorów - w tym samym lub innym formacie.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_modname}-%{version}
phpize
%configure

%{__make} \
	CFLAGS_CLEAN="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{extensionsdir}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/php-module-install install %{_modname} %{_sysconfdir}/php.ini

%preun
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove %{_modname} %{_sysconfdir}/php.ini
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/examples/{*.php,*.jpg,*.gif}
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
