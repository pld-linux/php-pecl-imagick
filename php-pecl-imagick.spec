Summary:	PHP wrapper to the Image Magick Library
Summary(pl):	PHP-owy wrapper do biblioteki Image Magick
Name:		php-pecl-imagick
Version:	0.1.2
Release:	1
License:	PHP 2.02
Group:		Development/Languages/PHP
Source0:	http://pear.php.net/get/imagick-%{version}.tgz
URL:		http://pear.php.net/
BuildRequires:	ImageMagick-devel
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

%description -l pl
ImageMagick to du¿y zestaw narzêdzi i bibliotek do odczytu, zapisu i
modyfikowania obrazków w wielu formatach (ponad 68 g³ównych), w tym
popularnych, takich jak TIFF, JPEG, PNG, PDF, PhotoCD i GIF. Za pomoc±
ImageMagick mo¿na dynamicznie tworzyæ obrazki, co jest przydatne w
aplikacjach WWW. Mo¿na je tak¿e przeskalowywaæ, obracaæ, wyostrzaæ,
zmniejszaæ ilo¶æ kolorów - w tym samym lub innym formacie.

%prep
%setup -q -c

%build
cd imagick-%{version}
phpize
%configure \
	--with-imagick=/usr/X11R6/include/X11/

%{__make} CPPFLAGS="-DHAVE_CONFIG_H -I/usr/X11R6/include/X11/"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{extensionsdir}

install imagick-%{version}/modules/imagick.so $RPM_BUILD_ROOT%{extensionsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/php-module-install install imagick %{_sysconfdir}/php.ini

%preun
if [ "$1" = "0" ]; then
	%{_sbindir}/php-module-install remove imagick %{_sysconfdir}/php.ini
fi

%files
%defattr(644,root,root,755)
%doc imagick-%{version}/{CREDITS,EXPERIMENTAL,*.php}
%attr(755,root,root) %{extensionsdir}/imagick.so
