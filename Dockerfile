FROM finalduty/archlinux:monthly
#FROM kpouget/tuto-gdb.py
MAINTAINER Kevin Pouget <kpouget@imag.fr>

ENTRYPOINT ["bash"]
CMD ["init.sh"]

RUN pacman --noconfirm --needed -Sy gdb strace libdwarf make binutils gcc vim \
    && rm -rf /var/cache/pacman/pkg/ \
    && mkdir -p /var/cache/pacman/pkg/


RUN mkdir -p /home/gdb.py
WORKDIR /home/gdb.py

COPY home /home/gdb.py
COPY Dockerfile /home/gdb.py

RUN date > /home/gdb.py/.version
VOLUME /home/gdb.py
