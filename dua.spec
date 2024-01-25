%define name dua
%define version 2.28.0
%define release 2%{?dist}

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
* Thu Jan 25 2024 Danie de Jager - 2.28.0-2
- Initial RPM build
