import os
from shutil import rmtree, move

PACKAGE_NAME = "datareducer"

os.system("python3 setup.py sdist")
rmtree("./" + PACKAGE_NAME + ".egg-info")
# rmtree("./build")

# test.pypi.org
os.system('python3 -m twine upload --repository-url "https://test.pypi.org/legacy/" "dist/*"')

# live
# os.system('python3 -m twine upload "dist/*"')
