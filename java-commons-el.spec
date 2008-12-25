#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc

%include	/usr/lib/rpm/macros.java
Summary:	The Commons Extension Language
Summary(pl.UTF-8):	Commons Extension Language - język rozszerzeń Commons
Name:		java-commons-el
Version:	1.0
Release:	2
License:	Apache
Group:		Libraries/Java
Source0:	http://www.apache.org/dist/commons/el/source/commons-el-%{version}-src.tar.gz
# Source0-md5:	25038283a0b5f638db5e891295d20020
Patch0:		commons-el-license.patch
Patch1:		commons-el-ant.patch
URL:		http://commons.apache.org/commons/el/
BuildRequires:	ant
BuildRequires:	jpackage-utils >= 0:1.6
BuildRequires:	jsp
BuildRequires:	junit
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	servlet
Requires:	jpackage-utils
Provides:	jakarta-commons-el
Obsoletes:	commons-el
Obsoletes:	jakarta-commons-el
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An implementation of standard interfaces and abstract classes for
javax.servlet.jsp.el which is part of the JSP 2.0 specification.

%description -l pl.UTF-8
Implementacja standardowych interfejsów i klas abstrakcyjnych dla
javax.servlet.jsp.el, będących częścią specyfikacji JSP 2.0.

%package javadoc
Summary:	Javadoc for commons-el
Summary(pl.UTF-8):	Dokumentacja javadoc dla commons-el
Group:		Documentation
Requires:	jpackage-utils
Obsoletes:	commons-el-javadoc

%description javadoc
Javadoc for commons-el.

%description javadoc -l pl.UTF-8
Dokumentacja javadoc dla commons-el.

%prep
%setup -q -n commons-el-%{version}-src
%patch0 -p1
%patch1 -p1

%build
cat > build.properties <<EOF
build.compiler=modern
servlet-api.jar=$(find-jar servlet)
jsp-api.jar=$(find-jar jsp-api)
junit.jar=$(find-jar junit)

servletapi.build.notrequired=true
jspapi.build.notrequired=true
EOF

%ant \
	-Dcompile.source=1.4 \
	-Dfinal.name=commons-el \
	-Dj2se.javadoc=%{_javadocdir}/java \
	jar javadoc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}

# jars
cp -a dist/commons-el.jar $RPM_BUILD_ROOT%{_javadir}/commons-el-%{version}.jar
ln -s commons-el-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/commons-el.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -a dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%doc LICENSE.txt STATUS.html
%{_javadir}/*.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}
%endif
