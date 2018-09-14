import operator

def accumulate(iterable, func=operator.add):
	def accum(iterable, func):
		total = 0
		for x in iterable:
			total = func(total, x)
			yield total

	return list(accum(iterable, func))

def makeList(l):
	if not l:
		return []
	elif not isinstance(l, list):
		return [l]
	else:
		return l

def minListLen(l, minLenght = 1):
	ls = makeList(l)

	for l in ls:
		if len(l) < minLenght:
			return False

	return True