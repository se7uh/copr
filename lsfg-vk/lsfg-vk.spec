%global debug_package %{nil}
%global toolchain clang

Name:           lsfg-vk
Version:        2.0.0
Release:        1%{?dist}
Summary:        Lossless Scaling Frame Generation on Linux

# Upstream is CC BY-NC-ND 4.0. The NoDerivatives clause forbids patching:
# never add Patch: lines or sed the sources here. Apache-2.0 and MIT come
# from the vendored thirdparty/ headers.
License:        CC-BY-NC-ND-4.0 AND Apache-2.0 AND MIT
URL:            https://lsfg-vk.dev/
# cgit only serves .tar.xz snapshots.
# sha256: abb688feac00d50f9e59dabb2476998bc1d3f0290fb971407d49cba26dd44b3b
Source0:        https://git.lsfg-vk.dev/lsfg-vk/snapshot/lsfg-vk-%{version}.tar.xz

BuildRequires:  clang
BuildRequires:  llvm
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  qt6-qtdeclarative-devel

# The layer dlopens libvulkan.so.1, so RPM cannot detect this dependency.
Requires:       vulkan-loader
Recommends:     %{name}-ui

%description
lsfg-vk brings Lossless Scaling frame generation to Linux by implementing a
Vulkan layer.

It requires the proprietary lsfg-vk.dll that ships with Lossless Scaling on
Steam. That file is not included in this package; install Lossless Scaling
from your Steam library first.

%package ui
Summary:        Qt6 configuration editor for lsfg-vk
Requires:       %{name} = %{version}-%{release}
Requires:       qt6-qtdeclarative

%description ui
Graphical configuration editor for lsfg-vk, built with Qt6 Quick.

%prep
# No patches: upstream is licensed CC BY-NC-ND 4.0 (NoDerivatives).
%autosetup

%build
# CMAKE_DISABLE_FIND_PACKAGE_Git stops Version.cmake from falling back to
# git-describe. Without it, a tarball build reports a bogus version such as
# "128.r128.g128-dirty" instead of 2.0.0.
%cmake \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INTERPROCEDURAL_OPTIMIZATION=ON \
  -DCMAKE_DISABLE_FIND_PACKAGE_Git=ON \
  -DLSFGVK_BUILD_LAYER=ON \
  -DLSFGVK_BUILD_CLI=ON \
  -DLSFGVK_BUILD_UI=ON \
  -DLSFGVK_MANAGED=ON
%cmake_build

%install
%cmake_install

%check
grep -qF '%{version}' %{buildroot}%{_bindir}/lsfg-vk-cli
! grep -qF -- '-dirty' %{buildroot}%{_bindir}/lsfg-vk-cli

%files
%license LICENSE.txt
%{_libdir}/liblsfg-vk-layer.so
%{_datadir}/vulkan/implicit_layer.d/VkLayer_LSFGVK_frame_generation.json
%{_bindir}/lsfg-vk-cli

%files ui
%{_bindir}/lsfg-vk-ui
%{_datadir}/applications/gay.pancake.lsfg-vk-ui.desktop
%{_datadir}/icons/hicolor/256x256/apps/gay.pancake.lsfg-vk-ui.png

%changelog
* Wed Nov 11 2026 boobaa <xenialv7@gmail.com> - 2.0.0-1
- Initial package for Fedora COPR
