files = setup.py src/ptkcmd/*.py
all: build upload install
build: $(files)
	echo "building"
	if [ -d ./build ]; then rm -rf ./build; fi
	if [ -d ./dist ]; then rm -rf ./dist; fi
	if [ -d ./ptkcmd.egg-info ]; then rm -rf ./ptkcmd.egg-info; fi
	pdoc --html --force --output-dir docs src/ptkcmd
	python3 setup.py sdist bdist_wheel
upload: build
	echo "uploading"
	python3 -m twine upload dist/*
install: upload
	echo "installing"
	python3 -m pip install --user --upgrade --force-reinstall ptkcmd
