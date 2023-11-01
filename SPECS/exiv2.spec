
%undefine __cmake_in_source_build

Summary: Exif and Iptc metadata manipulation library
Name:    exiv2
Version: 0.27.5
%global internal_ver %{version}
Release: 2%{?dist}

License: GPLv2+
URL:     http://www.exiv2.org/
%if 0%{?beta:1}
Source0: https://github.com/Exiv2/%{name}/archive/v%{version}-%{beta}.tar.gz
%else
Source0: http://exiv2.org/builds/%{name}-%{version}-Source.tar.gz
%endif

## upstream patches

## security fixes

## upstreamable patches
Patch0: exiv2-no-rpath.patch

BuildRequires: cmake
BuildRequires: expat-devel
BuildRequires: gcc-c++
BuildRequires: gettext
BuildRequires: pkgconfig
BuildRequires: zlib-devel
# docs
BuildRequires: doxygen graphviz libxslt

Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description
A command line utility to access image metadata, allowing one to:
* print the Exif metadata of Jpeg images as summary info, interpreted values,
  or the plain data for each tag
* print the Iptc metadata of Jpeg images
* print the Jpeg comment of Jpeg images
* set, add and delete Exif and Iptc metadata of Jpeg images
* adjust the Exif timestamp (that's how it all started...)
* rename Exif image files according to the Exif timestamp
* extract, insert and delete Exif metadata (including thumbnails),
  Iptc metadata and Jpeg comments

%package devel
Summary: Header files, libraries and development documentation for %{name}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
%description devel
%{summary}.

%package libs
Summary: Exif and Iptc metadata manipulation library
# not strictly required, but convenient and expected
%if 0%{?rhel} && 0%{?rhel} <= 7
Requires: %{name} = %{version}-%{release}
%else
Recommends: %{name} = %{version}-%{release}
%endif
%description libs
A C++ library to access image metadata, supporting full read and write access
to the Exif and Iptc metadata, Exif MakerNote support, extract and delete
methods for Exif thumbnails, classes to access Ifd and so on.

%package doc
Summary: Api documentation for %{name}
BuildArch: noarch
%description doc
%{summary}.

%prep
%autosetup -n %{name}-%{version}-%{?beta}%{!?beta:Source} -p1

%build
%cmake \
  -DCMAKE_INSTALL_DOCDIR="%{_pkgdocdir}" \
  -DEXIV2_BUILD_DOC:BOOL=ON \
  -DEXIV2_ENABLE_NLS:BOOL=ON \
  -DEXIV2_BUILD_SAMPLES:BOOL=OFF

%cmake_build
%cmake_build --target doc


%install
%cmake_install

%find_lang exiv2 --with-man


%check
export PKG_CONFIG_PATH="%{buildroot}%{_libdir}/pkgconfig${PKG_CONFIG_PATH:+:}${PKG_CONFIG_PATH}"
test "$(pkg-config --modversion exiv2)" = "%{internal_ver}"
test "$(pkg-config --variable=libdir exiv2)" = "%{_libdir}"
test -x %{buildroot}%{_libdir}/libexiv2.so


%files -f exiv2.lang
%license COPYING
%doc doc/ChangeLog
# README is mostly installation instructions
#doc README.md
%{_bindir}/exiv2
%{_mandir}/man1/exiv2*.1*

%ldconfig_scriptlets libs

%files libs
%{_libdir}/libexiv2.so.27*
%{_libdir}/libexiv2.so.%{internal_ver}

%files devel
%{_includedir}/exiv2/
%{_libdir}/libexiv2.so
%{_libdir}/pkgconfig/exiv2.pc
%{_libdir}/cmake/exiv2/
# todo: -static subpkg?  -- rex
%{_libdir}/libexiv2-xmp.a

%files doc
%{_pkgdocdir}/
%exclude %{_pkgdocdir}/ChangeLog


%changelog
* Mon Nov 15 2021 Jan Grulich <jgrulich@redhat.com> - 0.27.5-2
- Remove RPATH
  Resolves: bz#2018421

* Fri Nov 12 2021 Jan Grulich <jgrulich@redhat.com> - 0.27.5-1
- Exiv2 0.27.5
  Resolves: bz#2018421

  Fix stack exhaustion issue in the printIFDStructure function leading to DoS
  Resolves: bz#2003670

* Tue Aug 24 2021 Jan Grulich <jgrulich@redhat.com> - 0.27.4-7
- Properly install POC files
  Resolves: bz#1993247
  Resolves: bz#1993284

* Tue Aug 24 2021 Jan Grulich <jgrulich@redhat.com> - 0.27.4-6
- Include missing tests for CVEs
  Resolves: bz#1993247
  Resolves: bz#1993284

* Wed Aug 18 2021 Jan Grulich <jgrulich@redhat.com> - 0.27.4-5
- Fix test for CVE-2021-29470
  Resolves: bz#1993284

* Wed Aug 18 2021 Jan Grulich <jgrulich@redhat.com> - 0.27.4-4
- Fix out-of-bounds read in Exiv2::Jp2Image::printStructure
  Resolves: bz#1993247

- Fix out-of-bounds read in Exiv2::Jp2Image::encodeJp2Header
  Resolves: bz#1993284

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 0.27.4-3
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Thu Aug 05 2021 Jan Grulich <jgrulich@redhat.com> - 0.27.4-2
- Do not duplicate changelog file
  Resolves: bz#1989848

* Wed Aug 04 2021 Jan Grulich <jgrulich@redhat.com> - 0.27.4-1
- 0.27.4
  Resolves: bz#1989848

* Tue Jun 01 2021 Jan Grulich <jgrulich@redhat.com> - 0.27.3-9
- Bump version for rebuild (binutils)
  Resolves: bz#1964183
  Resolves: bz#1964189

* Tue May 25 2021 Jan Grulich <jgrulich@redhat.com> - 0.27.3-8
- CVE-2021-29623 exiv2: a read of uninitialized memory may lead to information leak
  Resolves: bz#1964183

- CVE-2021-32617 exiv2: DoS due to quadratic complexity in ProcessUTF8Portion
  Resolves: bz#1964189

* Mon May 03 2021 Jan Grulich <jgrulich@redhat.com> - 0.27.3-7
- CVE-2021-3482: Fix heap-based buffer overflow in Jp2Image::readMetadata()
  CVE-2021-29458 exiv2: out-of-bounds read in Exiv2::Internal::CrwMap::encode
  CVE-2021-29457 exiv2: heap-based buffer overflow in Exiv2::Jp2Image::doWriteMetadata
  CVE-2021-29470 exiv2: out-of-bounds read in Exiv2::Jp2Image::encodeJp2Header
  CVE-2021-29473 exiv2: out-of-bounds read in Exiv2::Jp2Image::doWriteMetadata
  Resolves: bz#1956174

* Thu Apr 15 2021 Mohan Boddu <mboddu@redhat.com> - 0.27.3-6
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.27.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Aug 26 2020 Rex Dieter <rdieter@fedoraproject.org> - 0.27.3-4
- support new cmake macro semantics

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.27.3-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.27.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 30 2020 Rex Dieter <rdieter@fedoraproject.org> - 0.27.3-1
- 0.27.3

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.27.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jul 29 2019 Rex Dieter <rdieter@fedoraproject.org> - 0.27.2-1
- 0.27.2

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.27.2-0.2.RC2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 16 2019 Rex Dieter <rdieter@fedoraproject.org> - 0.27.2-0.1.RC2
- 0.27.2-RC2 (#1720353)

* Fri Apr 26 2019 Rex Dieter <rdieter@fedoraproject.org> - 0.27.1-1
- exiv-0.27.1 (#1696117)

* Thu Jan 31 2019 Rex Dieter <rdieter@fedoraproject.org> - 0.27.0-3
- -devel: Requires: expat-devel

* Wed Jan 30 2019 Rex Dieter <rdieter@fedoraproject.org> - 0.27.0-2
- pull in upstream fix for pkgconfig exiv2.pc

* Thu Jan 10 2019 Rex Dieter <rdieter@fedoraproject.org> - 0.27.0-1
- exiv2-0.27.0 (#1665246)

* Thu Jan 10 2019 Rex Dieter <rdieter@fedoraproject.org> - 0.26-13
- backport pentax DNG crasher (#1585514, exiv2#201)

* Tue Jul 24 2018 Jan Grulich <jgrulich@redhat.com> - 0.26-12
- Security fix for CVE-2017-17723, CVE-2017-17725, CVE-2018-10958, CVE-2018-10998,
  CVE-2018-11531, CVE-2018-12264, CVE-2018-12265, CVE-2018-14046, CVE-2018-5772,
  CVE-2018-8976, CVE-2018-8977, CVE-2018-9144

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May 03 2018 Germano Massullo <germano.massullo@gmail.com> - 0.26-10
- added patches that fix CVE-2017-17723 CVE-2017-17725 CVE-2017-5772
- moved 0006-1296-Fix-submitted.patch file from sources to package tree

* Tue Feb 20 2018 Rex Dieter <rdieter@fedoraproject.org> - 0.26-9
- BR: gcc-c++

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.26-7
- Switch to %%ldconfig_scriptlets

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.26-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun May 28 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.26-4
- Security fix for CVE-2017-9239 (#1455859,#1455860)

* Sat May 20 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.26-3
- -libs: use Recommends: instead (#1452938)

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Tue May 02 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.26-1
- exiv2-0.26 (#1447129)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Feb 22 2016 Rex Dieter <rdieter@fedoraproject.org> 0.25-3
- embedded copy of exempi should be compiled with BanAllEntityUsage (#888769)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jun 22 2015 Rex Dieter <rdieter@fedoraproject.org> 0.25-1
- exiv2-0.25 (#1234185)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Apr 14 2015 Rex Dieter <rdieter@fedoraproject.org> 0.24-6
- rebuild (gcc5)

* Thu Feb 19 2015 Rex Dieter <rdieter@fedoraproject.org> 0.24-5
- rebuild (gcc5)

* Mon Jan 05 2015 Rex Dieter <rdieter@fedoraproject.org> 0.24-4
- CVE-2014-9449 exiv2: buffer overflow in RiffVideo::infoTagsHandler (#1178909)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Dec 02 2013 Rex Dieter <rdieter@fedoraproject.org> - 0.24-1
- exiv2-0.24, abi bump
- -doc subpkg
- ready experimental cmake buildsystem support

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 14 2012 Rex Dieter <rdieter@fedoraproject.org> 0.23-3
- empty html doc dir (#848025)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 24 2012 Rex Dieter <rdieter@fedoraproject.org> 0.23-1
- exiv2-0.23
- abi bump

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-5
- Rebuilt for c++ ABI breakage

* Mon Jan 16 2012 Rex Dieter <rdieter@fedoraproject.org> 0.22-4
- better rpath handling
- revert locale change, move back to -libs

* Mon Jan 16 2012 Rex Dieter <rdieter@fedoraproject.org> 0.22-3
- move locale files to main pkg (from -libs)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 14 2011 Rex Dieter <rdieter@fedoraproject.org> 0.22-1
- exiv2-0.22

* Tue Sep 27 2011 Rex Dieter <rdieter@fedoraproject.org> 0.21.1-3
- New Tamron 70-300 mm lens improperly recognized (#708403)

* Mon Sep 26 2011 Rex Dieter <rdieter@fedoraproject.org> 0.21.1-2
- gthumb crashes because of bug in exiv2 0.21.1 (#741429)

* Sat Feb 26 2011 Rex Dieter <rdieter@fedoraproject.org> 0.21.1-1
- exiv2-0.21.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Rex Dieter <rdieter@fedoraproject.org> 0.21-2
- Move ldconfig scriptlet calls to -libs (#672361)

* Wed Dec 01 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.21-1
- exiv2-0.21

* Sun May 30 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.20-1
- exiv2-0.20

* Wed Dec 30 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.19-1
- exiv2-0.19 (#552275)

* Sun Dec 13 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.18.2-3
- -libs unconditional
- tighten deps using %%?_isa

* Fri Aug 07 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.18.2-2
- (again) drop -fvisibility-inlines-hidden (#496050)

* Fri Jul 24 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.18.2-1
- exiv2-0.18.2
- drop visibility patch

* Fri Apr 17 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.18.1-1
- exiv2-0.18.1
- drop -fvisibility-inlines-hidden (#496050)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 18 2008 Rex Dieter <rdieter@fedoraproject.org> 0.18-1
- exiv2-0.18

* Fri Dec 12 2008 Rex Dieter <rdieter@fedoraproject.org> 0.17.2-2
- rebuild for pkgconfig deps

* Mon Jun 23 2008 Rex Dieter <rdieter@fedoraproject.org> 0.17.1-1
- exiv2-0.17.1

* Mon Feb 11 2008 Rex Dieter <rdieter@fedoraproject.org> 0.16-2
- respin (gcc43)
- gcc43 patch

* Sun Jan 13 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 0.16-1
- eviv2-0.16

* Mon Dec 17 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.16-0.3.pre1
- CVE-2007-6353 (#425924)

* Mon Nov 26 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.16-0.2.pre1
- -libs subpkg toggle (f8+)

* Tue Nov 13 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.16-0.1.pre1
- exiv2-0.16-pre1

* Tue Sep 18 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.15-4
- -libs: -Requires: %%name

* Tue Aug 21 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.15-3
- -libs subpkg to be multilib-friendlier (f8+)

* Sat Aug 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.15-2
- License: GPLv2+

* Thu Jul 12 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.15-1
- exiv2-0.15

* Mon Apr 02 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.14-1
- exiv2-0.14

* Tue Nov 28 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.12-1
- exiv2-0.12

* Wed Oct 04 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.11-3
- respin

* Tue Sep 19 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.11-2
- BR: zlib-devel

* Tue Sep 19 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.11-1
- exiv2-0.11

* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.10-2
- fc6 respin

* Sat Jun 03 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.10-1
- 0.10

* Wed May 17 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.1-3
- cleanup %%description
- set eXecute bit on installed lib.
- no_rpath patch
- deps patch (items get (re)compiled on *every* call to 'make')

* Wed May 17 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.1-2
- %%post/%%postun: /sbin/ldconfig

* Tue May 16 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.1-1
- first try
