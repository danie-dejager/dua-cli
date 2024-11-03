%define name dua
%define version 2.29.4
%define release 1%{?dist}

Summary:  View disk space usage and delete unwanted data, fast.
Name:     %{name}
Version:  %{version}
Release:  %{release}
License:  MIT License
URL:      https://github.com/Byron/dua-cli
Source0:  https://github.com/Byron/dua-cli/archive/refs/tags/v%{version}.tar.gz

%define debug_package %{nil}

BuildRequires: curl
BuildRequires: gcc

%description
View disk space usage and delete unwanted data, fast.

%prep
%setup -q -n dua-cli-%{version}

%build
# Install Rust using curl
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
export PATH="$PATH:$HOME/.cargo/bin"
cargo build --release

%install
# Create the necessary directory structure in the buildroot
mkdir -p %{buildroot}/bin

# Copy the binary to /bin in the buildroot
strip target/release/dua
install -m 755 target/release/dua %{buildroot}/bin/

%files
# List all the files to be included in the package
/bin/dua

%changelog
* Sun Nov 3 2024 - Danie de Jager - 2.29.4-1
* Thu Sep 12 2024 Danie de Jager - 2.29.2-2
* Sun Aug 11 2024 Danie de Jager - 2.29.2-1
* Thu Jul 4 2024 Danie de Jager - 2.29.0-4
* Sat May 11 2024 Danie de Jager - 2.29.0-3
- Built with rustc 1.78.0
* Mon May 6 2024 Danie de Jager - 2.29.0-2
- Built with rustc 1.77.2
* Sun Mar 10 2024 Danie de Jager - 2.29.0-1
* Thu Jan 25 2024 Danie de Jager - 2.28.0-2
- Initial RPM build
