# SYS/WAIT.H
if not cdata.has('HAVE_SYS_WAIT_H')
configure_file(input : cppdefs_src,
               output : 'c++defs.h',
               copy: true)
configure_file(input : warnonuse_src,
               output : 'warn-on-use.h',
               copy: true)
configure_file(input : sys_wait_src,
               output : 'wait.h',
               configuration: generated_header_data)
endif
