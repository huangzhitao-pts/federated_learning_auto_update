from flask import Blueprint
from flask import current_app as app

import os
import docker
import yaml
import paramiko


NEW_IMAGE_TAG = set()


auto_update = Blueprint("auto_update", __name__)


@auto_update.route("/version/up")
def version_up():
    client = docker.from_env()

    # 是否有更新
    FLAG = False

    # 获取yaml文件内容
    yaml_path = app.config.get("YAML_PATH")
    local_run_path = app.config.get("LOCAL_RUN_PWD")
    with open(yaml_path, encoding='utf-8') as f:
        yaml_dict = yaml.safe_load(f)

    # 将version号替换stable -> beta
    for _, svc in yaml_dict["services"].items():
        # 当前运行镜像的short_id
        print(svc["image"])
        current_image_id = client.images.get(svc["image"]).short_id
        print(current_image_id)

        svc["image"] = svc["image"].replace("stable", "beta")
        # 更新镜像
        print(f"Pull image {svc['image']}")
        new_image = client.images.pull(svc["image"])
        print(new_image.short_id)
        # 有需要更新的镜像
        if current_image_id != new_image.short_id and not FLAG:
            FLAG = True
    print(FLAG)
    if FLAG:
        # 将改变写入yaml文件
        with open(yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(yaml_dict, f, default_flow_style=False)

        # 重启docker-compose
        # ssh创建连接
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=app.config.get("LOCAL_HOST"), port=22, username='root')
        print(f'docker-compose --project-directory {local_run_path} -f {os.path.join(local_run_path, yaml_path[1:])} up -d')
        stdin, stdout, stderr = ssh.exec_command(
            f'docker-compose --project-directory {local_run_path} -f {os.path.join(local_run_path, yaml_path[1:])} up -d')
        # print(stdin.read().decode())
        print(stdout.read().decode())
        # print(stderr.read().decode())
        ssh.close()

    return "ok"