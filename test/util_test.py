#import collections
execfile('collections.py')

def test(d,key):
	try:
		cmd="print 'd[%s] = %%(%s)s'%%d"%(key,key)
		print('"%s" results in:'%cmd)
		exec(cmd)
	except KeyError as ke:
		print 'KeyError: %s'%ke.message
class foo(object):
	def __init__(self):
		self.c='c'
		self.d=lambda: 'd'
		self.str='abcdefg'

d=dotdict()
a={'a': 1}
b={'b': a}
d['a']=a
d['b']=b
b['f']=foo()
d['numbers']=['one','two','three','four','five']

test(d,'a')
test(d,'a.a')
test(d,'b')
test(d,'b.a')
test(d,'b.b')
test(d,'b.b.a')
test(d,'b.f')
test(d,'b.f.c')
test(d,'b.f.d')
test(d,'b.f.str')
test(d,'b.f.str.2')
test(d,'numbers')
test(d,'numbers.4')
test(d,'numbers.-1')
test(d,'numbers.6')
test(d,'foobar')




