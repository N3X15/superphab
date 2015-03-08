import os, sys, yaml, json
script_dir = os.path.dirname(os.path.realpath(__file__))

config = {}
with open('supervisor_config.yml', 'r') as f:
    config = yaml.load(f)

DESTFILE = os.path.abspath(config['paths']['outfile'])
BASEPATH = os.path.abspath(config['paths']['phabricator'])
PID_DIR = os.path.abspath(config['paths']['piddir'])

if not os.path.isdir(BASEPATH):
    print('ERROR: {} does not exist.'.format(BASEPATH))

DAEMON_CONFIGS = os.path.join(script_dir, 'daemon_configs')
DAEMONS = []
DAEMON_IDS = []

daemon_default = {
     'count':1,
}

def buildDaemonConfig(where, dclass, args):
    global PID_DIR
    config = {
        'piddir':PID_DIR,
        'daemons': [
            {
                'class':dclass,
                'argv':args,
            }
        ]
    }
    with open(where, 'w') as f:
        json.dump(config, f)
        print('Wrote {} config to {}.'.format(dclass, where))
        

if not os.path.isdir(DAEMON_CONFIGS):
    os.makedirs(DAEMON_CONFIGS)
    
for daemon_name, cfg in config['daemons'].items():
    if cfg is None:
        cfg = daemon_default
    count = cfg.get('count', 1)
    cfg_args = cfg.get('args', [])
    cfg_user = cfg.get('user', '')
    for i in range(1, count + 1):
        id = daemon_name + str(i) if count > 1 else daemon_name
        cfgfile = os.path.join(DAEMON_CONFIGS, id + '.json')
        DAEMONS.append({'id':id, 'daemon':daemon_name, 'args':cfg_args, 'user':cfg_user, 'cfgfile':cfgfile})
        DAEMON_IDS.append(id)
        buildDaemonConfig(cfgfile, daemon_name, cfg_args)

with open(DESTFILE, 'w') as f:
    f.write('; Autogenerated with buildSupervisor.py.\n')
    f.write('[group:phabricator]\n')
    f.write('programs={}\n\n'.format(','.join(DAEMON_IDS)))

    for daemoncfg in DAEMONS:
        daemoncfg['basepath'] = BASEPATH
        with open(os.path.join(script_dir, 'supervisor.tmpl.conf'), 'r') as tmpl:
            for line in tmpl:
                line = line.strip().format(**daemoncfg)
                f.write(line + '\n')
            f.write('\n')
    print('Wrote {}.'.format(DESTFILE))