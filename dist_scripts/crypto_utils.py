from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA, ECC
from Crypto.Hash import SHA256
from Crypto.Signature import DSS


def aes_enc(key, text):
	cipher = AES.new(key, AES.MODE_EAX)
	enc_text, tag = cipher.encrypt_and_digest(text)
	return cipher.nonce, tag, enc_text


def aes_dec(key, nonce, tag, enc_text):
	cipher = AES.new(key, AES.MODE_EAX, nonce)
	return cipher.decrypt_and_verify(enc_text, tag)


def rsa_enc(public_key, text):
	key = RSA.import_key(public_key)
	return PKCS1_OAEP.new(key).encrypt(text)


def rsa_dec(private_key, enc_text):
	key = RSA.import_key(private_key)
	return PKCS1_OAEP.new(key).decrypt(enc_text)


def enc(public_key, text):
	session_key = get_random_bytes(16)
	enc_session_key = rsa_enc(public_key, session_key)
	nonce, tag, enc_text = aes_enc(session_key, text)
	return enc_session_key, nonce, tag, enc_text


def dec(private_key, enc_session_key, nonce, tag, enc_text):
	session_key = rsa_dec(private_key, enc_session_key)
	return aes_dec(session_key, nonce, tag, enc_text)


def ecc_signature_create(key, data):
	key = ECC.import_key(key)
	return DSS.new(key, "fips-186-3").sign(SHA256.new(data))


def ecc_signature_verify(key, data, signature):
	key = ECC.import_key(key)
	res = False
	try:
		DSS.new(key, "fips-186-3").verify(SHA256.new(data), signature)
		res = True
	except ValueError:
		pass
	return res


if __name__ == "__main__":
	text = b"hello"

	key = b"1234567890123456"
	nonce, tag, enc_text = aes_enc(key, text)
	print("nonce (%d): %s" % (len(nonce), nonce))
	print("tag (%d): %s" % (len(tag), tag))
	print("enc_text (%d): %s" % (len(enc_text), enc_text))
	print(aes_dec(key, nonce, tag, enc_text))

	key = RSA.generate(2048)
	private_key = key.export_key()
	public_key = key.publickey().export_key()
	print("private_key (%d): %s" % (len(private_key), private_key))
	print("public_key (%d): %s" % (len(public_key), public_key))
	enc_text = rsa_enc(public_key, text)
	print("enc_text (%d): %s" % (len(enc_text), enc_text))
	print(rsa_dec(private_key, enc_text))

	enc_session_key, nonce, tag, enc_text = enc(public_key, text)
	print("enc_session_key (%d): %s" % (len(enc_session_key), enc_session_key))
	print("nonce (%d): %s" % (len(nonce), nonce))
	print("tag (%d): %s" % (len(tag), tag))
	print("enc_text (%d): %s" % (len(enc_text), enc_text))
	print(dec(private_key, enc_session_key, nonce, tag, enc_text))

	key = ECC.generate(curve="P-256")
	private_key = key.export_key(format="PEM")
	public_key = key.public_key().export_key(format="PEM")
	print("private_key (%d): %s" % (len(private_key), private_key))
	print("public_key (%d): %s" % (len(public_key), public_key))
	signature = ecc_signature_create(private_key, text)
	print("signature (%d): %s" % (len(signature), signature))
	print(ecc_signature_verify(public_key, text, signature))
