import argparse
import requests
import json
import os
parser = argparse.ArgumentParser(add_help=False,usage='%(prog)s COMMAND')
parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                    help='show help message')
parser.add_argument("COMMAND", help="[list|create|update]")

def get_image_infos():
    r = requests.get('https://registry.hub.docker.com/v2/repositories/p208p2002/docker-for-ai-dev/tags')
    return json.loads(r.text),r.status_code

def list_image_tags():
    images_tags = []
    images,_ = get_image_infos()
    images = images.get('results',[])
    for image in images:
        last_updater_username = image['last_updater_username']
        image_name = image['name']
        # print("%s/%s"%(last_updater_username,image_name))
        images_tags.append("%s/docker-for-ai-dev:%s"%(last_updater_username,image_name))
    return images_tags

def create_container():
    user_options = {}
    #
    image_tags = list_image_tags()
    for i,image_tag in enumerate(image_tags):
        print("[%d] %s"%(i+1,image_tag))
    select_image_id = int(input("Select base image:"))
    select_image_tag = image_tags[select_image_id-1]
    user_options['select_image_tag'] = select_image_tag
    
    #
    use_gpu = input("Enable GPUs? y/n:")
    if(use_gpu == 'y'):
        use_gpu = True
    else:
        use_gpu = False
    user_options['use_gpu'] = use_gpu
    if(use_gpu):
        gpu_ids = input("Assign GPUs for container (by GPU id) e.g. 0 or 0,1 or all:")
        assert gpu_ids != ''
        user_options['gpu_ids'] = gpu_ids

    # user account
    user_options['username'] = input('username:')
    user_options['password'] = input('password:')

    # service
    ssh_port = input("ssh port:")
    user_options['ssh_porting'] = '-p %s:22'%ssh_port
    jupyter_port = input("jupyter port:")
    user_options['jupyter_porting'] = '-p %s:8888'%jupyter_port
    vscode_port = input("vscode port:")
    user_options['vscode_porting'] = '-p %s:8080'%vscode_port

    # create volume
    create_volume = input('create volume? (mount at /user_data) y/n:')
    if(create_volume == 'y'):
        create_volume = True
        print('volume name will same as your username, and mount at /user_data')
    else:
        create_volume = False
    user_options['create_volume'] = create_volume

    # auto restart
    auto_restart = input('container auto restart? y/n:')
    if(auto_restart == 'y'):
        auto_restart = True
    else:
        auto_restart = False
    user_options['auto_restart'] = auto_restart 

    # docker run options
    docker_run_options = input('any other options for images? e.g "-p 1234:1234 -p 1235:1235":')
    user_options['docker_run_options'] = docker_run_options
    print(user_options)

    # create docker run cmd
    _docker_run_options = ''
    if(user_options['use_gpu'] == True):
        _docker_run_options+='--gpus %s '%user_options['gpu_ids']
    if(user_options['create_volume'] == True):
        _docker_run_options+='-v %s:/user_data '%user_options['username']
    if(user_options['auto_restart'] == True):
        _docker_run_options+='--restart=always '
    #
    _docker_run_options += '--name=%s '%(user_options['username'])
    _docker_run_options += '-e"NAME"=%s '%(user_options['username'])
    _docker_run_options += '-e"PASSWORD"=%s '%(user_options['password'])

    docker_run_cmd = "docker run -itd %s %s %s %s %s %s"%(\
        _docker_run_options,\
        user_options['docker_run_options'],\
        user_options['ssh_porting'],\
        user_options['jupyter_porting'],\
        user_options['vscode_porting'],\
        user_options['select_image_tag']
    )

    print(docker_run_cmd)
    os.system(docker_run_cmd)

def update_images():
    image_tags = list_image_tags()
    for i,image_tag in enumerate(image_tags):
        print("[%d] %s"%(i+1,image_tag))
    update_image_id =  int(input('which image to update?'))-1
    os.system('docker pull %s'%image_tags[update_image_id])

def main():
    args = parser.parse_args()
    if(args.COMMAND == 'list'):
        image_tags = list_image_tags()
        for tag in image_tags:
            print(tag)

    elif(args.COMMAND == 'create'):
        create_container()

    elif(args.COMMAND == 'update'):
        update_images()