#
# Conditional build:
%bcond_with	bootstrap	# bootstrap (using binary servletapi5/jsp)
#
%include	/usr/lib/rpm/macros.java
Summary:	The Jakarta Commons Extension Language
Summary(pl.UTF-8):	Jakarta Commons Extension Language - język rozszerzeń Jakarta Commons
Name:		commons-el
Version:	1.0
Release:	0.1
License:	Apache Software License
Group:		Development/Languages/Java
Source0:	http://www.apache.org/dist/jakarta/commons/el/source/%{name}-%{version}-src.tar.gz
# Source0-md5:	25038283a0b5f638db5e891295d20020
Source1:	http://www.apache.org/dist/tomcat/tomcat-5/v5.5.23/bin/apache-tomcat-5.5.23.zip
# Source1-md5:	4a7e5c2ff3c20a114fbfc5a122d7247c
Patch0:		%{name}-license.patch
Patch1:		%{name}-ant.patch
URL:		http://jakarta.apache.org/commons/el/
BuildRequires:	ant
BuildRequires:	jpackage-utils >= 0:1.6
BuildRequires:	junit
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
%if %{without bootstrap}
BuildRequires:	jsp
BuildRequires:	servletapi5
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An implementation of standard interfaces and abstract classes for
javax.servlet.jsp.el which is part of the JSP 2.0 specification.

%description -l pl.UTF-8
Implementacja standardowych interfejsów i klas abstrakcyjnych dla
javax.servlet.jsp.el, będących częścią specyfikacji JSP 2.0.

%package javadoc
Summary:	Javadoc for %{name}
Summary(pl.UTF-8):	Dokumentacja javadoc dla commons-el
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Javadoc for %{name}.

%description javadoc -l pl.UTF-8
Dokumentacja javadoc dla commons-el.

%prep
%setup -q -n %{name}-%{version}-src %{?with_bootstrap:-a1}
%patch0 -p1
%patch1 -p1
%if %{with bootstrap}
ln -s apache-tomcat-* tomcat
%endif

%build
%if %{with bootstrap}
dir=$(pwd)
servlet_api=$dir/tomcat/common/lib/servlet-api.jar
jsp_api=$dir/tomcat/common/lib/jsp-api.jar
%else
servlet_api=$(build-classpath build-classpath servletapi5)
jsp_api=$(build-classpath build-classpath jspapi)
%endif

cat > build.properties <<EOF
build.compiler=modern
junit.jar=$(build-classpath junit)
servlet-api.jar=$servlet_api
jsp-api.jar=$jsp_api
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
for a in dist/*.jar; do
	jar=${a##*/}
	cp -a dist/$jar $RPM_BUILD_ROOT%{_javadir}/${jar%%.jar}-%{version}.jar
	ln -s ${jar%%.jar}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/$jar
done

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
	rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(644,root,root,755)
%doc LICENSE.txt STATUS.html
%{_javadir}/*.jar

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
