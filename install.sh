ALBERT_PY_MODULES="$HOME/.local/share/albert/org.albert.extension.python/modules"

if command -v git >/dev/null 2>&1; then
  git clone https://github.com/GabrielCzar/albert-jira-extension.git "$ALBERT_PY_MODULES/albert-jira-extension"
elif command -v unzip >/dev/null 2>&1; then
  wget -O albert-jira-extension.zip https://github.com/gabrielczar/albert-jira-extension/archive/master.zip
  unzip albert-jira-extension.zip
  mv albert-jira-extension-master "$ALBERT_PY_MODULES"
else
  echo "unable to install. Please download and copy project to: $ALBERT_PY_MODULES/"
fi
