files = $(find -type f -name '*.py')
all: .clean .build .upload .install

.clean:
	@echo "cleaning"
	if [ -d ./build ]; then rm -rf ./build; fi
	if [ -d ./dist ]; then rm -rf ./dist; fi
	if [ -d ./docs ]; then rm -rf ./docs; fi
	find -type d -name '*.egg-info' -prune -exec rm -r "{}" \;

.build: $(files) .clean
	@echo "building"
	pdoc --html --force --output-dir docs src/ptkcmd
	python3 setup.py sdist bdist_wheel
.upload: .build
	@echo "uploading"
	python3 -m twine upload dist/*
.install: .upload
	@echo "installing"
	sleep 2
	python3 -m pip install --user --upgrade --force-reinstall --no-cache ptkcmd
