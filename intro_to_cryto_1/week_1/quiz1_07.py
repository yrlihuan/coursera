c1 = "6c73d5240a948c86981bc294814d".decode("hex")
m1 = "attack at dawn"

k = ""
for i in xrange(0, len(c1)):
  k += chr(ord(c1[i]) ^ ord(m1[i]))

c2 = ""
m2 = "attack at dusk"
for i in xrange(0, len(m2)):
  c2 += chr(ord(k[i]) ^ ord(m2[i]))

print c2.encode('hex')

