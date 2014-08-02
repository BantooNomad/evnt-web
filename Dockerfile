#
# RethinkDB Dockerfile
#
# https://github.com/dockerfile/rethinkdb
#

# Pull base image.
FROM dockerfile/ubuntu

# Install RethinkDB.
RUN \
  add-apt-repository -y ppa:rethinkdb/ppa && \
  apt-get update && \
  apt-get install -y rethinkdb

# Define mountable directories.
VOLUME ["/data"]

# Define working directory.
WORKDIR /data

# Define default command.
CMD ["rethinkdb", "--bind", "all"]

# Expose ports.
#   - 8080: web UI
#   - 28015: process
#   - 29015: cluster
EXPOSE 8080
EXPOSE 28015
EXPOSE 29015




# http://www.rethinkdb.com/
# version 1.12.4
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





docker run -d -p 8080:8080 -p 28015:28015 -p 29015:29015 dockerfile/rethinkdb

docker run -d -p 8080:8080 -p 28015:28015 -p 29015:29015 -v <data-dir>:/data dockerfile/rethinkdb rethinkdb --bind=all --canonical-address `curl -s ipecho.net/plain` --machine-name `hostname | sed 's/-/_/g'`


docker run -d -p 8080:8080 -p 28015:28015 -p 29015:29015 -v <data-dir>:/data dockerfile/rethinkdb rethinkdb --bind all --canonical-address `curl -s ipecho.net/plain` --machine-name `hostname | sed 's/-/_/g'` --join <first-host-ip>:29015
