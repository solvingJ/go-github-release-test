#!/bin/sh -e
curl https://dl.bintray.com/solvingj/public-rpm/SolvingJ-Public-RPM.repo -o /etc/yum.repos.d/SolvingJ-Public-RPM.repo
cd /mnt/travis_build_dir
go-bin-rpm generate --file rpm-creation-data.json --version 0.0.1