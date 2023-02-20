# -*- coding: utf-8 -*-
"""
我的 Python 在哪里？
"""
import subprocess
import sys

import click


@click.command()
@click.option('--py_pth', default='', help='python 路径', type=str)
def main(py_pth: str):
    if not py_pth:
        py_pth = sys.executable

    site_packages_pth = None
    code, out_text = subprocess.getstatusoutput(
        f'{py_pth} -c "import site; print(site.getsitepackages()[0])"')
    if code == 0:
        site_packages_pth = out_text

    pip_pth = None
    if py_pth.endswith('python') or py_pth.endswith('python3'):
        bin_pth = py_pth.replace(py_pth.split('/')[-1], '')
        code, out_text = subprocess.getstatusoutput(f'ls {bin_pth}|grep pip')
        if code == 0 and 'pip' in out_text:
            pip_pth = bin_pth + 'pip'

    print(f'\033[32mpython       \033[0m: {py_pth}')
    if site_packages_pth:
        print(f'\033[32msite-packages\033[0m: {site_packages_pth}')
    if pip_pth:
        print(f'\033[32mpip          \033[0m: {pip_pth}')


if __name__ == '__main__':
    main()
