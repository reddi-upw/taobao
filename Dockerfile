FROM centos:7.2.1511

RUN yum -y install epel-release
RUN yum -y update && \
    yum install -y zlib-devel saslwrapper-devel cyrus-sasl-devel \
    libxml2-devel libxslt-devel lapack-devel liblas-devel libffi-devel postgresql-devel \
    rsync grep screen tzdata redhat-lsb-core wget python-pip python34-devel python34 python34-setuptools
RUN yum groupinstall -y "Development tools" && yum clean all

RUN mkdir -p /taobao

RUN localedef -c -i en_US -f UTF-8 en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

RUN easy_install-3.4 pip

RUN pip3 install --upgrade pip ipython ipdb

COPY requirements.txt /
RUN pip3 install -r /requirements.txt

WORKDIR /taobao

COPY . /taobao
