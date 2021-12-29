# A Golang Demo: Package Name and `go.mod`

This demo shows you that:

in the recent Go, the package name conventions are surprisingly liberal.

## [moddemo.py](moddemo.py)

This all-in-one Python program does:
1. create 0/00.go, 1/11.go, 2/22_test.go, and [012]/go.mod
1. `git add -f [12]/go.mod`
1. `git commit ...` 
1. `go mod tidy` for each dir in [12]
1. run 1/11.go that prints a datum exported from 00.go
1. run 2/22_test.go that discards a datum exported from 00.go

## Running from command lines

1. create [012]/*, run [12]
   ```shell
   git reset --hard aa.seed
   ./moddemo.py
   ```
1. see the differences after [moddemo.py](moddemo.py) ran
   ```shell
   git diff aa.seed
   git diff ab.go-mod/edit
   git diff ac.go-mod/tidy
   ```

## Running from GUI

.vscode/*.json are ready for you.
