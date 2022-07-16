import sys
import subprocess
import os
import tempfile

# We want to print line endings normally, but each line should be a b'' string
def clean(x):
    lines = []
    for l in x.splitlines():
        lines.append(str(l))
    return '\n'.join(lines)

def check_error(run_result, expected_code, expected_out, expected_err, ignore_err, m4_input) -> int:
    res = 0
    lout = clean(run_result.stdout)
    lerr = clean(run_result.stderr)
    rout = clean(expected_out)
    rerr = clean(expected_err)
    if run_result.returncode != expected_code:
        print('Unexpected return code: {0}'.format(run_result.returncode))
        print('Expected return code: {0}'.format(expected_code))
        res = 1
    if lout != rout:
        print('Unexpected stdout:\n{0}'.format(lout))
        print('Expected stdout:\n{0}'.format(rout))
        res = 1
    if not ignore_err and lerr != rerr:
        print('Unexpected stderr:\n{0}'.format(lerr))
        print('Expected stderr:\n{0}'.format(rerr))
        res = 1
    print('The input was:\n{0}'.format(clean(m4_input)))
    return res

def main() -> int:
    m4 = sys.argv[1]
    input_path = sys.argv[2]
    tmproot = sys.argv[3]
    workdir = sys.argv[4]
    with open(input_path, 'rb') as input_file, tempfile.TemporaryDirectory(dir=tmproot) as tmpdir:
        m4_env = {'TMPDIR': tmpdir,
                  'M4PATH': 'examples'}
        expected_out = bytes()
        expected_err = bytes()
        ignore_err = False
        m4_input = bytes()
        for l in input_file.read().splitlines():
            if l.startswith(b'dnl @ expected status: '):
                expected_code = int(l[len('dnl @ expected status: '):].rstrip())
            if l.startswith(b'dnl @ extra options: '):
                args = l[len('dnl @ extra options: '):].rstrip().decode()
            if l.startswith(b'dnl @result{}'):
                expected_out += l[len('dnl @result{}'):]
            if l.startswith(b'dnl @error{}'):
                expected_err += l[len('dnl @error{}'):]
            if l.startswith(b'dnl @ expected error: ignore'):
                ignore_err = True
            if not l.startswith(b'dnl @'):
                m4_input += l + os.linesep.encode()
        runargs = []
        runargs.append('m4')
        runargs.append('-d')
        for arg in args.split(' '):
            if len(arg) > 0:
                runargs.append(arg)
        runargs.append('-')
        print('Arguments are: {0}'.format(' '.join(runargs)))
        res = subprocess.run(runargs,
                             input=m4_input,
                             capture_output=True,
                             cwd=workdir,
                             env=m4_env,
                             executable=m4)
        if res.returncode == 77:
            return 77
        return check_error(res, expected_code, expected_out, expected_err, ignore_err, m4_input)

if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit
