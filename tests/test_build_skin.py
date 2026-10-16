"""tools/build_skin.py with --out outside the repository.

A bench build writes the zip into a scratch directory. The summary line used
to call ``relative_to(ROOT)`` on the output path, which raised ValueError after
the zip was written, so the command exited 1 on a good build.
"""

from __future__ import annotations

import subprocess
import sys
import zipfile

from conftest import ROOT


def test_build_to_a_directory_outside_the_repo(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools" / "build_skin.py"),
            "--out",
            str(tmp_path),
            "service.tvos.pythonfix",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    zips = list(tmp_path.glob("service.tvos.pythonfix-*.zip"))
    assert len(zips) == 1
    assert str(zips[0]) in result.stdout
    with zipfile.ZipFile(zips[0]) as z:
        assert "service.tvos.pythonfix/addon.xml" in z.namelist()
