#!/usr/bin/env python

import Crypto.Cipher.AES as AES


k1 = '140b41b22a29beb4061bda66b6747e14'
c1 = '4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81'

k2 = '140b41b22a29beb4061bda66b6747e14'
c2 = '5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253'

k3 = '36f18357be4dbd77f050515c73fcf9f2'
c3 = '69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329'

k4 = '36f18357be4dbd77f050515c73fcf9f2'
c4 = '770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451'

def cbc_decode(k, c):
  iv = c[0:16]
  start = 16

  cipher = AES.new(k, AES.MODE_ECB)

  result = ''
  while start < len(c):
    block = c[start:start+16]

    decoded = cipher.decrypt(block)
    for i in xrange(0, 16):
      iv_i = ord(iv[i])
      d_i = ord(decoded[i])

      result += chr(iv_i ^ d_i)

    iv = block
    start += 16

  padding = ord(result[-1])
  return result[0:-padding]

def ctr_decode(k, c):
  iv = c[0:16]
  start = 16

  cipher = AES.new(k, AES.MODE_ECB)

  result = ''
  while start < len(c):
    end = start + 16 > len(c) and len(c) or start + 16
    block = c[start:end]

    decoded = cipher.encrypt(iv)
    for i in xrange(0, len(block)):
      m_i = ord(block[i])
      d_i = ord(decoded[i])

      result += chr(m_i ^ d_i)

    iv = iv[0:15] + chr(ord(iv[-1]) + 1)
    if 0 == ord(iv[-1]):
      iv = iv[0:14] + chr(ord(iv[-2]) + 1) + iv[15]

    start += 16

  return result

if __name__ == "__main__":
  print cbc_decode(k1.decode('hex'), c1.decode('hex'))
  print cbc_decode(k2.decode('hex'), c2.decode('hex'))
  print ctr_decode(k3.decode('hex'), c3.decode('hex'))
  print ctr_decode(k4.decode('hex'), c4.decode('hex'))

