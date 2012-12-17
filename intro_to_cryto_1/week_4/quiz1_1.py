iv = "20814804c1767293b99f1d9cab3bc3e7"
cipher = "ac1e37bfb15599e5f40eef805488281d"

ch1 = "1"
ch2 = "5"

c = ord(ch1) ^ ord(ch2)
iv_ = iv.decode("hex")
iv_ = iv_[0:8] + chr(ord(iv_[8]) ^ c) + iv_[9:]
iv = iv_.encode("hex")

print len(iv)
print iv
