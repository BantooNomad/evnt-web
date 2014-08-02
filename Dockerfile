# Pull base image
FROM dockerfile/ubuntu

# Install RethinkDB
RUN \
  add-apt-repository -y ppa:rethinkdb/ppa && \
  apt-get update && \
  apt-get install -y rethinkdb

# Define mountable directories
VOLUME ["/data"]

# Define working directory
WORKDIR /data

# Define default command
CMD ["rethinkdb", "--bind", "all"]

# Expose ports.
#   - 8080: web UI
#   - 28015: process
#   - 29015: cluster
EXPOSE 8080
EXPOSE 28015
EXPOSE 29015

FROM debian:jessie

ADD add-apt-repository /usr/sbin/add-apt-repository
RUN add-apt-repository ppa:rethinkdb/ppa && apt-get update && \
    apt-get install -y rethinkdb

# process cluster webui
EXPOSE 28015 29015 8080

VOLUME ["/rethinkdb"]
WORKDIR /rethinkdb
ENTRYPOINT ["/usr/bin/rethinkdb"]
CMD ["--help"]
