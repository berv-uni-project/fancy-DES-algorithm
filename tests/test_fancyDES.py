from fancyDES.fancyDES import FancyDES
import binascii

def test_main_function():
  MODE = "OFB"
  desFancy = FancyDES(
        path="samples/lorem-ipsum.txt", key="HELLO WORLD! HAHAHHA", fromFile=True
  )
  original_message = desFancy.message
  cipher = desFancy.generate_cipher(mode=MODE)
  fancyDES1 = FancyDES(message=cipher, key="HELLO WORLD! HAHAHHA", fromFile=False)
  plainteks = fancyDES1.generate_cipher(decrypt=True, mode=MODE)
  binascii.hexlify(plainteks)
  assert plainteks.startswith(original_message)