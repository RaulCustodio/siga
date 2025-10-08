import jpype, jpype.imports
from jpype.types import *
from pathlib import Path
import zipfile

JAR = r"C:\Users\raulc\Documents\SIGA\lib\mpxj.jar"

# 1) Verifique se o .jar contém a classe esperada
assert Path(JAR).is_file(), f"Jar inexistente: {JAR}"
with zipfile.ZipFile(JAR, 'r') as zf:
    has_cls = any(n.lower() == "net/sf/mpxj/reader/universalprojectreader.class" for n in zf.namelist())
print("Jar tem UniversalProjectReader.class?", has_cls)

# 2) Subir JVM com classpath explícito
print("JVM started before?", jpype.isJVMStarted())
if not jpype.isJVMStarted():
    # Ative a import hook do JPype
    import jpype.imports
    jpype.startJVM(classpath=[JAR])

from java.lang import System
cp = System.getProperty("java.class.path")
print("Classpath da JVM:", cp)

# 3) Tentar carregar via JClass (sem import hook)
try:
    UPR = jpype.JClass("net.sf.mpxj.reader.UniversalProjectReader")
    print("JClass carregou UniversalProjectReader ✔")
except Exception as e:
    print("JClass falhou:", repr(e))

# 4) Agora pelo import hook
try:
    from net.sf.mpxj.reader import UniversalProjectReader
    print("Import hook carregou UniversalProjectReader ✔")
except Exception as e:
    print("Import hook falhou:", repr(e))
