# SuperPhab

This is a simple set of scripts to generate and update supervisord configuration for Phabricator daemons.

# Installation

Assuming that you have Phabricator installed in /opt/phacility/phabricator:

```bash
# Clone the repo
cd /opt/phacility && git clone https://github.com/N3X15/superphab`
# Copy the phd-daemon wrapper to the Phabricator installation
cp superphab/phd-daemon-launcher phabricator/
# Change directory to superphab's install directory
cd superphab/
# Copy over the default configuration.
cp supervisor_config.yml.dist supervisor_config.yml
```

Finally, edit supervisor_config.yml.

# Running

Simply make sure that supervisor_config.yml is up to date, and then run `./updateSupervisor.sh`.  It will automatically stop all Phabricator processes, update the supervisor configs, reload them, and restart the phabricator process group.

# Updating

`git pull && ./updateSupervisor.sh`
