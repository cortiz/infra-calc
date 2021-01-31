FROM python:alpine
WORKDIR /infracalc
COPY dist/infracalc-0.2.0.tar.gz infracalc.tar
RUN pip install ./infracalc.tar
ENTRYPOINT ["infracalc"]
