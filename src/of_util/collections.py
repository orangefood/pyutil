from . import LOG

class defaultsdict(dict):
	"""A dictionary that has another dictionary to provide
	default values when the key is not present in the dictionary"""
	def __init__(self, defaults=None):
		dict.__init__(self)
		self.defaults=defaults

	def __getitem__(self, key):
		try:
			return dict.__getitem__(self, key)
		except KeyError as err:
			if self.defaults!=None:
				return self.defaults[key]
			else:
				raise err

	def update_defaults(self,defaults):
		"""Provides a new dictionary for the defaults."""
		self.defaults=defaults
		return self

class Namespace(dict):
	def __init__():
		pass


	def __dir__(self):
		d=dir(self.__class__)
		d=d+self.__dict__.keys()+self.headers
		return sorted(d)


	def __getattr__(self,name):
		if name in self._cols:
			if len(self.shape)==1:
				return self[self._cols[name]]
			else:
				return np.array(self[:,self._cols[name]])
		else:
			return object.__getattr(self,name)


class dotdict(defaultsdict):
	"""A dictionary that can return keys from dictionaries within
	this dictionary using the dot-notation.  For example say there is a 
	dotdict called dd and dd contains another dictionary with the key 'foo' and 
	the value {'bar':42}.  Then dd['foo.bar'] returns 42, just as dd['foo']['bar'].

	Mostly (exclusivly) I use this for string formtting so:
	'The answer is $(foo.bar)d'%dd results in 'The answer is 42'

	This subclasses defaultsdict."""
	
	def __init__(self, local=None):
		defaultsdict.__init__(self,local)

	def __getitem__(self, key):
		try:
			return defaultsdict.__getitem__(self, key)
		except KeyError:
			v=self._getchilditem(self,key)
			LOG.debug('%s -> %s'%(key,v))
			return v

	def _getdotteditem(self,o,key):
			try:
				return self._getitemorattribute(o,key)
			except KeyError:
				return self._getchilditem(o,key)

	def _getchilditem(self,o,key):
			if '.' in key:
				(o2,dot,key2)=key.partition('.')
				LOG.debug("%s -> %s , %s"%(key,o2,key2))
				# When key='foo.bar' try to get o['foo'] or o.foo() or o.foo
				o2=self._getitemorattribute(o,o2) 
				return self._getdotteditem(o2,key2)
			else:
				raise KeyError(key)

	def _getitemorattribute(self,o,key):
		LOG.debug('_getitemorattribute( %s ,%s )',o,key)
		try:
			# First attempt try to get this from a mapping
			try:
				LOG.debug("%s.__getitem__( '%s' )",o,key)
				value=o.__getitem__(key) 
				LOG.debug('%s.__getitem__( %s ) = %s',o,key,value)
			except (TypeError,ValueError): # Maybe it wants an integer for the index?
				LOG.debug("%s.__getitem__( int( '%s' ) )",o,key,exc_info=True)
				value=o.__getitem__(int(key))
			LOG.debug('value = %s'%value)
		except (AttributeError, ValueError, KeyError,IndexError):
			# AttributeError -> no _me_getitem__ so not a mapping
			# ValueError -> Attempt to go from str to int failed
			# KeyError -> the item didn't exist in the mapping
			# Don't except IndexErrors, (maybe make it a key error)
			try:
				LOG.debug("%s.__getattribute__( '%s' )",o,key,exc_info=True)
				value=o.__getattribute__(key)
				if hasattr(value,'__call__'):
					try:
						value=value.__call__()
					except:
						pass
			except AttributeError:
				try: 
					LOG.debug("%s.__getattr__( '%s' )",o,key,exc_info=True)
					value=o.__getattr__(key)
					if hasattr(value,'__call__'):
						try:
							value=value.__call__()
						except:
							pass
				except (NameError,AttributeError):
					raise KeyError(key)
		LOG.debug('value = %s'%value)
		return value
		
			
