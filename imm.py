import os
from fabric.api import abort, cd, env, get, hide, hosts, local, prompt, \
    put, require, roles, run, runs_once, settings, show, sudo, warn, puts

from fabric.colors import green, blue, cyan, magenta, red, white, yellow

__author__ = 'pahaz'


def local_env():
    env.user = 'vagrant'
    env.password = 'vagrant'
    env.host_string = 'localhost:22'


def supercomputer_env():
    env.user = 'WRITE YOU USERNAME'
    env.password = 'WRITE YOU PASSWORD'
    env.host_string = 'umt.imm.uran.ru:22'


def _put(name):
    put(name, '~/' + name, use_sudo=False)


def _get(name):
    get('~/' + name, name)


def _mpi(name):
    """MPI with OpenMP compile

    Example:

       _mpi('mpi.c')

    """
    if os.path.extsep not in name:
        raise Exception('filename does not contain extsep')
    base_name, name_ext = name.rsplit(os.path.extsep, 1)

    _put(name)
    run('mpicc {name} -openmp -o {base_name} && ./{base_name}'
        .format(**locals()))

    run('mqrun -np 2 -stdout out.txt -stderr err.txt ./{base_name}')
    run('tail ./err.txt')
    run('tail ./out.txt')
    _get('out.txt')
    _get('err.txt')


def _cuda(name):
    """Cuda compile

    Example:

        _cuda('cuda.cu')

    """
    if os.path.extsep not in name:
        raise Exception('filename does not contain extsep')
    base_name, name_ext = name.rsplit(os.path.extsep, 1)

    _put(name)
    # run('nvcc {name} -o {base_name} && ./{base_name}'.format(**locals())
    run('nvcc {name} -o {base_name} && srun --gres=gpu:2 ./{base_name}'
        .format(**locals()))


def main():
    _put('kmeans.cpp')
    _put('data-gen.cpp')
    run('g++ data-gen.cpp -o data-gen && ./data-gen 3 10 10 data-gen.txt')
    _get('data-gen.txt')
    run('g++ kmeans.cpp -o kmeans -fopenmp && ./kmeans 10 data-gen.txt kmeans.txt')
    _get('kmeans.txt')


if __name__ == "__main__":
    local_env()
    # supercomputer_env()
    main()
