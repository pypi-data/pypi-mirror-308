#!/bin/sh

echo
echo '[VERSION AT src/smyoon/sense/__init__.py]'
grep __version__ src/smyoon/sense/__init__.py

echo

echo '[VERSION AT pyproject.toml]'
grep version pyproject.toml
echo

echo '[VERSION AT README.md]'
grep version README.md
echo

echo 'Do versions match? (y/n)'
read -r ANSWER

echo "${ANSWER}"

if [ "${ANSWER}" = "n" ]; then
  exit
fi

sudo apt install python3.8
sudo apt install python3.8-venv

python3.8 --version
python3.8 -m pip install --upgrade pip
python3.8 -m pip install --upgrade build

rm -rf .github
rm -rf .idea
rm -rf .pytest_cache

rm -rf dist
mkdir dist
rm -rf .gitignore
rm -rf .idea

python3.8 -m build
git reset --hard

python3.8 -m pip install --upgrade twine

#cp -f ~/.pypirc_for_project_smyoonear ~/.pypirc
python3.8 -m twine upload dist/* --verbose --repository smyoon
#rm -rf ~/.pypirc

# python3.8 -m pip install --index-url https://test.pypi.org/simple/ --no-deps smyoon
# python3.8 -c 'import smyoon.sense; print(smyoon.sense.APIConfig())'
