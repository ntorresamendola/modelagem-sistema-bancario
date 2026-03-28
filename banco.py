from __future__ import annotations
from abc import ABC, abstractmethod
import datetime

class Cliente:
    def __init__(self, endereco: str) -> None:
        self._endereço = endereco
        self._contas = []

    def realizar_transacao(self, conta: Conta, transacao: Transacao) -> None:
        transacao.registrar(conta)

    def adicionar_conta(self, conta:Conta) -> None:
        self._contas.append(conta)
        return

    @property
    def endereco(self) -> str:
        return self.endereco

    @endereco.setter
    def endereco(self, value:str) -> None:
        self.endereco = value

    @property
    def contas(self) -> list[Conta]:
        return self._contas

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}. Endereço: {self._endereço}, " 
            f"Número de contas: {len(self._contas)}." 
        )
    
class PessoaFisica(Cliente):
    def __init__(self, endereco: str,  cpf: str, data_nascimento: datetime.date, nome: str):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    @property
    def cpf(self) -> str:
        return self._cpf

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def data_nascimento(self) -> datetime.date:
        return self._data_nascimento
    
    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}. Nome: {self._nome}, Endereço: {self._endereço}, " 
            f"CPF: {self._cpf}, Data de nascimento: {str(self.data_nascimento)}, " 
            f"Número de contas: {len(self._contas)}."
        ) 


class Transacao(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod   
    def registrar(self, conta: Conta) -> None:
        pass

class Deposito(Transacao):
    def __init__(self, valor: float) -> None:

        if valor < 0:
            raise ValueError("O valor do depósito precisa ser positivo")
        
        super().__init__()
        self._valor = valor

    def registrar(self, conta: Conta) -> None:
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

    @property
    def valor(self) -> float:
        return self._valor
    
    def __str__(self) -> str:
        return f"Tipo de transação: depósito. Valor: {self._valor:.2f}."
    
class Saque(Transacao):
    def __init__(self, valor:float) -> None:

        if valor < 0:
            raise ValueError("O valor do saque precisa ser positivo")  
              
        super().__init__()
        self._valor = valor

    @property
    def valor(self) -> float:
        return self._valor
    
    def registrar(self, conta: Conta) -> None:
        if conta.sacar(self._valor):
            conta.historico.adicionar_transacao(self)
       
    def __str__(self) -> str:
        return f"Tipo de transação: saque. Valor: {self._valor:.2f}."        

class  Historico:
    def __init__(self) -> None:
        self._historico = []

    def adicionar_transacao(self, transacao: Transacao) -> None: 
        self._historico.append(transacao)

    @property
    def historico(self) -> list[Transacao]:
        return self._historico
    
    def __str__(self) -> str:
        historico_transacoes = ""
        if (len(self._historico) == 0):
            return "Sem movimentações"
        else:
            for transasoes in self._historico:
                historico_transacoes = historico_transacoes + str(transasoes) + "\n"
            return historico_transacoes

class Conta(object):
    def __init__(self, saldo: float, numero: int, agencia: str, cliente:  Cliente) -> None:
        if saldo < 0:
            raise ValueError("O saldo inicial não pode ser negativo")
        
        self._saldo = saldo
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()

    @property
    def agencia(self) -> str:
        return self._agencia
    
    @agencia.setter
    def agencia(self, value: str) -> None:
        self._agencia = value 

    @property
    def saldo(self) -> float:
        return self._saldo

    @saldo.setter
    def saldo(self, valor) -> None:
        if valor < 0:
            raise ValueError("A conta não pode ter saldo negativo")
        else:
            self._saldo = valor

    @property
    def historico(self) -> Historico:
        return self._historico
    
    def depositar(self, valor: float) -> bool:
            self._saldo += valor
            return True
        
    def sacar(self, valor: float) -> bool:
        if valor > self._saldo:
            print("Não há saldo suficiente para o saque")
            return False
        else:
            self._saldo -= valor
            return True 
        
    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: int) -> Conta:
        return cls(0, numero, "", cliente)
        
    def __str__(self) -> str:
            return f"Numero: {self._numero}, agência: {self._agencia}, saldo: {self.saldo}."

class ContaCorrente(Conta):
    def __init__(self, saldo: float, numero: int, agencia: str, cliente: Cliente, 
                limite: float, limite_saques: int) -> None:
        super().__init__(saldo, numero, agencia, cliente)

        if limite < 0:
            raise ValueError("Limite precisar ser número positivo")

        if limite_saques < 1:
            raise ValueError("Limite de saques deve ser pelo menos um")
        
        self._limite = limite
        self._limite_saques = limite_saques

    @property
    def limite(self) -> float:
        return self._limite
    
    @limite.setter
    def limite(self, value:float) -> None:
        if value < 0:
            raise ValueError("Limite precisar ser número positivo")
        self._limite = value
    
    @property
    def limite_saques(self) -> int:
        return self._limite_saques

    @limite_saques.setter
    def limite_saques(self, value:int) -> None:
        if value < 1:
            raise ValueError("Limite de saques deve ser pelo menos um")
        self._limite_saques = value

    def sacar(self, valor: float) -> bool:
        numero_saques = len(
            [saque for saque in self.historico.historico 
             if saque.__class__.__name__ == "Saque"]
        )
        if numero_saques >= self._limite_saques:
            print("Limite de saques excedido")
            return False
        else:
            return super().sacar(valor)
        
    def __str__(self) -> str:
        return (
            f"Numero: {self._numero}, agência: {self._agencia}, saldo: {self.saldo},"
            f"limite: {self._limite}, limite de saques: {self._limite_saques}"
        )
