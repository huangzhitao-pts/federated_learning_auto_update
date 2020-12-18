# -*- coding: utf-8 -*-
import os


class Config(object):
    # yaml文件path
    YAML_PATH = "/mnt/docker-compose.yaml"
    # 镜像的名称前缀
    IMAGE_PREFIX = os.getenv("IMAGE_PREFIX")
    # 宿主机ip
    LOCAL_HOST = os.getenv("LOCAL_HOST")
    # 宿主机运行路径
    LOCAL_RUN_PWD = os.getenv("LOCAL_RUN_PWD")