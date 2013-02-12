import os
import stat
from datetime import datetime
from setuptools import setup

def read(fname):
	return open(os.path.join(os.path.dirname(__file__), fname)).read()

def most_recent_mod(directory):
	mod=0;
	for dirpath, dirnames, filenames in os.walk(directory): 
		for filename in filenames:
			fname=os.path.join(dirpath,filename)
			stats=os.stat(fname)
			mtime=stats[stat.ST_MTIME]
			mod=max(mod,stats[stat.ST_MTIME])
	return mod

src='src/of_util'

ver=datetime.fromtimestamp(most_recent_mod(src)).strftime('%Y.%m.%d.%H.%M')

setup(
	name='of_util',
	description='Some utility modules',
	author='Robert I. Petersen',
	author_email='python@orangefood.com', 
	version=ver, 
	package_dir={'of_util': src},
	packages=['of_util'], 
	license='GPL 2.0', 
	classifiers=[
'Development Status :: 4 - Beta',
'Intended Audience :: Developers',
'License :: OSI Approved :: GNU General Public License (GPL)',
'Programming Language :: Python',
'Topic :: Text Processing :: Markup :: XML'
	],
	long_description=read("README")
)
