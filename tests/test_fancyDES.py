from fancyDES.fancyDES import FancyDES
import binascii

def test_expected_length():
  MODE = "OFB"
  desFancy = FancyDES(
        path="samples/lorem-ipsum.txt", key="HELLO WORLD! HAHAHHA", fromFile=True
  )
  cipher = desFancy.generate_cipher(mode=MODE)
  assert len(cipher) == 93184