# Intent it to run this from root of project package and from their setup up needed installs + virtual environment

# Note, aim to manage python environments and packages with a mix of: pyenv (OG: https://github.com/pyenv/pyenv#windows ; Windows fork: https://github.com/pyenv-win/pyenv-win) and Poetry ()
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"

# NOTE YOU MAY HAVE TO CLOSE TERMINAL AND REOPEN FOR IT TO GET UPDATED PATH WHICH KNOWS WHERE PYENV IS 
# If pyenv is not recognised when you run it, close the terminal and start it again

# Alternative Install:
# pip install pyenv-win --target %USERPROFILE%\\.pyenv --no-user --upgrade

# Want to install python Poetry: https://python-poetry.org/docs/
# Use Pipx per their reccomendation to isolate python version: https://github.com/pypa/pipx
python -m pip install --user pipx

# Now actually install poetry
pipx install poetry

# Use pyenv to setup python version
