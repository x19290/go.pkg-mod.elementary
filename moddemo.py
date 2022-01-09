#!/usr/bin/env python3

_PKGS = r'01'

_00IMPL = r'''
package anyid

const private = "*** private ***"
const Public = "*** hello ***"
'''[1:]

_12DEMO = '''
package main

import (
\t"fmt"
\tz "0"
)

func main() {
\tfmt.Println(z.Public)
}
'''[1:]

_01TEST = '''
package anyid

import (
\t"testing"
)

func Test0(*testing.T) {
\t_, _ = private, Public
}
'''[1:]

_ODDMOD = r'999---'  # /\w[\w-]*/. used as mod names in */go.mod. safe?


def main():
    from os.path import relpath  # wiser than Path.relative_to
    from pathlib import Path

    base = Path(__file__).resolve().parent
    base = Path(relpath(base, Path.cwd()))
    pkgs = tuple(base / y for y in _PKGS)

    def report(todo):
        from sys import stderr
        print(r'+ %s' % todo, file=stderr)
    def nuke(pkg):
        # a long time ago, there was a command with that name
        # in Linux-initrd
        from shutil import rmtree
        report(r'nuke %s' % pkg)
        try:
            pkg.mkdir()
        except FileExistsError:
            pass
        for y in pkg.iterdir():
            try:
                y.unlink()
            except:
                rmtree(y)
    def call(command, distance=None):
        from subprocess import call
        shell = isinstance(command, str)
        cwd = base / distance if distance else base
        report(r'%(cwd)s$ %(command)s' % locals())
        return call(command, shell=shell, cwd=cwd)
    def check_call(command, distance=None):
        status = call(command, distance)
        if status != 0:
            raise SystemExit(status)

    for pkg in pkgs:
        nuke(pkg)

    pkg0, pkg1 = pkgs

    (pkg0 / r'00.go').write_text(_00IMPL)
    (pkg0 / r'01_test.go').write_text(_01TEST)
    (pkg1 / r'12.go').write_text(_12DEMO)

    for pkg in pkgs:
        check_call(r'go mod init %s' % _ODDMOD, pkg)
        check_call(r'go mod edit -replace 0=../0', pkg)
        check_call(r'git add -f go.mod', pkg)
    call(r'git,commit,-a,-m,chore: add -f */go.mod'.split(r','))

    for pkg in pkgs:
        check_call(r'go mod tidy', pkg)

    check_call(r'go test ./...', r'0')
    check_call(r'go run .', r'1')
    check_call(r'git diff')


if __name__ == r'__main__':
    main()
