#!/bin/bash
supervisorctl stop phabricator:*
python ./buildSupervisor.py
supervisorctl reread
supervisorctl update
supervisorctl start phabricator:*
