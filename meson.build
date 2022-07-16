project('m4', 'c',
  version: '1.4.19',
  license: 'GPLv3+',
  default_options: [
    'c_std=gnu11',
  ],
  meson_version: '>= 0.59.0', # required for executable(..., win_subsystem: ...)
)

subdir('lib')
subdir('src')
if get_option('enable_tests')
  subdir('checks')
endif
