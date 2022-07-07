project('m4', 'c',
  version: '1.4.19',
  license: 'GPLv3+',
  default_options: [
    'c_std=gnu11',
    'warning_level=1',
    'buildtype=debugoptimized'
  ],
  meson_version: '>= 0.59.0', # required for executable(..., win_subsystem: ...)
)

add_project_arguments('-D_GNU_SOURCE', language: 'c')

subdir('lib')
subdir('src')
