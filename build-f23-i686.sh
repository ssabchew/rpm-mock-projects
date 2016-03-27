#!/bin/bash

set -x
set -e

#ARCH=${ARCH:-$(uname -m)}
ARCH=i386
BARCH=i686
RELEASEVER=23
DIST=f${RELEASEVER}
MOCKCFG="fedora-${RELEASEVER}-${ARCH}"
REPO_SSH='root@repo'
REPO_DST_PATH='/srv/www/repo/'
REPO_SSH_DIR=${REPO_DST_PATH}/fedora/${RELEASEVER}/

chk_srcs() {
    spectool -g "$1"
}


pre_check() {
    local distro="$1"
    local ARCH="$2"
    if [ -z "$distro" ]; then
        echo "Distro argumetn empty!"
        exit 254
    fi

    for i in ~/repo-"$distro"{,/$ARCH,/.gnupg,/repodata,/SRPMS,/rpmbuild,/rpmbuild/tmp}; do
        if [ ! -d "$i" ]; then
            mkdir -p "$i"
        fi
    done

    if [ ! -d ~/repo-"$distro"/$ARCH ]; then
        mkdir -p ~/repo-"$distro"/$ARCH
    fi

    if [ ! -f ~/repo-"$distro"/.rpmmacros ]; then
        cat <<EOF > ~/repo-"$distro"/.rpmmacros
%__arch_install_post   /usr/lib/rpm/check-rpaths   /usr/lib/rpm/check-buildroot

%_topdir		%(echo \$HOME)/rpmbuild
%_tmppath		%{_topdir}/tmp
%_smp_mflags		-j3

%packager		Stiliyan Sabchew
%vendor			Stiliyan Sabchew
%_signature             gpg
%_gpg_name		repo-build@ssabchew.info
EOF
    fi

    if [ ! -d ~/repo-"$distro"/.gnupg ]; then
        echo "****************************************************************"
        echo "*** copy .gnupg to ~/repo-"$distro"/.gnupg to enable signing ***"
        echo "****************************************************************"
        sleep 1
    fi

}


pre_check "$DIST" "$ARCH"

chk_srcs *.spec

rm -rf output/*.rpm

mock -r "$MOCKCFG" --buildsrpm --sources=./ --spec *.spec --resultdir=output/ # --no-cleanup-after

mock -r "$MOCKCFG" --rebuild output/*.src.rpm --resultdir=output/ # --no-cleanup-after

if [ -d ~/repo-"$DIST"/.gnupg ]; then
    HOME=~/repo-"$DIST"/ rpmsign --addsign output/*.rpm
fi

if ls output/*.src.rpm > /dev/null 2>&1; then
    cp output/*.src.rpm ~/repo-"$DIST"/SRPMS/
fi

if ls output/*.nosrc.rpm > /dev/null 2>&1; then
    cp output/*.nosrc.rpm ~/repo-"$DIST"/SRPMS/
fi

if ls output/*.noarch.rpm > /dev/null 2>&1; then
    cp output/*.noarch.rpm ~/repo-"$DIST"/$ARCH/
fi

if ls output/*.$ARCH.rpm > /dev/null 2>&1; then
    cp output/*.$ARCH.rpm ~/repo-"$DIST"/$ARCH/
fi

createrepo --pretty --database ~/repo-"$DIST"/

if [ ! -d ~/repo-"$DIST"/.gnupg ]; then
    echo "Not sending to the repo, not signed"
    exit 0
fi

read -e -n 1 -t 30 -p 'Send to the repo (y/N): ' REPLY
if [ "$REPLY" != 'y' ] && [ "$REPLY" != 'Y' ]; then
    echo "OK, not sending to the repo."
    exit 0
fi

if ls output/*.src.rpm > /dev/null 2>&1; then
    scp output/*.src.rpm "$REPO_SSH:$REPO_SSH_DIR/SRPMS/"
fi

if ls output/*.nosrc.rpm > /dev/null 2>&1; then
    scp output/*.nosrc.rpm "$REPO_SSH:$REPO_SSH_DIR/SRPMS/"
fi

if ls output/*.noarch.rpm > /dev/null 2>&1; then
    scp output/*.noarch.rpm "$REPO_SSH:$REPO_SSH_DIR/$ARCH/os/"
fi

if ls output/*."$BARCH".rpm > /dev/null 2>&1; then
    for i in output/*."$BARCH".rpm; do
        if [[ "$i" =~ .*-debuginfo-.*\.rpm ]]; then
            scp "$i" "$REPO_SSH:$REPO_SSH_DIR/$ARCH/debug/"
        else
            scp "$i" "$REPO_SSH:$REPO_SSH_DIR/$ARCH/os/"
        fi
    done
fi

#ssh "$REPO_SSH" "cd $REPO_DST_PATH; ./mkrepo-$DIST.sh"
#echo 'Run mkrepo on the repo...'


echo 'OK!'
