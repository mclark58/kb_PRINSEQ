FROM kbase/kbase:sdkbase.latest
MAINTAINER KBase Developer
# -----------------------------------------

# Insert apt-get instructions here to install
# any required dependencies for your module.

# RUN apt-get update
RUN cd /opt \
    && mkdir lib \
    && cd lib \
    && wget -o prinseq-lite-0.20.4.tar.gz 'https://downloads.sourceforge.net/project/prinseq/standalone/prinseq-lite-0.20.4.tar.gz?r=https%3A%2F%2Fsourceforge.net%2Fprojects%2Fprinseq%2Ffiles%2Fstandalone%2Fprinseq-lite-0.20.4.tar.gz%2Fdownload&ts=1497050557&use_mirror=gigenet' \
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
