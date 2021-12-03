import pytest

from mkkey.completion import InstallCompletionError, _get_path

# def test_install():
#     shell, path = install()
#     assert shell in ["bash", "zsh", "fish"]
#     assert isinstance(path, str)


@pytest.mark.parametrize(
    "shell, path",
    [
        ("bash", "~/.mkkey-complete.bash"),
        ("zsh", "~/.mkkey-complete.zsh"),
        ("fish", "~/.config/fish/completions/mkkey.fish"),
    ],
)
def test__get_path(shell, path):
    res = _get_path(shell)
    assert res == path


@pytest.mark.parametrize(
    "shell, msg",
    [
        ("xxsh", "Unsupported shell: xxsh."),
    ],
)
def test__get_path_with_invalid_arg(shell, msg):
    with pytest.raises(InstallCompletionError) as err:
        _get_path(shell)
        pytest.fail("_get_path() must fail.")
    assert msg in str(err.value)
