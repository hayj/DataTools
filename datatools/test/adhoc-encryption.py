from datatools.dataencryptor import *
from systemtools.basics import *

de = DataEncryptor()

key = 'f5j7z15j69e94xcn1glo789'
idRsaPubPath = homeDir() + "/b.txt"
idRsa = fileToStr(idRsaPubPath)
key = idRsa + key
key = md5(key)
print(key)


encryptFile(homeDir() + "/b.json", key,
                            ext=de.encryptedExtensionSecondPart,
                            remove=False)









