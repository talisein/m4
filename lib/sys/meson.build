# SYS/WAIT.H
sys_files = []
if not cdata.has('HAVE_SYS_WAIT_H') or not cdata.has('HAVE_SYS_TYPES_H')
sys_files += configure_file(input : cppdefs_src,
                            output : 'c++defs.h',
                            copy: true)
sys_files += configure_file(input : warnonuse_src,
                            output : 'warn-on-use.h',
                            copy: true)
endif
if not cdata.has('HAVE_SYS_WAIT_H') or generated_header_data.get('GNULIB_WAITPID') == 1
sys_files += configure_file(input : sys_wait_src,
                            output : 'wait.h',
                            configuration: generated_header_data)
endif
if not cdata.has('HAVE_SYS_TYPES_H') or host_machine.system() == 'windows'
sys_files += configure_file(input : sys_types_src,
                            output : 'types.h',
                            configuration: generated_header_data)
endif
