PREBUMP=
  git fetch --tags origin master
  git pull origin master

PREVERSION=
  changelog finalize --version !newversion!
  git commit change.log -m "changelog: !newversion!"
  emd gen -in README.e.md > README.md
  git commit README.md -m "README: !newversion!"
  changelog md -o CHANGELOG.md --vars='{"name":"dummy"}'
  git commit CHANGELOG.md -m "changelog.md: !newversion!"

POSTVERSION=
  git push
  git push --tags