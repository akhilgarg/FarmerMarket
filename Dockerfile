FROM centos:centos7

RUN yum clean all && \
    yum -y install epel-release && \
    yum -y install python3 && \
    yum -y install git && \
    yum clean all && \
    rm -rf /var/cache/yum

MAINTAINER Akhil Garg (email@domain.com)

WORKDIR /root
RUN whoami
RUN git clone https://github.com/akhilgarg/FarmerMarket.git
RUN pwd
RUN ls -l FarmerMarket/FarmerMarket
RUN pip3 install -r /root/FarmerMarket/FarmerMarket/requirements.txt

RUN python3 --version

WORKDIR /root/FarmerMarket/FarmerMarket
RUN ls -l

CMD ["python3", "checkout.py", "&"]

EXPOSE 5000
