from banco import *
import datetime

def testes():
    pessoa1 = Cliente("Travessa Vinte e Três, 1507. Araguari-MG")
    pessoa2 = PessoaFisica("Rua das Cegonhas, 235. Palhoça-SC.", "717.272.269-84", 
                           datetime.date(year=1960, month=12, day=22), "Tomás Cavalcanti Gomes")
    
    conta1 = Conta(100, 1, "123-1", pessoa1)
    conta2 = Conta(0, 2, "000-1",pessoa1)
    conta3 = ContaCorrente(40, 3, "356-1", pessoa1, 3000, 4)
    print(conta3)

    conta4 = ContaCorrente(0, 4, "000-1", pessoa2, 1000, 3)
    conta5 = Conta.nova_conta(pessoa2, 5)
    conta5.agencia = "000-2"
    conta5.saldo = 0
    print(conta5)

    print("")

    pessoa1.adicionar_conta(conta1)
    pessoa1.adicionar_conta(conta2)
    pessoa1.adicionar_conta(conta3)
    print(pessoa1)

    pessoa2.adicionar_conta(conta4)
    print(pessoa2)

    print("")

    pessoa1.realizar_transacao(pessoa1.contas[0], Deposito(20))
    pessoa1.realizar_transacao(pessoa1.contas[0], Deposito(100))
    pessoa1.realizar_transacao(pessoa1.contas[0], Saque(100))
    #deve exibir na tela que o saque não foi possível por falta de fundos
    pessoa1.realizar_transacao(pessoa1.contas[0], Saque(500))

    print("")

    print("Histórico de transações da conta 1:")
    print(pessoa1.contas[0].historico) 
    print(conta1.saldo) # saldo deverá ser de 120

    print("Histórico de transações da conta 2:")
    print(pessoa1.contas[1].historico)
    print(conta2.saldo) # saldo deverá ser de 0

    print("")
    pessoa2.realizar_transacao(pessoa2.contas[0], Deposito(500))
    pessoa2.realizar_transacao(pessoa2.contas[0], Saque(30))
    pessoa2.realizar_transacao(pessoa2.contas[0], Saque(30))
    pessoa2.realizar_transacao(pessoa2.contas[0], Saque(30))
    # a partir daqui deverá dizer que o limite de saques foi excedido e não alterar o saldo
    pessoa2.realizar_transacao(pessoa2.contas[0], Saque(30))
    pessoa2.realizar_transacao(pessoa2.contas[0], Saque(30))
    
    print(pessoa2.contas[0].historico) #deverá ter um depósito e três saques
    print(pessoa2.contas[0].saldo) #deverá ser de 410


if __name__ == "__main__":
    testes()