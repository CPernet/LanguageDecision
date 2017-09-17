FROM continuumio/miniconda3

RUN useradd -ms /bin/bash langdec

# Set the ENTRYPOINT to use bash
ENTRYPOINT [ "/bin/bash", "-c" ]

# Use the environment.yml to create the conda environment.
ADD environment-linux.yml /tmp/environment.yml
WORKDIR /tmp
RUN [ "conda", "env", "create", "-f", "environment.yml"]

ADD . /app

WORKDIR /app
RUN [ "/bin/bash", "-c", "source activate lang-dec" ]

COPY run-notebook.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/run-notebook.sh

USER langdec
CMD [ "run-notebook.sh" ]
