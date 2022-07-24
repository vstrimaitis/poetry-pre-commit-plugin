# TODO: currently can't write realistic tests because running actual commands
# like `poetry install` during the test in some temporary directory doesn't work
# properly because `poetry` detects that it is running in a virtual environment
# and therefore doesn't create a new one. Related GH issue:
# https://github.com/python-poetry/poetry/issues/4055

def test_success():
    assert True

# Below is my initial attempt at a test which failed due to the issue above.

# import shutil
# from pathlib import Path
# import subprocess

# def copy_project(source_name: str, testing_dir: Path) -> None:
#     resources = Path(__file__).parent / "resources"
#     shutil.copytree(resources / source_name, testing_dir)

# def run_git_init(testing_dir: Path) -> None:
#     rc = subprocess.check_call(
#         ["git", "init"],
#         stdout=subprocess.DEVNULL,
#         stderr=subprocess.DEVNULL,
#         cwd=testing_dir,
#     )
#     assert rc == 0

# def run_install(testing_dir: Path) -> None:
#     rc = subprocess.check_call(
#         ["poetry", "install"],
#         stdout=subprocess.DEVNULL,
#         stderr=subprocess.DEVNULL,
#         cwd=testing_dir,
#     )
#     assert rc == 0

# def run_add(testing_dir: Path) -> None:
#     rc = subprocess.check_call(
#         ["poetry", "add", "--group", "dev", "pre-commit"],
#         stdout=subprocess.DEVNULL,
#         stderr=subprocess.DEVNULL,
#         cwd=testing_dir,
#     )
#     assert rc == 0


# def test_project_without_pre_commit_hooks(tmp_path: Path) -> None:
#     testing_dir = tmp_path / "testing_package"
#     copy_project("sample_project_no_pre_commit", testing_dir)
#     pre_commit_hook_path = testing_dir / ".git" / "hooks" / "pre-commit"
#     assert not pre_commit_hook_path.exists()

#     run_git_init(testing_dir)
#     assert not pre_commit_hook_path.exists()

#     run_install(testing_dir)  # <-- this pollutes the actual project's virtualenv
#     assert not pre_commit_hook_path.exists()

#     run_add(testing_dir)
#     assert pre_commit_hook_path.exists()
