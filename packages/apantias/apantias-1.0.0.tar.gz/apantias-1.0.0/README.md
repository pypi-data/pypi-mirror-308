new features/bugs/requests:
https://github.com/shakamaran/apantias/issues

Steps to upload package:
https://packaging.python.org/en/latest/tutorials/packaging-projects/

Uploading to PyPi works automatically when merging to the github main-branch.

Be sure to update the version both in __init__.py and pyproject.toml!

COL vs ROW Convention:

In ROOT its (col, row), but:
data is represented as (frame,row,nreps,col), so i will use (row, col) here, since its the
natural order in the array.