%define	name	mirrormagic
%define	version	2.0.2
%define release	%mkrel 2
%define	Summary	A puzzle game with mirrors and ray of lights

Name:		%{name}
Summary:	%{Summary}
Version:	%{version}
Release:	%{release}
Source0:	http://www.artsoft.org/RELEASES/unix/mirrormagic/%{name}-%{version}.tar.bz2
Source1:	%{name}-16x16.png
Source2:	%{name}-32x32.png
Source3:	%{name}-48x48.png
#Patch0:	mirrormagic-fix-va_arg.patch.bz2
URL:		http://www.artsoft.org/mirrormagic/
License:	GPL
Group:		Games/Puzzles
BuildRequires:	SDL_image-devel SDL_mixer-devel X11-devel alsa-lib-devel esound-devel
Packager:	Guillaume Cottenceau <gc@mandrakesoft.com>
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This game was first released as "Mindbender" in the year 1989 on the Amiga
(with ports on other computer systems) and is in fact a clone of the C64
game "Deflektor".

%prep
%setup -q
#%patch0 -p0
#perl -pi -e "s/^OPTIONS.*/OPTIONS = $RPM_OPT_FLAGS/" src/Makefile

%build
%{__make} OPTIONS="$RPM_OPT_FLAGS -O3" sdl

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__install} -m755 %{name} -D $RPM_BUILD_ROOT%{_gamesbindir}/%{name}.wrapped
%{__install} -d $RPM_BUILD_ROOT%{_gamesdatadir}/%{name}
%{__cp} -a graphics levels scores sounds music $RPM_BUILD_ROOT%{_gamesdatadir}/%{name}
%{__chmod} 644 $RPM_BUILD_ROOT%{_gamesdatadir}/%{name}/music/mod.enter_our_world

%{__cat} << EOF > $RPM_BUILD_ROOT%{_gamesbindir}/%{name}
#!/bin/sh
pushd %{_gamesdatadir}/%{name}
%{_gamesbindir}/%{name}.wrapped
popd
EOF

%{__install} -d $RPM_BUILD_ROOT%{_menudir}
%{__cat} <<EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}):command="%{_gamesbindir}/%{name}" \
		icon=%{name}.png \
		needs="x11" \
		section="Amusement/Puzzles" \
		title="Mirror Magic"\
		longtitle="%{Summary}"
EOF

%{__install} %{SOURCE1} -D $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
%{__install} %{SOURCE2} -D $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
%{__install} %{SOURCE3} -D $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png

%post
%update_menus

%postun
%clean_menus

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(755,root,root,755)
%{_gamesbindir}/%{name}*
%defattr(644,root,root,755)
%doc README
%{_gamesdatadir}/%{name}
%{_menudir}/%{name}
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png

