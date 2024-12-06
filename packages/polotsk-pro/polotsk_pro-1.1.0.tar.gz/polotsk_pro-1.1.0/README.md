# POLOTSK

* polotsk project
* polotsk admin

```bash
python3.11 -m pip uninstall polotsk --break-system-packages
python3.11 setup.py sdist bdist_wheel
python3.11 -m twine upload --verbose --repository pypi dist/*
python3.11 -m pip install polotsk --upgrade --break-system-packages
ls $HOME/.local/lib/python3.11/site-packages/polotsk/
ls $HOME/.local/lib/python3.11/site-packages/polotsk-admin/
python3.11 -m polotsk-admin --app nn
```
