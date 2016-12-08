FROM kbase/kbase:sdkbase.latest
MAINTAINER KBase Developer
# -----------------------------------------

# Insert apt-get instructions here to install
# any required dependencies for your module.

# RUN apt-get update
RUN cd /opt \
    && mkdir lib \
    && cd lib \
    && wget "https://sourceforge.net/projects/prinseq/files/standalone/prinseq-lite-0.20.4.tar.gz" \
    && tar -zxvf prinseq-lite-0.20.4.tar.gz \
    && cd prinseq-lite-0.20.4 \
    && chmod +x prinseq-lite.pl \
    && ls -l


# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod 777 /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
