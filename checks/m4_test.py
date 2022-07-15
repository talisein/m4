import sys
import subprocess

def main() -> int:
    """Echo the input arguments to standard output"""
    m4 = sys.argv[1]
    inputfile = sys.argv[2]
    with open(inputfile, 'rb') as f:
        lines = f.read().splitlines(keepends=True)
        expected_out = []
        expected_err = []
        data = bytes()
        for l in lines:
            if l.startswith(b'dnl @ expected status: '):
                expected_code = int(l[len('dnl @ expected status: '):].rstrip())
            if l.startswith(b'dnl @ extra options: '):
                args = l[len('dnl @ extra options: '):].rstrip().decode()
            if l.startswith(b'dnl @result{}'):
                expected_out.append(l[len('dnl @result{}'):])
            if l.startswith(b'dnl @ expected error: '):
                expected_err.append(l[len('dnl @ expected error: '):])
            if not l.startswith(b'dnl @'):
                data += l
        runargs = []
        runargs.append(m4)
        runargs.append('-d')
        for arg in args.split(' '):
            if len(arg) > 0:
                runargs.append(arg)
        runargs.append('-')
        byte_expected = b''.join(expected_out)
        byte_expected_err = b''.join(expected_err)
        print('Arguments are: {0}'.format(' '.join(runargs)))
        res = subprocess.run(runargs, input=data, capture_output=True)
        if res.returncode == 77:
            return 77
        if res.returncode != expected_code:
            print('Unexpected return code: {0}, expected {1}'.format(res.returncode, expected_code))
            print('Here is the output. Expected:\n{0}\nGot:\n{1}'.format(byte_expected, res.stdout))
            if len(res.stderr) > 0:
                print('Stderr:\n{0}'.format(res.stderr))
            return 1
        if byte_expected.splitlines() != res.stdout.splitlines():
            print('Unexpected output. Expected:\n{0}\nGot:\n{1}'.format(byte_expected, res.stdout))
            if len(res.stderr) > 0:
                print('stderr:\n{0}'.format(res.stderr))
            return 1
        if len(byte_expected_err) > 0 and byte_expected_err != b'ignore\n' and byte_expected_err != res.stderr.replace(b'\r\n', b'\n'):
            print('unexpected error. Expected:\n{0}\nGot:\n{1}'.format(byte_expected_err, res.stderr.replace(b'\r\n', b'\n')))
            return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit
