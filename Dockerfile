FROM finalduty/archlinux:monthly

MAINTAINER Kevin Pouget <kpouget@imag.fr>

ENTRYPOINT ["bash"]
CMD ["init.sh"]

RUN pacman --noconfirm --needed -Sy gdb strace libdwarf make binutils gcc vim sudo \
    && rm -rf /var/cache/pacman/pkg/ \
    && mkdir -p /var/cache/pacman/pkg/

RUN echo "## Allow all users to run any commands anywhere" >> /etc/sudoers
RUN echo "ALL ALL=(ALL) 	ALL" >> /etc/sudoers
RUN echo "auth    sufficient    pam_permit.so" > /etc/pam.d/su

RUN mkdir -p /home/gdb
WORKDIR /home/gdb

COPY home /home/gdb

RUN date > /home/gdb/.version
COPY Dockerfile /home/gdb

VOLUME /home/gdb
