%define		glib_ver	1:2.37.3
%define		gtk_ver		3.3.16

Summary:	The cinnamon-desktop libraries (and common settings schemas for the cinnamon desktop)
Summary(pl.UTF-8):	Biblioteki cinnamon-desktop (i wspólne schematy ustawień dla środowiska cinnamon)
Name:		cinnamon-desktop
Version:	3.4.2
Release:	1
License:	GPL v2+ (libcvc), LGPL v2.1+ (libcinnamon-desktop)
Group:		X11/Applications
#Source0Download: https://github.com/linuxmint/cinnamon-desktop/releases
Source0:	https://github.com/linuxmint/cinnamon-desktop/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	db689f777868962c66a0a03a4a24c6a7
Patch0:		set_font_defaults.patch
URL:		http://cinnamon.linuxmint.com/
BuildRequires:	accountsservice-devel
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake >= 1:1.11
BuildRequires:	gdk-pixbuf2-devel >= 2.22.0
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= %{glib_ver}
BuildRequires:	gobject-introspection-devel >= 0.9.7
BuildRequires:	gtk+3-devel >= %{gtk_ver}
BuildRequires:	intltool >= 0.40.6
BuildRequires:	libtool >= 2:2.2.6
BuildRequires:	pkgconfig >= 1:0.14.0
BuildRequires:	pulseaudio-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	xkeyboard-config
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel >= 1.1
BuildRequires:	xorg-lib-libXrandr-devel >= 1.3
BuildRequires:	xorg-lib-libxkbfile-devel
Requires(post,postun):	glib2 >= %{glib_ver}
Requires:	%{name}-libs = %{version}-%{release}
Requires:	applnk
Requires:	hwdata
# Make sure to update libgnome schema when changing this
#Requires:	system-backgrounds-gnome
# Make sure that gnome-themes-standard gets pulled in for upgrades
Requires:	gnome-themes-standard
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The libcinnamon-desktop library provides API shared by several
applications on the desktop.

The libcvc library is a utility library for volume control.

%description -l pl.UTF-8
Biblioteka libcinnamon-desktop udostępnia API współdzielone przez
kilka aplikacji środowiska.

Biblioteka libcvc to biblioteka narzędziowa do sterowania głośnością.

%package libs
Summary:	Shared cinnamon-desktop libraries
Summary(pl.UTF-8):	Biblioteki współdzielone cinnamon-desktop
Group:		Libraries
Requires:	gdk-pixbuf2 >= 2.22.0
Requires:	glib2 >= %{glib_ver}
Requires:	gtk+3 >= %{gtk_ver}
Requires:	xorg-lib-libXext >= 1.1
Requires:	xorg-lib-libXrandr >= 1.3
Conflicts:	cinnamon-desktop < 2.4.2-2

%description libs
The libcinnamon-desktop library provides API shared by several
applications on the desktop.

The libcvc library is a utility library for volume control.

%description libs -l pl.UTF-8
Biblioteka libcinnamon-desktop udostępnia API współdzielone przez
kilka aplikacji środowiska.

Biblioteka libcvc to biblioteka narzędziowa do sterowania głośnością.

%package devel
Summary:	Header files for cinnamon-desktop libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek cinnamon-desktop
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= %{glib_ver}
Requires:	gtk+3-devel >= %{gtk_ver}
Requires:	pulseaudio-devel
Requires:	xorg-lib-libxkbfile-devel

%description devel
Header files for cinnamon-desktop libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek cinnamon-desktop.

%prep
%setup -q
%patch0 -p1

%build
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--disable-static \
	--with-pnp-ids-path="%{_datadir}/hwdata/pnp.ids"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libc*.la

%find_lang cinnamon-desktop

%clean
rm -rf $RPM_BUILD_ROOT

%postun
if [ $1 -eq 0 ]; then
	%glib_compile_schemas
fi

%posttrans
%glib_compile_schemas

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files -f cinnamon-desktop.lang
%defattr(644,root,root,755)
%doc AUTHORS README
%attr(755,root,root) %{_bindir}/cinnamon-desktop-migrate-mediakeys
%{_datadir}/glib-2.0/schemas/org.cinnamon.desktop.enums.xml
%{_datadir}/glib-2.0/schemas/org.cinnamon.desktop.*.gschema.xml

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcinnamon-desktop.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcinnamon-desktop.so.4
%attr(755,root,root) %{_libdir}/libcvc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcvc.so.0
%{_libdir}/girepository-1.0/CDesktopEnums-3.0.typelib
%{_libdir}/girepository-1.0/CinnamonDesktop-3.0.typelib
%{_libdir}/girepository-1.0/Cvc-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcinnamon-desktop.so
%attr(755,root,root) %{_libdir}/libcvc.so
%{_includedir}/cinnamon-desktop
%{_datadir}/gir-1.0/CDesktopEnums-3.0.gir
%{_datadir}/gir-1.0/CinnamonDesktop-3.0.gir
%{_datadir}/gir-1.0/Cvc-1.0.gir
%{_pkgconfigdir}/cinnamon-desktop.pc
%{_pkgconfigdir}/cvc.pc
