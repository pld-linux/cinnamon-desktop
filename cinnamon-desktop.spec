%define gtk3_version 3.3.6
%define startup_notification_version 0.5
%define gtk_doc_version 1.9
%define glib2_version 1:2.32
Summary:	Shared code among cinnamon-session, nemo, etc
Name:		cinnamon-desktop
Version:	2.4.2
Release:	2
License:	GPL v2+ and LGPL v2+ add MIT
Group:		X11/Applications
Source0:	https://github.com/linuxmint/cinnamon-desktop/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	22d78e5c86135b65231b62b15ede27b7
Patch0:		set_font_defaults.patch
URL:		http://cinnamon.linuxmint.com/
BuildRequires:	gdk-pixbuf2-devel >= 2.21.3
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel >= %{glib2_version}
BuildRequires:	gnome-common
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk+3-devel >= %{gtk3_version}
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	pkg-config >= 0.14.0
BuildRequires:	rpm-pythonprov
BuildRequires:	xkeyboard-config
BuildRequires:	xorg-lib-libXext-devel >= 1.1
BuildRequires:	xorg-lib-libXrandr-devel >= 1.3
BuildRequires:	xorg-lib-libxkbfile-devel
Requires:	%{name}-libs = %{version}-%{release}
Requires:	applnk
Requires:	glib2 >= 1:2.26.0
Requires:	hwdata
# Make sure to update libgnome schema when changing this
#Requires:	system-backgrounds-gnome
# Make sure that gnome-themes-standard gets pulled in for upgrades
Requires:	gnome-themes-standard
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The cinnamon-desktop package contains an internal library
(libcinnamondesktop) used to implement some portions of the CINNAMON
desktop, and also some data files and other shared components of the
CINNAMON user environment.

%package libs
Summary:	Libraries for libcinnamon-desktop
License:	LGPL
Group:		Libraries
Conflicts:	%{name} < 2.4.2-2

%description libs
Libraries for libcinnamon-desktop.

%package devel
Summary:	Libraries and headers for libcinnamon-desktop
License:	LGPL v2+
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2-devel >= %{glib2_version}
Requires:	gtk+3-devel >= %{gtk3_version}
Requires:	startup-notification-devel >= %{startup_notification_version}

%description devel
Libraries and header files for the CINNAMON-internal private library
libcinnamondesktop.

%prep
%setup -q
%patch0 -p1

%build
NOCONFIGURE=1 ./autogen.sh
%configure \
	--disable-silent-rules \
	--disable-static \
	--with-pnp-ids-path="%{_datadir}/hwdata/pnp.ids"

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libcinnamon-desktop.la

%find_lang cinnamon-desktop-3.0 --all-name --with-gnome

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

%files -f cinnamon-desktop-3.0.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING COPYING.LIB README
%attr(755,root,root) %{_bindir}/cinnamon-desktop-migrate-mediakeys
%{_datadir}/glib-2.0/schemas/org.cinnamon.*.xml
%{_libexecdir}/cinnamon-rr-debug
%{_libdir}/girepository-1.0/CDesktopEnums-3.0.typelib
%{_libdir}/girepository-1.0/CinnamonDesktop-3.0.typelib

%files libs
%defattr(644,root,root,755)
%{_libdir}/libcinnamon-desktop.so.*.*.*
%ghost %{_libdir}/libcinnamon-desktop.so.4

%files devel
%defattr(644,root,root,755)
%{_libdir}/libcinnamon-desktop.so
%{_pkgconfigdir}/cinnamon-desktop.pc
%{_includedir}/cinnamon-desktop
%{_datadir}/gir-1.0/CDesktopEnums-3.0.gir
%{_datadir}/gir-1.0/CinnamonDesktop-3.0.gir
