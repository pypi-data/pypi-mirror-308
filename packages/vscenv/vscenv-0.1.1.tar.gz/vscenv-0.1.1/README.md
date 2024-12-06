# vscenv - Management of isolated VSCODE environments

vscenv is a command-line tool that makes it easy to maintain and manage isolated vscode environments written in Python.

![](./resources/img.png)

---

## Installation
- Option 1 : Install from pypi
    ```
    pip install vscenv --user
    ```
- Option 2 : Install from soruce
    ```
    git clone https://github.com/jugangdae/vscenv
    cd vscenv
    pyhton -m build
    pip install vscenv-0.0.1-py3-none-any.whl
    ```
---
## Commands

1. `create` : Create a new vscenv environment.
    ```
    vscenv create [vscenv_env]
    vscenv c [vscenv_env]
    ```
2. `list` : Show vscenv env list
    ```
    vscenv list
    vscenv l
    ```
3. `run` : Executes VSCODE using an vscenv environment
    ```
    vscenv run [vscenv_env] [work_path]
    vscenv r [vscenv_env] [work_path]
    ```
4. `Delete` : Delete an vscenv environment.
    ```
    vscenv delete [vscenv_env]
    vscenv d [vscenv_env]
    ```
5. `help` and `version`
    ```
    vscenv -h, --help
    vscenv -v, --version
    ```
---
## Config (~/.vscenvconfig)
```
[setting]
vscenv_run = [code or code-insider]
vscenv_dir = [path of vscenv environments directory]
```
