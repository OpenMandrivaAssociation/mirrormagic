Name:		mirrormagic
Summary:	A puzzle game with mirrors and ray of lights
Version:	2.0.2
Release:	%{mkrel 5}
Source0:	http://www.artsoft.org/RELEASES/unix/mirrormagic/%{name}-%{version}.tar.bz2
Source1:	%{name}-16x16.png
Source2:	%{name}-32x32.png
Source3:	%{name}-48x48.png
Patch0:		mirrormagic-2.0.2-debian-gcc4.patch
Patch1:		mirrormagic-2.0.2-str-fmt.patch
URL:		https://www.artsoft.org/mirrormagic/
License:	GPL+
Group:		Games/Puzzles
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	SDL_image-devel
BuildRequires:	SDL_mixer-devel

%description
This game was first released as "Mindbender" in the year 1989 on the Amiga
(with ports on other computer systems) and is in fact a clone of the C64
game "Deflektor".

%prep
%setup -q
%patch0 -p1 -b .gcc4
%patch1 -p0 -b .str

%build
%{__make} OPTIONS="%{optflags}" sdl

%install
%{__rm} -rf %{buildroot}
%{__install} -m755 %{name} -D %{buildroot}%{_gamesbindir}/%{name}.wrapped
%{__install} -d %{buildroot}%{_gamesdatadir}/%{name}
%{__cp} -a graphics levels scores sounds music %{buildroot}%{_gamesdatadir}/%{name}
%{__chmod} 644 %{buildroot}%{_gamesdatadir}/%{name}/music/mod.enter_our_world

%{__cat} << EOF > %{buildroot}%{_gamesbindir}/%{name}
#!/bin/sh
pushd %{_gamesdatadir}/%{name}
%{_gamesbindir}/%{name}.wrapped
popd
EOF

mkdir -p %{buildroot}%{_datadir}/applications/
cat << EOF > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Exec=%{_gamesbindir}/%{name}
Icon=%{name}
Categories=Game;LogicGame;
Name=Mirror Magic
Comment=Puzzle game with mirrors and ray of lights
EOF

%{__install} %{SOURCE1} -D %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
%{__install} %{SOURCE2} -D %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%{__install} %{SOURCE3} -D %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(755,root,root,755)
%{_gamesbindir}/%{name}*
%defattr(644,root,root,755)
%doc README
%{_gamesdatadir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png

