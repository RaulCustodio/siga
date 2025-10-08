import jpype
import jpype.imports
from jpype.types import *

# Caminho completo para o JAR
jar_path = r"C:\Users\raulc\Documents\SIGA\lib\mpxj.jar"

# Inicia a JVM se ainda não estiver ativa
if not jpype.isJVMStarted():
    jpype.startJVM(classpath=[jar_path])

# Agora a importação funciona
from net.sf.mpxj.reader import UniversalProjectReader

reader = UniversalProjectReader()
project = reader.read(r"C:\caminho\para\seu\arquivo.mpp")

for task in project.getTasks():
    print(f"Tarefa: {task.getName()} | Início: {task.getStart()} | Fim: {task.getFinish()}")
