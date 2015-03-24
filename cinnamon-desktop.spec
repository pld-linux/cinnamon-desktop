%define gtk3_version                      3.10.0
%define startup_notification_version      0.5
%define gtk_doc_version                   1.9
%define po_package                        cinnamon-desktop-3.0
Summary:	Shared code among cinnamon-session, nemo, etc
Name:		cinnamon-desktop
Version:	2.4.2
Release:	1
License:	GPL v2+ and LGPL v2+ add MIT
Group:		X11/Applications
Source0:	https://github.com/linuxmint/cinnamon-desktop/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	22d78e5c86135b65231b62b15ede27b7
Patch0:		set_font_defaults.patch
URL:		http://cinnamon.linuxmint.com/
BuildRequires:	gnome-common
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk+3-devel >= %{gtk3_version}
BuildRequires:	gtk-doc >= %{gtk_doc_version}
BuildRequires:	intltool
BuildRequires:	itstool
BuildRequires:	startup-notification-devel >= %{startup_notification_version}
BuildRequires:	xkeyboard-config
BuildRequires:	xorg-lib-libxkbfile-devel
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

%package devel
Summary:	Libraries and headers for libcinnamon-desktop
License:	LGPL v2+
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
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

%find_lang %{po_package} --all-name --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
	%glib_compile_schemas
fi

%posttrans
%glib_compile_schemas

%files -f %{po_package}.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING COPYING.LIB README
%attr(755,root,root) %{_bindir}/cinnamon-desktop-migrate-mediakeys
%{_datadir}/glib-2.0/schemas/org.cinnamon.*.xml
%{_libexecdir}/cinnamon-rr-debug
# LGPL
%{_libdir}/libcinnamon-desktop.so.*.*.*
%ghost %{_libdir}/libcinnamon-desktop.so.4
%{_libdir}/girepository-1.0/CDesktopEnums-3.0.typelib
%{_libdir}/girepository-1.0/CinnamonDesktop-3.0.typelib

%files devel
%defattr(644,root,root,755)
%{_libdir}/libcinnamon-desktop.so
%{_pkgconfigdir}/cinnamon-desktop.pc
%{_includedir}/cinnamon-desktop
%{_datadir}/gir-1.0/CDesktopEnums-3.0.gir
%{_datadir}/gir-1.0/CinnamonDesktop-3.0.gir
