import subprocess
from typing import Tuple

import shellingham


class InstallCompletionError(Exception):
    def __init__(self, shell, msg):
        self.shell = shell
        super().__init__(msg)


def install() -> Tuple[str, str]:
    path: str = ""
    shell: str = shellingham.detect_shell()[0]
    if shell == "bash":
        path = "~/.mkkey-complete.bash"
    elif shell == "zsh":
        path = "~/.mkkey-complete.zsh"
    elif shell == "fish":
        path = "~/.config/fish/completions/mkkey.fish"
    else:
        raise InstallCompletionError(shell, f"Unsupported shell: {shell}.")
    subprocess.call(f"_MKKEY_COMPLETE={shell}_source mkkey > {path}", shell=True)
    return shell, path
