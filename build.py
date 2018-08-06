# v1.0.0
import os
from shutil import rmtree, move
from glob import glob

PACKAGE_NAME = "datareducer"

os.system("python3 setup.py sdist")
rmtree("./" + PACKAGE_NAME + ".egg-info")
move(glob("./dist/" + PACKAGE_NAME + "*")[0], "./")
rmtree("./dist")
