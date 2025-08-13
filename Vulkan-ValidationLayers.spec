#
# Conditional build:
%bcond_without	wayland		# Wayland support
%bcond_without	x11		# X11 (Xlib/XCB) support

%define	api_version	1.4.321.0
%define	gitref		vulkan-sdk-%{api_version}

Summary:	Vulkan Validation Layers (VVL)
Summary(pl.UTF-8):	Vulkan Validation Layers (VVL) - warstwy sprawdzania poprawności
Name:		Vulkan-ValidationLayers
Version:	%{api_version}
Release:	1
License:	Apache v2.0
Group:		Applications/Graphics
#Source0Download: https://github.com/KhronosGroup/Vulkan-ValidationLayers/tags
Source0:	https://github.com/KhronosGroup/Vulkan-ValidationLayers/archive/%{gitref}/%{name}-%{gitref}.tar.gz
# Source0-md5:	df6d480d5baf24dd82fece3b71766628
URL:		https://github.com/KhronosGroup/Vulkan-ValidationLayers
BuildRequires:	Vulkan-Loader-devel >= %{api_version}
BuildRequires:	Vulkan-Utility-Libraries >= %{api_version}
BuildRequires:	cmake >= 3.22.1
BuildRequires:	libstdc++-devel >= 6:7
%{?with_x11:BuildRequires:	libxcb-devel}
BuildRequires:	pkgconfig
BuildRequires:	python3 >= 1:3
BuildRequires:	robin_hood-devel
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	spirv-headers >= 1.6.1-5
BuildRequires:	spirv-tools >= 1:2025.1
%{?with_wayland:BuildRequires:	wayland-devel}
%{?with_x11:BuildRequires:	xorg-lib-libX11-devel}
Obsoletes:	vulkan-sdk-validation-layers < 1.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Vulkan is an Explicit API, enabling direct control over how GPUs
actually work. By design, minimal error checking is done inside a
Vulkan driver. Applications have full control and responsibility for
correct operation. Any errors in how Vulkan is used can result in a
crash. This project provides Vulkan validation layers that can be
enabled to assist development by enabling developers to verify their
applications correct use of the Vulkan API.

%description -l pl.UTF-8
Vulkan to bezpośrednie API, umożliwiające bezpośrednie sterowanie
działaniem GPU. Zgodnie z projektem w sterowniku Vulkan zachodzi
minimalne sprawdzanie błędów. Aplikacje mają pełną kontrolę i
odpowiedzialność za poprawność operacji. Błędy w użyciu Vulkana
mogą skutkować awarią. Ten projekt zapewnia warstwy sprawdzania
poprawności Vulkana, umożliwiające programisom sprawdzanie
poprawnego użycia API Vulkan w aplikacjach.

%prep
%setup -q -n %{name}-%{gitref}

%build
%cmake -B build \
	%{!?with_wayland:-DBUILD_WSI_WAYLAND_SUPPORT=OFF} \
	%{!?with_x11:-DBUILD_WSI_XCB_SUPPORT=OFF} \
	%{!?with_x11:-DBUILD_WSI_XLIB_SUPPORT=OFF}

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libVkLayer_khronos_validation.so
%{_datadir}/vulkan/explicit_layer.d/VkLayer_khronos_validation.json
