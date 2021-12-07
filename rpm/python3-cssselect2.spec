# Adapted for SailfishOS
# + Disable check by default
# + Remove redundant python-cssselect2

%define srcname cssselect2
%global py3_prefix python3
%bcond_with check

Name:           python3-%{srcname}
Version:        0.4.1
Release:        1
Summary:        CSS selectors for Python ElementTree
License:        BSD
URL:            https://%{srcname}.readthedocs.io/
BuildArch:      noarch
Source0:        %{name}-%{version}.tar.gz

# patch present in master:
# https://github.com/Kozea/cssselect2/commit/6a8b3769a51420702ab5644af41200053809c6d2
#Patch0:         cssselect2-fix-isort.patch

BuildRequires:  %{py3_prefix}-devel
BuildRequires:  %{py3_prefix}-setuptools >= 39.2.0
%if %{with check}
BuildRequires:  %{py3_prefix}-pytest
BuildRequires:  %{py3_prefix}-pytest-cov
BuildRequires:  %{py3_prefix}-pytest-isort
BuildRequires:  %{py3_prefix}-pytest-runner
%endif
BuildRequires:  %{py3_prefix}-tinycss2
BuildRequires:  %{py3_prefix}-webencodings
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3dist(toml)
BuildRequires:  python3dist(pip)
BuildRequires:  python3dist(flit)
%{?python_provide:%python_provide %{py3_prefix}-cssselect2}
%global _version %(echo %{version}|sed -e 's/\+.*//')

%description
cssselect2 is a straightforward implementation of CSS3 Selectors for markup
documents (HTML, XML, etc.) that can be read by ElementTree-like parsers,
including cElementTree, lxml, html5lib_, etc.


%prep
%autosetup -p1 -n %{name}-%{version}/upstream
# Skip the flake8 plugin: linting is useful for upstream only. Also flake8 was
# not available in time for the Python 3.9 rebuild (and that might be the case
# for Python 3.10+) so let's just remove it.
#sed -i 's/--flake8//' setup.cfg


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files cssselect2

%check
%if %{with check}
%{__python3} -m pytest -v
# remove files which are only required for unit tests
%endif
rm -rf %{buildroot}%{python3_sitelib}/%{srcname}/tests

%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc README.rst
