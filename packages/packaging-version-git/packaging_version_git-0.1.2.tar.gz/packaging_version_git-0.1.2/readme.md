# packaging-version-git

Implementation of creating version based on git status

[![PyPI](https://img.shields.io/pypi/v/packaging-version-git)](https://pypi.org/project/packaging-version-git/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/packaging-version-git)](https://pypi.org/project/packaging-version-git/)

[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=rocshers_packaging-version-git&metric=coverage)](https://sonarcloud.io/summary/new_code?id=rocshers_packaging-version-git)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=rocshers_packaging-version-git&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=rocshers_packaging-version-git)

[![Downloads](https://static.pepy.tech/badge/packaging-version-git)](https://pepy.tech/project/packaging-version-git)
[![GitLab stars](https://img.shields.io/gitlab/stars/rocshers/python/packaging-version-git)](https://gitlab.com/rocshers/python/packaging-version-git)
[![GitLab last commit](https://img.shields.io/gitlab/last-commit/rocshers/python/packaging-version-git)](https://gitlab.com/rocshers/python/packaging-version-git)

## Documentation

Install:

```bash
pip install packaging-version-git
```

Usage:

```python
from packaging_version_git import GitVersion

version = GitVersion.from_tag()
print(version) # 0.1.0

version = GitVersion.from_commit(as_dev=True)
print(version) # 0.1.0.dev5+ef7fd31
```

## Contribute

Issue Tracker: <https://gitlab.com/rocshers/python/packaging-version-git/-/issues>  
Source Code: <https://gitlab.com/rocshers/python/packaging-version-git>

Before adding changes:

```bash
make install
```

After changes:

```bash
make format test
```
