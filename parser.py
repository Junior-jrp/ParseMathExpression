import re
from enum import Enum
from dataclasses import dataclass


class TipoToken(Enum):
    NUMERO = 'NUMERO'
    SOMA = 'SOMA'
    SUBTRACAO = 'SUBTRACAO'
    PRODUTO = 'PRODUTO'
    DIVISAO = 'DIVISAO'
    POTENCIA = 'POTENCIA'
    PARENTESES_ABRE = 'PARENTESES_ABRE'
    PARENTESES_FECHA = 'PARENTESES_FECHA'
    FIM_DA_EXPRESSAO = 'FIM_DA_EXPRESSAO'


@dataclass
class Token:
    tipo: TipoToken
    valor: object = None

    def __repr__(self):
        return f"Token({self.tipo.name}, {self.valor})"


class LexerError(Exception):
    pass


class Lexer:
    REGRAS_TOKEN = [
        (r'[ \t]+', None),
        (r'\d+(\.\d*)?', TipoToken.NUMERO),
        (r'\+', TipoToken.SOMA),
        (r'-', TipoToken.SUBTRACAO),
        (r'\*', TipoToken.PRODUTO),
        (r'\/', TipoToken.DIVISAO),
        (r'\^', TipoToken.POTENCIA),
        (r'\(', TipoToken.PARENTESES_ABRE),
        (r'\)', TipoToken.PARENTESES_FECHA),
    ]
    REGRAS_COMPILADAS = [(re.compile(regra), tipo) for regra, tipo in REGRAS_TOKEN]

    def __init__(self, expressao: str):
        self.expressao = expressao
        self.posicao = 0

    def proximo_token(self):
        while self.posicao < len(self.expressao):
            for regex, tipo in self.REGRAS_COMPILADAS:
                match = regex.match(self.expressao, self.posicao)
                if match:
                    valor = match.group(0)
                    self.posicao = match.end()

                    if tipo is None:
                        continue

                    if tipo == TipoToken.NUMERO:
                        return Token(tipo, float(valor))
                    else:
                        return Token(tipo, valor)

            raise LexerError(f"Caractere inválido na posição {self.posicao}: '{self.expressao[self.posicao]}'")

        return Token(TipoToken.FIM_DA_EXPRESSAO)

    def gerar_tokens(self):
        while True:
            token = self.proximo_token()
            yield token
            if token.tipo == TipoToken.FIM_DA_EXPRESSAO:
                break


class Expressao:
    def resolver(self):
        raise NotImplementedError("O método 'resolver' deve ser implementado nas subclasses.")


class Constante(Expressao):
    def __init__(self, valor):
        self.valor = valor

    def resolver(self):
        return self.valor

    def __repr__(self):
        return f"Constante({self.valor})"


class Unario(Expressao):
    def __init__(self, operando: Expressao):
        self.operando = operando


class Negacao(Unario):
    def resolver(self):
        return -self.operando.resolver()

    def __repr__(self):
        return f"Negacao({self.operando})"


class Binaria(Expressao):
    def __init__(self, esquerda: Expressao, direita: Expressao):
        self.esquerda = esquerda
        self.direita = direita


class Soma(Binaria):
    def resolver(self):
        return self.esquerda.resolver() + self.direita.resolver()

    def __repr__(self):
        return f"Soma({self.esquerda}, {self.direita})"


class Subtracao(Binaria):
    def resolver(self):
        return self.esquerda.resolver() - self.direita.resolver()

    def __repr__(self):
        return f"Subtracao({self.esquerda}, {self.direita})"


class Produto(Binaria):
    def resolver(self):
        return self.esquerda.resolver() * self.direita.resolver()

    def __repr__(self):
        return f"Produto({self.esquerda}, {self.direita})"


class Divisao(Binaria):
    def resolver(self):
        divisor = self.direita.resolver()
        if divisor == 0:
            raise ZeroDivisionError("Divisão por zero não é permitida.")
        return self.esquerda.resolver() / divisor

    def __repr__(self):
        return f"Divisao({self.esquerda}, {self.direita})"


class Potencia(Binaria):
    def resolver(self):
        return self.esquerda.resolver() ** self.direita.resolver()

    def __repr__(self):
        return f"Potencia({self.esquerda}, {self.direita})"


class ParserError(Exception):
    pass


class Parser:
    def __init__(self, token_generator):
        self.tokens = token_generator
        self.token_atual = None
        self._avancar()

    def _avancar(self):
        self.token_atual = next(self.tokens)

    def _consumir(self, tipo_esperado: TipoToken):
        if self.token_atual.tipo == tipo_esperado:
            self._avancar()
        else:
            raise ParserError(
                f"Token inesperado: esperado {tipo_esperado.name}, "
                f"encontrado {self.token_atual.tipo.name}"
            )

    def parse(self):
        if self.token_atual.tipo == TipoToken.FIM_DA_EXPRESSAO:
            raise ParserError("Expressão vazia não é permitida.")
        ast = self._expressao()
        if self.token_atual.tipo != TipoToken.FIM_DA_EXPRESSAO:
            raise ParserError("Expressão mal formada, tokens extras no final.")
        return ast

    def _fator(self):
        token = self.token_atual

        if token.tipo == TipoToken.SUBTRACAO:
            self._avancar()
            return Negacao(self._fator())
        if token.tipo == TipoToken.SOMA:
            self._avancar()
            return self._fator()
        if token.tipo == TipoToken.NUMERO:
            self._avancar()
            return Constante(token.valor)
        if token.tipo == TipoToken.PARENTESES_ABRE:
            self._avancar()
            expressao = self._expressao()
            self._consumir(TipoToken.PARENTESES_FECHA)
            return expressao

        raise ParserError(f"Token inesperado na análise: {token}")

    def _potencia(self):
        esquerda = self._fator()
        if self.token_atual.tipo == TipoToken.POTENCIA:
            self._avancar()
            direita = self._potencia()
            return Potencia(esquerda, direita)
        return esquerda

    def _termo(self):
        mapa_operacoes = {TipoToken.PRODUTO: Produto, TipoToken.DIVISAO: Divisao}
        esquerda = self._potencia()

        while self.token_atual.tipo in mapa_operacoes:
            operador = self.token_atual
            self._avancar()
            direita = self._potencia()
            esquerda = mapa_operacoes[operador.tipo](esquerda, direita)

        return esquerda

    def _expressao(self):
        mapa_operacoes = {TipoToken.SOMA: Soma, TipoToken.SUBTRACAO: Subtracao}
        esquerda = self._termo()

        while self.token_atual.tipo in mapa_operacoes:
            operador = self.token_atual
            self._avancar()
            direita = self._termo()
            esquerda = mapa_operacoes[operador.tipo](esquerda, direita)

        return esquerda


def resolver_expressao(expressao_str: str):
    try:
        lexer = Lexer(expressao_str)
        parser = Parser(lexer.gerar_tokens())
        arvore_sintatica = parser.parse()
        return arvore_sintatica.resolver()
    except (LexerError, ParserError, ZeroDivisionError) as e:
        raise


