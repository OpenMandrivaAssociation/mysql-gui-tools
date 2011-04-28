%define build_java 0
%define build_autotools 1
%define build_administrator 1
%define build_query_browser 1

# commandline overrides:
# rpm -ba|--rebuild --with 'xxx'
%{?_with_java: %{expand: %%global build_java 1}}
%{?_without_java: %{expand: %%global build_java 0}}
%{?_with_autotools: %{expand: %%global build_autotools 1}}
%{?_without_autotools: %{expand: %%global build_autotools 0}}
%{?_with_administrator: %{expand: %%global build_administrator 1}}
%{?_without_administrator: %{expand: %%global build_administrator 0}}
%{?_with_query_browser: %{expand: %%global build_query_browser 1}}
%{?_without_query_browser: %{expand: %%global build_query_browser 0}}

%define r_ver r14

%define ma_realversion 1.2.12
%define qb_realversion 1.2.12

%define libname %mklibname 0

Summary:	GUI Tools for MySQL 5.0 - common files
Name:		mysql-gui-tools
Group:		Databases
Version:	5.0
Release:	1.%{r_ver}.9
License:	GPL
URL:		http://www.mysql.com/products/tools/
Source:		ftp://ftp.sunet.se/pub/databases/relational/mysql/Downloads/MySQLGUITools/%{name}-%{version}%{r_ver}.tar.gz
Source1:	mysql-administrator-doc.tar.bz2
Source2:	mysql-query-browser-doc.tar.bz2
Patch0:		mysql-gui-tools-mdv_conf.diff
Patch2:         mysql-administrator-1.1.5-shellbang.patch
Patch3:		mysql-administrator-help.patch
Patch4:		mysql-query-browser.patch
Patch5:		mysql-query-browser-gcc4.patch
Patch6:		mysql-gui-common-pkg-config.patch
Patch7:		mysql-gui-common-unused-func.patch
Patch8:		mysql-gui-common-warnings.patch
Patch10:	mysql-gui-tools-gcc42.patch
Patch11:	mysql-gui-tools-bash.patch
Patch12:	mysql-gui-tools-global.patch
Patch14:	mysql-gui-tools-sigc_2.1.1_api_fixes.diff
Patch15:	mysql-gui-tools.chema_change_freeze_bug.patch
Patch17:	mysql-gui-tools-gcc43.diff
Patch18:	mysql-gui-tools-no-DISABLE_DEPRECATED.diff
Patch19:	mysql-gui-tools-5.0r14-garbage_fix.diff
Patch20:	mysql-gui-tools-5.0r14-invalid_const_char_conversion.diff
Patch21:	mysql-gui-tools-5.0r14-format_not_a_string_literal_and_no_format_arguments.diff
Patch22:	mysql-gui-tools-gtksourceview-cflags.patch
Patch23:	mysql-gui-tools-5.0r14-gnome_cflags.diff
BuildRequires:	autoconf2.5
BuildRequires:	expat-devel
BuildRequires:	file
BuildRequires:	gettext-devel
BuildRequires:	glib2-devel
BuildRequires:	glibmm2.4-devel
BuildRequires:	gtk2-devel
BuildRequires:	gtkmm2.4-devel >= 2.6
BuildRequires:	imagemagick
BuildRequires:	libext2fs-devel
BuildRequires:	libglade2.0-devel >= 2.5
BuildRequires:	libsigc++2.0-devel
BuildRequires:	libslang-devel
BuildRequires:	libtool
BuildRequires:	libuuid-devel
BuildRequires:	libxml2-devel
%if %mdkversion < 200700
BuildRequires:	libgtkhtml-3.6-devel
BuildRequires:	liblua-devel >= 5.0.2
BuildRequires:	Mesa-devel
BuildRequires:	MesaGLU-devel
%else
BuildRequires:	libfcgi-devel
BuildRequires:	gtkhtml-3.14-devel
BuildRequires:	lua5.0-devel
BuildRequires:	mesagl-devel
BuildRequires:	mesaglu-devel
%endif
%if %{build_java}
BuildRequires:  junit
BuildRequires:  java-gcj-compat-devel
BuildRequires:  jpackage-utils
%endif
BuildRequires:	gettext
BuildRequires:	libgnome2-devel
BuildRequires:	libgnomeprint-devel >= 2.2.0
BuildRequires:	mysql-devel >= 5.0
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	pcre-devel >= 5.0
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	readline-devel
BuildRequires:	termcap-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root

%description 
GUI Tools for MySQL 5.0 is a suite of applications written for developing and
managing MySQL servers.

This package contains data files and libraries for MySQL GUI Tools. Actual
applications are in packages mysql-administrator, mysql-query-browser and
mysql-workbench

%if %{build_administrator}
%package -n	mysql-administrator
Summary:	Administration tool for MySQL 5.0
Group:		Databases
Requires:	mysql-gui-tools = %{version}

%description -n	mysql-administrator
MySQL Administrator is a powerful graphical administration console that enables
you to easily administer your MySQL environment and gain significantly better
visibility into how your databases are operating. MySQL Administrator now
integrates database management and maintenance into a single, seamless
environment, with a clear and intuitive graphical user interface.

This is MySQL Administrator %{ma_realversion}.
%endif

%if %{build_query_browser}
%package -n	mysql-query-browser
Summary:	Query shell for MySQL 5.0
Group:		Databases
Requires:	mysql-gui-tools = %{version}

%description -n	mysql-query-browser
MySQL Query Browser is a GUI tool for executing SQL queries. It will display
the result in a list where you can edit its contents and save. It has several
auxiliar features to facilitate work, such as query "bookmarking", query
history, syntax highlighting and online help.

This is MySQL QueryBrowser %{qb_realversion}.
%endif

%prep

%setup -q -n %{name}-%{version}%{r_ver} -a1 -a2

# fixups
mv common mysql-gui-common

mv administrator/* mysql-administrator/
rm -rf administrator

mv query-browser/* mysql-query-browser/
rm -rf query-browser

# will probably never work on linux
rm -rf migration-tool

%patch0 -p1
%patch2 -p0

pushd mysql-administrator
%patch3
popd

pushd mysql-query-browser
%patch4
%patch5
popd

pushd mysql-gui-common
%patch6
%patch7
%patch8
popd

%patch10 -p1
%patch11 -p1
%patch12 -p0
%patch14 -p1
%patch15 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p0
%patch20 -p0
%patch21 -p0
%patch22 -p0
%patch23 -p0

%if %{build_java}
# remove binary-only jars from filesystem
%{__rm} mysql-gui-common/res/java/jtds-1.2.jar
%{__rm} mysql-gui-common/res/java/junit.jar
%{__ln_s} %{_javadir}/junit.jar mysql-gui-common/res/java/junit.jar
%{__rm} mysql-gui-common/res/java/mysql-connector-java-5.0.4-bin.jar
%{__rm} mysql-gui-common/res/java/sapdbc-7_6_00_12_4339.jar

# remove references to binary jars from java Makefile
%{__perl} -pi -e 's/^javalib_DATA=.*/javalib_DATA=/' mysql-gui-common/source/java/Makefile.{am,in}
%endif

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

%build
export CPPFLAGS="-D_GNU_SOURCE=1"

pushd  mysql-gui-common
%if %{build_autotools}
sh ./autogen.sh \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --sysconfdir=%{_sysconfdir} \
    --datadir=%{_datadir} \
    --includedir=%{_includedir} \
    --libdir=%{_libdir} \
    --libexecdir=%{_libexecdir} \
    --localstatedir=%{_localstatedir}/lib \
    --mandir=%{_mandir} \
    --enable-grt \
    --enable-python-modules \
%if %mdkversion >= 200700
    --enable-fastcgi \
%if %{build_java}
    --enable-java-modules \
    --with-java-includes=%{java_home}/include \
%else
    --disable-java-modules \
%endif
%endif
    --enable-readline \
    --enable-canvas \
    --with-bonobo
%endif

%configure2_5x \
    --enable-grt \
    --enable-python-modules \
%if %mdkversion >= 200700
    --enable-fastcgi \
%if %{build_java}
    --enable-java-modules \
    --with-java-includes=%{java_home}/include \
%else
    --disable-java-modules \
%endif
%endif
    --enable-readline \
    --enable-canvas \
    --with-bonobo

%make
popd

%if %{build_administrator}
# administrator
pushd mysql-administrator
%if %{build_autotools}
sh ./autogen.sh \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --sysconfdir=%{_sysconfdir} \
    --datadir=%{_datadir} \
    --includedir=%{_includedir} \
    --libdir=%{_libdir} \
    --libexecdir=%{_libexecdir} \
    --localstatedir=%{_localstatedir}/lib \
    --mandir=%{_mandir} \
    --with-bonobo

%endif

%configure2_5x \
    --with-bonobo

%make
popd
%endif

%if %{build_query_browser}
# query-browser
pushd mysql-query-browser
%if %{build_autotools}
sh ./autogen.sh \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --sbindir=%{_sbindir} \
    --sysconfdir=%{_sysconfdir} \
    --datadir=%{_datadir} \
    --includedir=%{_includedir} \
    --libdir=%{_libdir} \
    --libexecdir=%{_libexecdir} \
    --localstatedir=%{_localstatedir}/lib \
    --mandir=%{_mandir} \
%if %mdkversion < 200700
    --with-gtkhtml=libgtkhtml-3.6 \
%else
    --with-gtkhtml=libgtkhtml-3.14 \
%endif
%endif
    --with-bonobo \
    --disable-maintainer-mode

%configure2_5x \
%if %mdkversion < 200700
    --with-gtkhtml=libgtkhtml-3.6 \
%else
    --with-gtkhtml=libgtkhtml-3.14 \
%endif
    --with-bonobo \
    --disable-maintainer-mode

%make
popd
%endif

%install
rm -rf %{buildroot}

%makeinstall_std -C mysql-gui-common

# fix some menu entries and stuff...
install -d %{buildroot}%{_miconsdir}
install -d %{buildroot}%{_iconsdir}
install -d %{buildroot}%{_liconsdir}

%if %{build_administrator}
################################################################################
# mysql-administrator
%makeinstall_std -C mysql-administrator

rm -f %{buildroot}%{_datadir}/applications/MySQLAdministrator.desktop 
cat > %{buildroot}%{_datadir}/applications/mysql-administrator.desktop << EOF
[Desktop Entry]
Name=MySQL Administrator
Comment=MySQL Administration Tool
Exec=%{_bindir}/mysql-administrator
Terminal=false
Type=Application
Icon=mysql-administrator
Categories=X-MandrivaLinux-MoreApplications-Databases;GTK;Database;Development;Application;
EOF

# make some icons
convert %{buildroot}%{_datadir}/mysql-gui/MySQLIcon_Admin_48x48.png -resize 16x16  %{buildroot}%{_miconsdir}/mysql-administrator.png
convert %{buildroot}%{_datadir}/mysql-gui/MySQLIcon_Admin_48x48.png -resize 32x32  %{buildroot}%{_iconsdir}/mysql-administrator.png
convert %{buildroot}%{_datadir}/mysql-gui/MySQLIcon_Admin_48x48.png -resize 48x48  %{buildroot}%{_liconsdir}/mysql-administrator.png

%find_lang mysql-administrator --all-name
%endif

%if %{build_query_browser}
################################################################################
# mysql-query-browser
%makeinstall_std -C mysql-query-browser

rm -f %{buildroot}%{_datadir}/applications/MySQLQueryBrowser.desktop
cat > %{buildroot}%{_datadir}/applications/mysql-query-browser.desktop << EOF
[Desktop Entry]
Name=MySQL Query Browser
Comment=MySQL Query Tool
Exec=%{_bindir}/mysql-query-browser
Terminal=false
Type=Application
Icon=mysql-query-browser
Categories=X-MandrivaLinux-MoreApplications-Databases;GTK;Database;Development;Application;
EOF

# make some icons
convert %{buildroot}%{_datadir}/mysql-gui/MySQLIcon_QueryBrowser_48x48.png -resize 16x16  %{buildroot}%{_miconsdir}/mysql-query-browser.png
convert %{buildroot}%{_datadir}/mysql-gui/MySQLIcon_QueryBrowser_48x48.png -resize 32x32  %{buildroot}%{_iconsdir}/mysql-query-browser.png
convert %{buildroot}%{_datadir}/mysql-gui/MySQLIcon_QueryBrowser_48x48.png -resize 48x48  %{buildroot}%{_liconsdir}/mysql-query-browser.png

%find_lang mysql-query-browser --all-name
%endif

%if %{build_administrator}
%if %mdkversion < 200900
%post -n mysql-administrator
%update_menus
%endif

%if %mdkversion < 200900
%postun -n mysql-administrator
%clean_menus
%endif
%endif

%if %{build_query_browser}
%if %mdkversion < 200900
%post -n mysql-query-browser
%update_menus
%endif

%if %mdkversion < 200900
%postun -n mysql-query-browser
%clean_menus
%endif
%endif

%clean
rm -rf %{buildroot}

%files 
%defattr(-, root, root)
%doc mysql-gui-common/COPYING
%doc mysql-gui-common/README
%doc mysql-gui-common/README.translating
%dir %{_datadir}/mysql-gui
%{_datadir}/mysql-gui/common/*
%if %mdkversion >= 200700
%if %{build_java}
%{_libdir}/mysql-gui/libmyx_grt_java*
%endif
%endif

%if %{build_administrator}
%files -n mysql-administrator -f mysql-administrator.lang
%defattr(-, root, root)
%doc mysql-administrator/ChangeLog
%doc mysql-administrator/COPYING 
%doc mysql-administrator/res/FAQ
%doc mysql-administrator/doc/*
%attr(0755,root,root) %{_bindir}/mabackup
%attr(0755,root,root) %{_bindir}/mysql-administrator
%attr(0755,root,root) %{_bindir}/mysql-administrator-bin
%dir %{_datadir}/mysql-gui/administrator
%{_datadir}/mysql-gui/MySQLIcon_Admin*
%{_datadir}/mysql-gui/administrator/*
%{_datadir}/applications/mysql-administrator.desktop
%{_iconsdir}/mysql-administrator.png
%{_liconsdir}/mysql-administrator.png
%{_miconsdir}/mysql-administrator.png
%endif

%if %{build_query_browser}
%files -n mysql-query-browser -f mysql-query-browser.lang
%defattr(-, root, root)
%doc mysql-query-browser/COPYING 
%doc mysql-query-browser/res/ChangeLog
%doc mysql-query-browser/doc/*
%dir %{_datadir}/mysql-gui/query-browser
%{_datadir}/mysql-gui/query-browser/*
%attr(0755,root,root) %{_bindir}/mysql-query-browser
%attr(0755,root,root) %{_bindir}/mysql-query-browser-bin
%{_datadir}/mysql-gui/MySQLIcon_Query*
%{_datadir}/applications/mysql-query-browser.desktop
%{_iconsdir}/mysql-query-browser.png
%{_liconsdir}/mysql-query-browser.png
%{_miconsdir}/mysql-query-browser.png
%endif

