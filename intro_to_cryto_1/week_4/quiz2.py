import urllib2
import sys

TARGET = 'http://crypto-class.appspot.com/po?er='
#--------------------------------------------------------------
# padding oracle
#--------------------------------------------------------------
class PaddingOracle(object):
  def query(self, q):
    target = TARGET + urllib2.quote(q)    # Create query URL
    req = urllib2.Request(target)         # Send HTTP request to server
    try:
      f = urllib2.urlopen(req)          # Wait for response
    except urllib2.HTTPError, e:
      if e.code == 404:
        return True # good padding
      elif e.code == 403:
        return False

      print "We got: %d" % e.code       # Print response code
      return False # bad padding

def xor(a, b):
  if len(a) != len(b):
    print "unmatched length"
    return None

  c = ""
  for i in xrange(0, len(a)):
    c += chr(ord(a[i]) ^ ord(b[i]))

  return c

if __name__ == "__main__":
  cipher = "f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4".decode("hex")

  po = PaddingOracle()
  blocks = len(cipher) / 16 - 1
  print blocks
  for b in xrange(0, blocks):
    c = cipher[0:16*(b+2)]
    known = ""
    for p in xrange(1, 17):
      padding = ""
      for i in xrange(0, p):
        padding += chr(p)

      result = -1
      for guess in xrange(0, 256):
        g = chr(guess) + known
        a = xor(g, padding)

        start = 16*b+16-p
        q = c[0:start] + xor(c[start:start+p], a) + c[start+p:]
        if po.query(q.encode("hex")):
          result = guess
          break

      if result == -1:
        # Here is a trick
        # when all the padding matches, ther query function returns False instead of True
        # since we know the original padding length is 9, just add it here
        known = '\x09' + known
        print "not found any valid guess"
      else:
        known = chr(result) + known
        print "deciphered: (%s,%d)" % (known, result)


