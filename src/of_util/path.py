import os
import shutil

def copyr(src,dest,ignore=None):
	if not os.path.exists(dest):
		os.makedirs(dest)
		shutil.copystat(src,dest)
	src_files=os.listdir(src)
	if ignore!=None:
		src_files=list(set(src_files)^set(ignore(src,src_files)))
	for f in src_files:
		src_file=os.path.join(src,f)
		if os.path.isdir(src_file):
			copyr(src_file,os.path.join(dest,f),ignore)
		else:
			shutil.copy2(src_file,dest)	
