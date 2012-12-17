#!/usr/bin/env python

import Crypto.Hash.SHA256 as SHA256

def calc_h0(data):
  l = len(data)
  chunks = (l + 1023) / 1024
  padding = ""
  digest = ""
  ind = chunks - 1
  while ind >= 0:
    start = 1024 * ind
    end = 1024 * (ind + 1)
    end = end > l and l or end

    payload = data[start:end]
    payload += padding

    padding = SHA256.SHA256Hash(payload).digest()
    digest = SHA256.SHA256Hash(payload).hexdigest()

    ind -= 1

  return digest




if __name__ == "__main__":
  sample = open("quiz_2_sample.mp4").read()

  print calc_h0(sample)

  target = open("quiz_2_target.mp4").read()

  print calc_h0(target)
