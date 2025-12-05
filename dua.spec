%define name dua
%define version 2.32.2
%define release 2%{?dist}

Summary: View disk space usage and delete unwanted data, fast.
Name: %{name}
Version: %{version}
Release: %{release}
License: MIT
URL: https://github.com/Byron/dua-cli
Source0: https://github.com/Byron/dua-cli/archive/refs/tags/v%{version}.tar.gz

%define debug_package %{nil}

BuildRequires: curl
BuildRequires: gcc

%description
View disk space usage and delete unwanted data, fast.

%package zsh
Summary: Zsh completions for %{name}
Requires: %{name} = %{version}-%{release}

%description zsh
Zsh shell completions for %{name}.

%package fish
Summary: Fish completions for %{name}
Requires: %{name} = %{version}-%{release}

%description fish
Fish shell completions for %{name}.

%prep
%setup -q -n dua-cli-%{version}

%build
# Install Rust using curl
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
export PATH="$PATH:$HOME/.cargo/bin"
cargo build --release

%install
# Create the necessary directory structure in the buildroot
install -D -m 755 target/release/dua %{buildroot}%{_bindir}/dua

# Generate completion scripts
mkdir -p completions
./target/release/dua completions bash > completions/dua.bash
./target/release/dua completions zsh  > completions/_dua
./target/release/dua completions fish > completions/dua.fish

# Install bash completions
install -D -m 644 completions/dua.bash %{buildroot}%{_datadir}/bash-completion/completions/dua

# Install zsh completions
install -D -m 644 completions/_dua %{buildroot}%{_datadir}/zsh/site-functions/_dua

# Install fish completions
install -D -m 644 completions/dua.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/dua.fish

%files
%license LICENSE
%{_bindir}/dua
%{_datadir}/bash-completion/completions/dua

%files zsh
%{_datadir}/zsh/site-functions/_dua

%files fish
%{_datadir}/fish/vendor_completions.d/dua.fish

%changelog
* Fri Dec 5 2025 - Danie de Jager - 3.32.2-2
* Tue Oct 28 2025 - Danie de Jager - 3.32.2-1
* Mon Sep 15 2025 - Danie de Jager - 3.32.0-1
* Sun Sep 14 2025 - Danie de Jager - 3.31.0-2
* Wed Aug 6 2025 - Danie de Jager - 3.31.0-1
* Sat Jul 26 2025 - Danie de Jager - 3.30.1-2
* Sun May 11 2025 - Danie de Jager - 3.30.1-1
* Wed Feb 26 2025 - Danie de Jager - 3.30.0-2
* Tue Jan 28 2025 - Danie de Jager - 3.30.0-1
* Fri Dec 27 2024 - Danie de Jager - 2.29.4-2
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
