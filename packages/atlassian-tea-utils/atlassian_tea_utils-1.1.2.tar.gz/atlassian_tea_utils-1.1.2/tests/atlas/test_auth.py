import subprocess
import sys
from unittest.mock import Mock

import pytest

from atlassian_tea_utils.atlas.auth import possibly_get_auth_from_atlas_cli


@pytest.fixture()
def mock_run(monkeypatch):
    fake_run = Mock()
    monkeypatch.setattr(
        subprocess,
        "run",
        fake_run,
    )
    return fake_run


@pytest.fixture()
def is_a_tty(monkeypatch):
    is_tty = Mock(return_value=True)
    monkeypatch.setattr(
        sys.stdout,
        "isatty",
        is_tty,
    )


@pytest.fixture()
def is_not_a_tty(monkeypatch):
    is_tty = Mock(return_value=False)

    monkeypatch.setattr(
        sys.stdout,
        "isatty",
        is_tty,
    )


@pytest.fixture()
def not_in_pipelines(monkeypatch) -> None:
    monkeypatch.delenv("PIPELINES_JWT_TOKEN", raising=False)


@pytest.fixture()
def not_using_local_ide(monkeypatch) -> None:
    monkeypatch.delenv("LOCAL_IDE_IN_USE", raising=False)


@pytest.fixture()
def using_local_ide(monkeypatch) -> None:
    monkeypatch.setenv("LOCAL_IDE_IN_USE", "some-value")


@pytest.mark.parametrize(
    "with_prefix, expected_value, expected_value_prefix",
    [
        (False, "example-value", ""),
        (True, "example-value", "SLAUTH "),
    ],
)
def test_auth_from_env(
    mock_run,
    not_in_pipelines,
    not_using_local_ide,
    monkeypatch,
    with_prefix,
    expected_value,
    expected_value_prefix,
) -> None:
    # Given
    local_env_var = "EXAMPLE_ENV_VAR"
    expected = "example-value"
    monkeypatch.setenv(local_env_var, expected)

    # When
    result = possibly_get_auth_from_atlas_cli(
        "eg",
        local_env_var=local_env_var,
        command=[],
        fallback_command="eg",
        with_prefix=with_prefix,
    )

    # Then
    mock_run.assert_not_called()
    assert result == f"{expected_value_prefix}{expected_value}"


@pytest.mark.parametrize(
    "with_prefix, expected_value, expected_value_prefix",
    [
        (False, "pipelines-value", ""),
        (True, "pipelines-value", "Bearer "),
    ],
)
def test_auth_from_pipelines(
    mock_run, monkeypatch, with_prefix, expected_value, expected_value_prefix
) -> None:
    # Given
    monkeypatch.setenv("PIPELINES_JWT_TOKEN", expected_value)

    # When
    result = possibly_get_auth_from_atlas_cli(
        "eg",
        local_env_var="<not-existing>",
        command=[],
        fallback_command="eg",
        with_prefix=with_prefix,
    )

    # Then
    mock_run.assert_not_called()
    assert result == f"{expected_value_prefix}{expected_value}"


@pytest.mark.parametrize(
    "with_prefix, expected_value, expected_value_prefix",
    [
        (False, "example-value", ""),
        (True, "example-value", "SLAUTH "),
    ],
)
def test_auth_from_command_local_ide_in_use(
    mock_run,
    not_in_pipelines,
    using_local_ide,
    is_not_a_tty,
    monkeypatch,
    with_prefix,
    expected_value,
    expected_value_prefix,
) -> None:
    # Given
    mock_process = Mock(name="mock process")
    mock_process.stdout.strip.return_value = expected_value
    mock_run.return_value = mock_process

    # When
    result = possibly_get_auth_from_atlas_cli(
        "eg",
        local_env_var="non-existing-value-11a",
        command=[],
        fallback_command="eg",
        with_prefix=with_prefix,
    )

    # Then
    mock_run.assert_called_once_with(
        [], encoding="utf-8", stdout=subprocess.PIPE, check=True
    )
    assert result == f"{expected_value_prefix}{expected_value}"


@pytest.mark.parametrize(
    "with_prefix, expected_value, expected_value_prefix",
    [
        (False, "example-value", ""),
        (True, "example-value", "SLAUTH "),
    ],
)
def test_auth_from_command_local_is_a_tty(
    mock_run,
    not_in_pipelines,
    not_using_local_ide,
    is_a_tty,
    monkeypatch,
    with_prefix,
    expected_value,
    expected_value_prefix,
) -> None:
    # Given
    mock_process = Mock(name="mock process")
    mock_process.stdout.strip.return_value = expected_value
    mock_run.return_value = mock_process

    # When
    result = possibly_get_auth_from_atlas_cli(
        "eg",
        local_env_var="non-existing-value-11a",
        command=[],
        fallback_command="eg",
        with_prefix=with_prefix,
    )

    # Then
    mock_run.assert_called_once_with(
        [], encoding="utf-8", stdout=subprocess.PIPE, check=True
    )
    assert result == f"{expected_value_prefix}{expected_value}"


@pytest.mark.parametrize(
    "with_prefix",
    [False, True],
)
def test_auth_from_command_local_exec_failure(
    mock_run,
    not_in_pipelines,
    not_using_local_ide,
    is_a_tty,
    monkeypatch,
    with_prefix,
) -> None:
    # Given
    mock_run.side_effect = subprocess.CalledProcessError(1, cmd="a-value")

    # When

    with pytest.raises(RuntimeError):
        possibly_get_auth_from_atlas_cli(
            "eg",
            local_env_var="non-existing-value-11a",
            command=[],
            fallback_command="eg",
            with_prefix=with_prefix,
        )

    # Then
    mock_run.assert_called_once_with(
        [], encoding="utf-8", stdout=subprocess.PIPE, check=True
    )
