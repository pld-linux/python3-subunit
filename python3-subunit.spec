#
# Conditional build:
%bcond_without	tests	# unit tests

Summary:	subunit - streaming protocol for test results
Summary(pl.UTF-8):	subunit - protokół strumieniowy do wyników testów
Name:		python3-subunit
Version:	1.4.3
Release:	1
License:	Apache v2.0 or BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/python-subunit/
Source0:	https://files.pythonhosted.org/packages/source/p/python-subunit/python-subunit-%{version}.tar.gz
# Source0-md5:	30ed3d6a2586a5e29ab560c12735c58a
Patch0:		python-subunit-tests.patch
URL:		https://pypi.org/project/python-subunit/
BuildRequires:	python3-modules >= 1:3.7
BuildRequires:	python3-setuptools >= 1:43
BuildRequires:	python3-testtools >= 0.9.34
%if %{with tests}
BuildRequires:	python3-fixtures
BuildRequires:	python3-hypothesis
BuildRequires:	python3-testscenarios
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python3-modules >= 1:3.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Subunit is a streaming protocol for test results.

This package contains Python 3.x modules.

%description -l pl.UTF-8
Subunit to protokół strumieniowy przeznaczony do wyników testów.

Ten pakiet zawiera moduły Pythona 3.x.

%package -n subunit-python3
Summary:	Python 3 tools for subunit streaming protocol for test results
Summary(pl.UTF-8):	Narzędzia Pythona 3 dla protokołu strumieniowego do wyników testów subunit
Group:		Development/Tools
Requires:	python3-subunit = %{version}-%{release}

%description -n subunit-python3
Python 3 tools for subunit streaming protocol for test results.

%description -n subunit-python3 -l pl.UTF-8
Narzędzia Pythona 3 dla protokołu strumieniowego do wyników testów
subunit.

%package -n subunit-python
Summary:	Python tools for subunit streaming protocol for test results
Summary(pl.UTF-8):	Pythonowe narzędzia dla protokołu strumieniowego do wyników testów subunit
Group:		Development/Tools
Requires:	subunit-python3 = %{version}-%{release}

%description -n subunit-python
Python tools for subunit streaming protocol for test results.

%description -n subunit-python -l pl.UTF-8
Pythonowe narzędzia dla protokołu strumieniowego do wyników testów
subunit.

%prep
%setup -q -n python-subunit-%{version}
%patch0 -p1

%build
%py3_build

%if %{with tests}
PYTHONPATH=$(pwd)/python \
%{__python3} -m subunit.run subunit.tests.test_suite | PYTHONPATH=$(pwd)/python %{__python3} python/subunit/filter_scripts/subunit2pyunit.py
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/subunit/tests

for f in $RPM_BUILD_ROOT%{_bindir}/* ; do
	if [ "${f%%-2}" = "$f" ]; then
		%{__mv} "$f" "${f}-3"
		ln -sf $(basename $f)-3 "$f"
	fi
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc NEWS README.rst
%{py3_sitescriptdir}/subunit
%{py3_sitescriptdir}/python_subunit-%{version}-py*.egg-info

%files -n subunit-python3
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/subunit-1to2-3
%attr(755,root,root) %{_bindir}/subunit-2to1-3
%attr(755,root,root) %{_bindir}/subunit-filter-3
%attr(755,root,root) %{_bindir}/subunit-ls-3
%attr(755,root,root) %{_bindir}/subunit-notify-3
%attr(755,root,root) %{_bindir}/subunit-output-3
%attr(755,root,root) %{_bindir}/subunit-stats-3
%attr(755,root,root) %{_bindir}/subunit-tags-3
%attr(755,root,root) %{_bindir}/subunit2csv-3
%attr(755,root,root) %{_bindir}/subunit2disk-3
%attr(755,root,root) %{_bindir}/subunit2gtk-3
%attr(755,root,root) %{_bindir}/subunit2junitxml-3
%attr(755,root,root) %{_bindir}/subunit2pyunit-3
%attr(755,root,root) %{_bindir}/tap2subunit-3

%files -n subunit-python
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/subunit-1to2
%attr(755,root,root) %{_bindir}/subunit-2to1
%attr(755,root,root) %{_bindir}/subunit-filter
%attr(755,root,root) %{_bindir}/subunit-ls
%attr(755,root,root) %{_bindir}/subunit-notify
%attr(755,root,root) %{_bindir}/subunit-output
%attr(755,root,root) %{_bindir}/subunit-stats
%attr(755,root,root) %{_bindir}/subunit-tags
%attr(755,root,root) %{_bindir}/subunit2csv
%attr(755,root,root) %{_bindir}/subunit2disk
%attr(755,root,root) %{_bindir}/subunit2gtk
%attr(755,root,root) %{_bindir}/subunit2junitxml
%attr(755,root,root) %{_bindir}/subunit2pyunit
%attr(755,root,root) %{_bindir}/tap2subunit
