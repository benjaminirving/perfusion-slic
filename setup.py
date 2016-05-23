
"""

Setup file for compiling cython extensions

To build cython libraries in place run:
python setup.py build_ext --inplace

# Build wheel and install wheel
python setup.py bdist_wheel
# Install wheel from local file
pip install perfusionslic-0.12-cp27-none-linux_x86_64.whl

"""

from setuptools import setup
from setuptools import Extension
from Cython.Build import cythonize

import numpy


Description = """/
Perfusion SLIC
"""

extensions = [
    Extension("perfusionslic.additional.bspline_smoothing",
              sources=["perfusionslic/additional/bspline_smoothing.pyx"],
              include_dirs=[numpy.get_include()]),
    Extension("perfusionslic.additional.create_im",
              sources=["perfusionslic/additional/create_im.pyx"],
              include_dirs=[numpy.get_include()]),
    Extension("perfusionslic._slic_feat",
              sources=["perfusionslic/_slic_feat.pyx"],
              include_dirs=[numpy.get_include()]),
    Extension("perfusionslic.additional.processing",
              sources=["perfusionslic/additional/processing.pyx",
                       "src/processing.cpp"],
              include_dirs=["src", numpy.get_include()],
              language="c++",
              extra_compile_args=["-std=c++11"])
]

setup(name="perfusionslic",
      packages=["perfusionslic", "perfusionslic.additional"],
      version="0.20",
      description="Library to calculate supervoxels on 4D perfusion images",
      author='Benjamin Irving',
      author_email='mail@birving.com',
      url='www.birving.com',
      long_description=Description,
      install_requires=['nibabel', 'scikit-image', 'scikit-learn', 'Cython', 'matplotlib'],
      ext_modules=cythonize(extensions)
)