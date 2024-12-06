project(
    'kvh',
    'cpp',
    version: configure_file(input: 'kvh/version.txt', output: '-', copy: true),
    default_options: [
        'cpp_std=c++11',
    ],
)
py = import('python').find_installation(pure: false)
pybind11_dep = dependency('pybind11')

py.extension_module('ckvh',
    ['kvh/ckvh.cpp', 'kvh/ckvh.h'],
    install: true,
    dependencies : [pybind11_dep],
    subdir: 'kvh'
)

py.install_sources(
    ['kvh/__init__.py', 'kvh/kvh.py', 'kvh/version.txt', './salut.kvh', 'LICENSE'],
    pure: false,
    subdir: 'kvh',
)
