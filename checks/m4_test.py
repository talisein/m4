import sys
import subprocess

def main() -> int:
    """Echo the input arguments to standard output"""
    m4 = sys.argv[1]
    inputfile = sys.argv[2]
    with open(inputfile) as f:
        lines = f.readlines()
        expected_out = []
        data = bytes()
        for l in lines:
            if l.startswith('dnl @ expected status: '):
                expected_code = l[23:].rstrip()
            if l.startswith('dnl @ extra options: '):
                args = l[22:].rstrip()
            if l.startswith('dnl @result{}'):
                expected_out.append(l[13:])
            if not l.startswith('dnl @'):
                data += l.encode()
        runargs = []
        runargs.append(m4)
        runargs.append('-d')
        for arg in args.split(' '):
            if len(arg) > 0:
                runargs.append(arg)
        runargs.append('-')
        res = subprocess.run(runargs, input=data, capture_output=True)
        if res.returncode == 77:
            return 77
        if str(res.returncode) != expected_code:
            print('Unexpected return code: {0}, expected {1}'.format(res.returncode, expected_code))
            print('Here is the output. Expected:\n{0}\nGot:\n{1}'.format(byte_expected, res.stdout.replace(b'\r\n', b'\n')))
            if len(res.stderr) > 0:
                printf('Stderr:\n{0}'.format(res.stderr))
            return 1
        byte_expected = ''.join(expected_out).encode('UTF-8')
        if byte_expected != res.stdout.replace(b'\r\n', b'\n'):
            print('unexpected output. Expected:\n{0}\nGot:\n{1}'.format(byte_expected, res.stdout.replace(b'\r\n', b'\n')))
            if len(res.stderr) > 0:
                printf('Stderr:\n{0}'.format(res.stderr))
            return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit
