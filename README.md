# A Golang Demo: Package Name and `go.mod`

This demo shows you that:
in the recent Go, the package name conventions are surprisingly liberal.

## [moddemo.py](moddemo.py)

This all-in-one Python program does:
1. create 0/00.go, 0/01_test.go, 1/12.go, and */go.mod
1. `git add -f */go.mod`
1. `git commit ...` 
1. `go mod tidy` for each dir in [01]
1. run 0/01_test.go that discards data from 00.go
1. run 1/12.go that prints a datum exported from 00.go

## Demo through command lines

1. to create [01]/*, to run [01]:
   ```shell
   git reset --hard n0.seed
   ./moddemo.py
   ```
1. to see the changes after [moddemo.py](moddemo.py) ran:
   ```shell
   git diff n0.seed n1.go-mod/edit
   git diff n1.go-mod/edit
   git diff
   git diff n2.go-mod/tidy
   ```

## Demo through GUI

.vscode/*.json are ready for you.
