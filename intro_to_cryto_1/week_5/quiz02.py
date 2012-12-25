#!/usr/bin/env python

import gmpy
from gmpy import mpz

g = mpz(11717829880366207009516117596335367088558084999998952205599979459063929499736583746670572176471460312928594829675428279466566527115212748467589894601965568L)
p = mpz(13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171L)
h = mpz(3239475104050450443565264378728065788649097520952449527834792452971981976143292558073856937958553180532878928001494706097394108577585732452307673444020333L)

gbases = []
t = g
for i in xrange(0, 1024):
  gbases.append(t)
  t = t * t % p

def mpz_pow(exp):
  result = mpz(1)
  for i in xrange(0, exp.bit_length()):
    b = exp.getbit(i)
    if b == 1:
      result = result * gbases[i] % p

  return result

d = {}
for x0 in xrange(0, 1024*1024):
  exp = x0 * 1024 * 1024
  right = mpz_pow(mpz(exp))
  d[right] = x0

print "dict generated"

c0 = h
exp_start = p - 1 - (1024*1024-1)
c1 = mpz_pow(exp_start)
left = c0 * c1 % p

x = 0
for x1 in xrange(0, 1024*1024):
  if left in d:
    x0 = d[left]
    x1 = 1024*1024-1-x1
    print x0
    print x1
    x = x0 * 1024 * 1024 + x1
    break

  left = left * g % p

print x
print mpz_pow(mpz(x))








