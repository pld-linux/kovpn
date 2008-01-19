%define		_rc _pre6
Summary:	Simple OpenVPN GUI for KDE
Summary(pl.UTF-8):	Prosty interfejs graficzny do OpenVPN-a dla KDE
Name:		kovpn
Version:	0.3
Release:	0.1
License:	GPL v2
Group:		X11/Applications
Source0:	http://home.bawue.de/~lighter/www.enlighter.de/files/%{name}-%{version}%{_rc}.tar.bz2
# Source0-md5:	5cb3ddf5248d3d83b96d831555ef1cf7
Patch0:		kde-ac260.patch
Patch1:		kde-am.patch
URL:		http://www.kde-apps.org/content/show.php?content=37043
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	kdelibs-devel >= 9:3.2.0
BuildRequires:	rpmbuild(macros) >= 1.129
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Kovpn is a simple OpenVPN GUI which is intended to fit end-user's
needs.

It runs without root privileges and can control the most important
functions of OpenVPN:
 - connect and disconnect
 - username and password input
 - private key passphrase input
 - show status
 - supports multiple OpenVPN connections
 - Store username and/or passwords in kwallet
 - Supports OpenVPN's management interface access control
 - Simple DCOP interface (status report, connect, disconnect)

It requires some changes to your OpenVPN configuration file: you have
to activate the management interface.

%description -l pl.UTF-8
Kovpn to prosty interfejs graficzny do OpenVPN-a, napisany z myślą o
użytkownikach końcowych.

Działa bez uprawnień roota, steruje najważniejszymi funkcjami
OpenVPN-a:
 - łączy się i rozłącza
 - pozwala podać nazwę użytkownika i hasło
 - pozwala podać hasło do klucza prywatnego
 - pokazuje stan połączenia
 - obsługuje wiele połączeń OpenVPN
 - przechowuje nazwy użytkowników i/lub hasła w kwallecie
 - obsługuje kontrolę dostępu do interfejsu zarządzajągo OpenVPN-a
 - ma prosty interfejs DCOP (informację o stanie, łączenie,
   rozłączanie).

Wymaga pewnych zmian w pliku konfiguracyjnym OpenVPN-a - trzeba
włączyć interfejs zarządzający.

%prep
%setup -q -n %{name}-%{version}%{_rc}
%patch0 -p1
%patch1 -p1

%build
cp -f /usr/share/automake/config.sub admin
%configure \
%if "%{_lib}" == "lib64"
	--enable-libsuffix=64 \
%endif
	--%{?debug:en}%{!?debug:dis}able-debug%{?debug:=full} \
	--with-qt-libraries=%{_libdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pixmapsdir},%{_desktopdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	kde_htmldir=%{_kdedocdir} \
	kde_libs_htmldir=%{_kdedocdir} \
	kdelnkdir=%{_desktopdir} \

%find_lang %{name} --with-kde
mv $RPM_BUILD_ROOT{%{_datadir}/applnk/Utilities,%{_desktopdir}}/kovpn.desktop

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_datadir}/apps/%{name}
%{_desktopdir}/*.desktop
%{_iconsdir}/*/*/apps/%{name}.png
