from glob import escape
from msilib.schema import Error
from fabric import Connection
import tarfile
import yaml
import re
import os
import sys


def exclude_function(filename):
    """
    excludes files
    :param filename:
    :return bool:
    """
    exclude_list = config['exclude']
    for item in exclude_list:
        # print(filename.name)
        if re.search(item, filename.name) is not None:
            return None
    return filename


# load config
with open('config.yaml', 'r') as f:
    config_data = f.read()
    config = yaml.load(config_data, Loader=yaml.Loader)

with Connection(host=config['host'], user=config['username'], connect_kwargs={'look_for_keys': False, 'password': config['password']}) as c:

    try:
        os.remove('export.tgz')
    except FileNotFoundError:
        print("File does not exist")
    except Exception as e:
        print("Bigger issues abound")
        sys.exit(1)

    # create local file
    with tarfile.open('export.tgz', 'w:gz') as tar:
        for f in os.listdir(config['local_location']):
            # print(f)
            tar.add(f, filter=exclude_function)
    # send local file to server
    c.put("export.tgz")
    # clean up previous folder if it exists
    path_info = os.path.split(config['local_location'])
    print(path_info[1])
    if c.run("rm -r {0}/".format(path_info[1]), warn=True).failed:
        print("Unable to find required directory")
    if c.run("mkdir -p {0}".format(path_info[1]), warn=True).failed:
        print("Create required directory")

    # extract file
    c.run('tar -xzvf export.tgz -C {0}'.format(path_info[1]))
    # move and change ownership
    move_command = "cp -R -T {0} {1}".format(
        path_info[1], config['dest_location'])
    if c.sudo(move_command, password=config['password'], warn=True).failed:
        c.sudo(
            'mkdir -p {0}'.format(config['dest_location']), password=config['password'])
        c.sudo(move_command, password=config['password'])
    c.sudo('chown -R {0}:{1} {2}'.format(config['srv_user'], config['srv_user'],
           config['dest_location']), password=config['password'])

# Restart Services
# sudo service milan_2022 status

# sudo service milan_2022 stop
# sudo service milan_2022 start
####### OR #########
# sudo service milan_2022 restart
