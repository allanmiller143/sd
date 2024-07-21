import stomp
import time

conexao = stomp.Connection([('localhost',61613)])
#conexao = stomp.Connection()
conexao.connect('', '', wait=True)

nomes = ['Marco', 'Guilherme', 'Othon', 'Allan', 'Julio', 'Duda', 'Marcela','Daniel', 'Gabriel', 'JP', 'Ana', 'Elian']

for n in nomes:
  time.sleep(1)
  print(n)
  conexao.send(body=n, destination='/queue/UPE-SD')


conexao.disconnect()



