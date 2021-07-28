tar -cvzf hcfg.tar.gz ../*
python setup.py sdist
twine upload dist/*