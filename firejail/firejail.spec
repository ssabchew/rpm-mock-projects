%global     commit     89f2705ae1e91b5b145cbe6c956977290f7980f4
%global     githash    %(c=%{commit}; echo ${c:0:7})
%global     gitdate    20161224
%global     gittime    1329

Name:       firejail
Version:    0.9.45
Release:    1.%{gitdate}%{gittime}git%{githash}%{?dist}
Summary:    Linux namespaces sandbox program

License:    GPL+
Group:      Development/Tools
Source0:    https://github.com/netblue30/firejail/archive/%{commit}/%{name}-v%{version}-%{githash}.tar.gz
URL:        https://github.com/netblue30/firejail

%description
Firejail is a SUID sandbox program that reduces the risk of security
breaches by restricting the running environment of untrusted applications
using Linux namespaces. It includes a sandbox profile for Mozilla Firefox.

%prep
echo ===
echo /usr/lib64/firejail/fcopy
echo ===

%setup -q -n %{name}-%{commit}

%build
%configure --prefix=%{_prefix} --disable-apparmor
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%files
%doc
%attr(4755, -, -) %{_bindir}/firejail
%{_bindir}/firemon
%{_bindir}/firecfg

%{_libdir}/%{name}/*

%{_datarootdir}/bash-completion/completions/firecfg
%{_datarootdir}/bash-completion/completions/firejail
%{_datarootdir}/bash-completion/completions/firemon
%{_docdir}/firejail
%{_mandir}/man1/firecfg.1.gz
%{_mandir}/man1/firejail.1.gz
%{_mandir}/man1/firemon.1.gz
%{_mandir}/man5/firejail-login.5.gz
%{_mandir}/man5/firejail-profile.5.gz
%config %{_sysconfdir}/firejail

%changelog
* Mon Oct 24 2016 ssabchew <ssabchew at yahoo.com> 0.9.44-1
- updated to latest version in master.

* Tue Jul 12 2016 ssabchew <ssabchew at yahoo.com> 0.9.40-2
- updated to latest master

* Sat May 14 2016 ssabchew <ssabchew at yahoo.com> 0.9.40-1
- Update to dev version 0.9.40

* Mon Sep 14 2015 netblue30 <netblue30@yahoo.com> 0.9.30-1
 - added a disable-history.inc profile as a result of Firefox PDF.js exploit;
   disable-history.inc included in all default profiles
 - Firefox PDF.js exploit (CVE-2015-4495) fixes
 - added --private-etc option
 - added --env option
 - added --whitelist option
 - support ${HOME} token in include directive in profile files
 - --private.keep is transitioned to --private-home
 - support ~ and blanks in blacklist option
 - support "net none" command in profile files
 - using /etc/firejail/generic.profile by default for user sessions
 - using /etc/firejail/server.profile by default for root sessions
 - added build --enable-fatal-warnings configure option
 - added persistence to --overlay option
 - added --overlay-tmpfs option
 - make install-strip implemented, make install renamed
 - bugfixes

* Sat Aug 1 2015 netblue30 <netblue30@yahoo.com> 0.9.28-1
 - network scanning, --scan option
 - interface MAC address support, --mac option
 - IP address range, --iprange option
 - traffic shaping, --bandwidth option
 - reworked printing of network status at startup
 - man pages rework
 - added firejail-login man page
 - added GNU Icecat, FileZilla, Pidgin, XChat, Empathy, DeaDBeeF default
   profiles
 - added an /etc/firejail/disable-common.inc file to hold common directory
   blacklists
 - blacklist Opera and Chrome/Chromium config directories in profile files
 - support noroot option for profile files
 - enabled noroot in default profile files
 - bugfixes

* Thu Apr 30 2015 netblue30 <netblue30@yahoo.com> 0.9.26-1
 - private dev directory
 - private.keep option for whitelisting home files in a new private directory
 - user namespaces support, noroot option
 - added Deluge and qBittorent profiles
 - bugfixes

* Sun Apr 5 2015  netblue30 <netblue30@yahoo.com> 0.9.24-1
 - whitelist and blacklist seccomp filters
 - doubledash option
 - --shell=none support
 - netfilter file support in profile files
 - dns server support in profile files
 - added --dns.print option
 - added default profiles for Audoacious, Clementine, Rhythmbox and Totem.
 - added --caps.drop=all in default profiles
 - new syscalls in default seccomp filter: sysfs, sysctl, adjtimex, kcmp
 -        clock_adjtime, lookup_dcookie, perf_event_open, fanotify_init
 - Bugfix: using /proc/sys/kernel/pid_max for the max number of pids
 - two build patches from Reiner Herman (tickets 11, 12)
 - man page patch from Reiner Herman (ticket 13)
 - output patch (ticket 15) from sshirokov

* Mon Mar 9 2015  netblue30 <netblue30@yahoo.com> 0.9.22-1
 - Replaced --noip option with --ip=none
 - Container stdout logging and log rotation
 - Added process_vm_readv, process_vm_writev and mknod to
     default seccomp blacklist
 - Added CAP_MKNOD to default caps blacklist
 - Blacklist and whitelist custom Linux capabilities filters
 - macvlan device driver support for --net option
 - DNS server support, --dns option
 - Netfilter support
 - Monitor network statistics, --netstats option
 - Added profile for Mozilla Thunderbird/Icedove
 - --overlay support for Linux kernels 3.18+
 - Bugfix: preserve .Xauthority file in private mode (test with ssh -X)
 - Bugfix: check uid/gid for cgroup

* Fri Feb 6 2015   netblue30 <netblue30@yahoo.com> 0.9.20-1
 - utmp, btmp and wtmp enhancements
 -    create empty /var/log/wtmp and /var/log/btmp files in sandbox
 -    generate a new /var/run/utmp file in sandbox
 - CPU affinity, --cpu option
 - Linux control groups support, --cgroup option
 - Opera web browser support
 - VLC support
 - Added "empty" attribute to seccomp command to remove the default
 -    syscall list form seccomp blacklist
 - Added --nogroups option to disable supplementary groups for regular
 -   users. root user always runs without supplementary groups.
 - firemon enhancements
 -   display the command that started the sandbox
 -   added --caps option to display capabilities for all sandboxes
 -   added --cgroup option to display the control groups for all sandboxes
 -   added --cpu option to display CPU affinity for all sandboxes
 -   added --seccomp option to display seccomp setting for all sandboxes
 - New compile time options: --disable-chroot, --disable-bind
 - bugfixes

* Sat Dec 27 2014  netblue30 <netblue30@yahoo.com> 0.9.18-1
 - Support for tracing system, setuid, setgid, setfsuid, setfsgid syscalls
 - Support for tracing setreuid, setregid, setresuid, setresguid syscalls
 - Added profiles for transmission-gtk and transmission-qt
 - bugfixes

* Tue Nov 4 2014  netblue30 <netblue30@yahoo.com> 0.9.16-1
 - Configurable private home directory
 - Configurable default user shell
 - Software configuration support for --docdir and DESTDIR
 - Profile file support for include, caps, seccomp and private keywords
 - Dropbox profile file
 - Linux capabilities and seccomp filters enabled by default for Firefox,
  Midori, Evince and Dropbox
 - bugfixes

* Wed Oct 8 2014  netblue30 <netblue30@yahoo.com> 0.9.14-1
 - Linux capabilities and seccomp filters are automatically enabled in
   chroot mode (--chroot option) if the sandbox is started as regular
   user
 - Added support for user defined seccomp blacklists
 - Added syscall trace support
 - Added --tmpfs option
 - Added --balcklist option
 - Added --read-only option
 - Added --bind option
 - Logging enhancements
 - --overlay option was reactivated
 - Added firemon support to print the ARP table for each sandbox
 - Added firemon support to print the route table for each sandbox
 - Added firemon support to print interface information for each sandbox
 - bugfixes

* Tue Sep 16 2014 netblue30 <netblue30@yahoo.com> 0.9.12-1
 - Added capabilities support
 - Added support for CentOS 7
 - bugfixes
