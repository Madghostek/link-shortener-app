import string
alpha = string.ascii_letters+string.digits

#short semi random token, won't collide anytime soon
def rng():
	rng.state += 257305203047
	rng.state %= 4294967296
	return rng.state

def rtoken():
	print("rtoken")
	t = rng()
	with open("lasttoken","w") as f:
		f.write(str(t))
	print("wrote",t)
	link = ""
	while t>1:
		link+=alpha[t%len(alpha)]
		t//=len(alpha)
	return link