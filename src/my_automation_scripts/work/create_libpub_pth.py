# -*- coding: utf-8 -*-
"""
生成公共库 pth 文件
"""
import logging
import os
import site

import click

IGNORE_DIRECTORIES = ['xue', 'xfe']

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',
    datefmt='%Y-%m-%d %A %H:%M:%S'
)


def get_python_site_packages_path() -> str:
    """获取当前 python 的 site-packages 路径

    :return str: 文件夹路径
    """
    path_list = site.getsitepackages()
    for path in path_list:
        if 'site-packages' in path:
            return path
    return ''


def combination_path(prefix_path: str, suffix_path: str) -> str:
    """组合路径

    :param str prefix_path: 路径前缀
    :param str suffix_path: 路径后缀
    :return str: 组合后的路径
    """
    if not prefix_path.endswith('/'):
        prefix_path += '/'
    if suffix_path.startswith('/'):
        suffix_path = suffix_path[1:]

    return prefix_path + suffix_path


def get_libpub_paths(prefix_path: str) -> list:
    """获取公共文件库路径列表

    :param str prefix_path: 文件库前缀路径
    :return list: 公共文件库列表
    """
    paths = list()
    if prefix_path.startswith('~'):
        prefix_path = os.path.expanduser(prefix_path)

    if os.path.exists(prefix_path):
        for f_name in os.listdir(prefix_path):
            f_path = combination_path(prefix_path, f_name)
            if (
                f_name.startswith('x')
                and os.path.isdir(f_path)
                and f_name not in IGNORE_DIRECTORIES
            ):
                paths.append(f_path)
    return paths


def create_pth(paths: list, site_packages_path: str):
    """生成 pth 路径

    :param list paths: 路径列表
    :param str site_packages_path: site-packages 路径
    """
    for path in paths:
        libpub_name = path.split('/')[-1] + '.pth'
        pth_path = combination_path(site_packages_path, libpub_name)
        if not os.path.exists(pth_path):
            with open(pth_path, 'w+') as f:
                f.write(path + os.linesep)
            logging.info(f'创建 {libpub_name}')
    logging.info('生成 pth 文件完成')


@click.command()
@click.option('--prefix_path', default='/web/www/', help='公共库路径', type=str)
def main(prefix_path: str):
    paths = get_libpub_paths(prefix_path)
    if not paths:
        logging.warning('没有找到公共库文件')
        return

    site_packages_path = get_python_site_packages_path()
    if not site_packages_path:
        logging.warning('没有找到当前 python 版本的 site-packages 路径')
        return

    create_pth(paths, site_packages_path)


if __name__ == '__main__':
    main()
