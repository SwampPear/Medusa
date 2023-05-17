import datetime
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend


private_key = rsa.generate_private_key(
  public_exponent=65537,
  key_size=2048,
  backend=default_backend()
)

builder = x509.CertificateBuilder()
builder = builder.subject_name(x509.Name([
  x509.NameAttribute(NameOID.COUNTRY_NAME, u'US'),
  x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u'Georgia'),
  x509.NameAttribute(NameOID.LOCALITY_NAME, u'Madison'),
  x509.NameAttribute(NameOID.ORGANIZATION_NAME, u'NA'),
  x509.NameAttribute(NameOID.COMMON_NAME, u'NA')
]))
builder = builder.issuer_name(x509.Name([
  x509.NameAttribute(NameOID.COUNTRY_NAME, u'US'),
  x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u'Georgia'),
  x509.NameAttribute(NameOID.LOCALITY_NAME, u'Madison'),
  x509.NameAttribute(NameOID.ORGANIZATION_NAME, u'NA'),
  x509.NameAttribute(NameOID.COMMON_NAME, u'NA')
]))
builder = builder.not_valid_before(datetime.datetime.now())
builder = builder.not_valid_after(datetime.datetime.now() + datetime.timedelta(days=365))
builder = builder.serial_number(x509.random_serial_number())
builder = builder.public_key(private_key.public_key())
builder = builder.add_extension(
  x509.BasicConstraints(ca=True, path_length=None), critical=True
)

certificate = builder.sign(
  private_key=private_key, algorithm=hashes.SHA256(), backend=default_backend()
)

with open('private_key.pem', 'wb') as key_file:
  key_file.write(private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
  ))

with open('ca_certificat.pem', 'wb') as cert_file:
  cert_file.write(certificate.public_bytes(serialization.Encoding.PEM))