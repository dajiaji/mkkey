import subprocess
from typing import Tuple

import shellingham


class InstallCompletionError(Exception):
    def __init__(self, shell, msg):
        self.shell = shell
        super().__init__(msg)


def _get_path(shell: str) -> str:
    if shell == "bash":
        return "~/.mkkey-complete.bash"
    if shell == "zsh":
        return "~/.mkkey-complete.zsh"
    if shell == "fish":
        return "~/.config/fish/completions/mkkey.fish"
    raise InstallCompletionError(shell, f"Unsupported shell: {shell}.")


def install() -> Tuple[str, str]:
    shell: str = shellingham.detect_shell()[0]
    path = _get_path(shell)
    subprocess.call(f"_MKKEY_COMPLETE={shell}_source mkkey > {path}", shell=True)
    return shell, path
