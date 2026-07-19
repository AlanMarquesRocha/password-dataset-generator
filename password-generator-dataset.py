#!/usr/bin/env python3
"""
Gerador de Dataset de Senhas Aleatórias
========================================
Gera senhas de diversos tipos e salva tudo em um dataset CSV com metadados
(tipo, comprimento, entropia estimada, conjunto de caracteres usado).

Usa o módulo `secrets` (criptograficamente seguro) em vez de `random`.

Uso:
    python gerador_dataset_senhas.py                    # padrão: 100 por tipo
    python gerador_dataset_senhas.py -n 500             # 500 por tipo
    python gerador_dataset_senhas.py -n 200 -o meu.csv  # arquivo de saída custom
"""

import argparse
import csv
import math
import secrets
import string

# ---------------------------------------------------------------------------
# Conjuntos de caracteres
# ---------------------------------------------------------------------------
DIGITOS = string.digits
MINUSCULAS = string.ascii_lowercase
MAIUSCULAS = string.ascii_uppercase
LETRAS = string.ascii_letters
ALFANUMERICO = LETRAS + DIGITOS
SIMBOLOS = "!@#$%^&*()-_=+[]{};:,.<>?/|~"
COMPLETO = ALFANUMERICO + SIMBOLOS
HEX = string.hexdigits.lower()[:16]  # 0-9a-f
BASE64_URL = ALFANUMERICO + "-_"

# Lista de palavras simples para passphrases (estilo Diceware reduzido)
PALAVRAS = [
    "casa", "lua", "sol", "mar", "rio", "flor", "pedra", "vento", "fogo", "gelo",
    "monte", "nuvem", "chuva", "areia", "folha", "raiz", "trigo", "milho", "uva", "figo",
    "lobo", "urso", "gato", "peixe", "corvo", "aguia", "tigre", "leao", "zebra", "foca",
    "norte", "sul", "leste", "oeste", "verde", "azul", "roxo", "preto", "branco", "cinza",
    "ponte", "torre", "porta", "chave", "livro", "papel", "tinta", "vidro", "ferro", "ouro",
    "prata", "cobre", "sonho", "tempo", "noite", "tarde", "manha", "verao", "outono", "brisa",
]


# ---------------------------------------------------------------------------
# Funções auxiliares
# ---------------------------------------------------------------------------
def entropia_bits(tamanho_alfabeto: int, comprimento: int) -> float:
    """Entropia teórica em bits: comprimento * log2(tamanho do alfabeto)."""
    return round(comprimento * math.log2(tamanho_alfabeto), 2)


def escolher(charset: str, n: int) -> str:
    return "".join(secrets.choice(charset) for _ in range(n))


# ---------------------------------------------------------------------------
# Geradores de cada tipo de senha
# ---------------------------------------------------------------------------
def gerar_pin(comprimento: int = 6) -> tuple[str, float]:
    return escolher(DIGITOS, comprimento), entropia_bits(10, comprimento)


def gerar_minusculas(comprimento: int = 10) -> tuple[str, float]:
    return escolher(MINUSCULAS, comprimento), entropia_bits(26, comprimento)


def gerar_alfanumerica(comprimento: int = 12) -> tuple[str, float]:
    return escolher(ALFANUMERICO, comprimento), entropia_bits(62, comprimento)


def gerar_completa(comprimento: int = 16) -> tuple[str, float]:
    """Garante ao menos 1 minúscula, 1 maiúscula, 1 dígito e 1 símbolo."""
    while True:
        senha = escolher(COMPLETO, comprimento)
        if (any(c in MINUSCULAS for c in senha)
                and any(c in MAIUSCULAS for c in senha)
                and any(c in DIGITOS for c in senha)
                and any(c in SIMBOLOS for c in senha)):
            return senha, entropia_bits(len(COMPLETO), comprimento)


def gerar_hex(comprimento: int = 32) -> tuple[str, float]:
    return escolher(HEX, comprimento), entropia_bits(16, comprimento)


def gerar_base64url(comprimento: int = 22) -> tuple[str, float]:
    return escolher(BASE64_URL, comprimento), entropia_bits(64, comprimento)


def gerar_passphrase(num_palavras: int = 4, separador: str = "-") -> tuple[str, float]:
    palavras = [secrets.choice(PALAVRAS) for _ in range(num_palavras)]
    frase = separador.join(palavras)
    return frase, round(num_palavras * math.log2(len(PALAVRAS)), 2)


def gerar_pronunciavel(silabas: int = 5) -> tuple[str, float]:
    """Alterna consoante-vogal para gerar senhas fáceis de pronunciar."""
    consoantes = "bcdfghjklmnpqrstvz"
    vogais = "aeiou"
    partes = [secrets.choice(consoantes) + secrets.choice(vogais) for _ in range(silabas)]
    senha = "".join(partes)
    ent = round(silabas * (math.log2(len(consoantes)) + math.log2(len(vogais))), 2)
    return senha, ent


def gerar_token_secrets(nbytes: int = 16) -> tuple[str, float]:
    """Usa secrets.token_urlsafe diretamente."""
    return secrets.token_urlsafe(nbytes), round(nbytes * 8, 2)


# ---------------------------------------------------------------------------
# Definição dos tipos do dataset
# ---------------------------------------------------------------------------
TIPOS = {
    "pin_4":            (lambda: gerar_pin(4), "digitos"),
    "pin_6":            (lambda: gerar_pin(6), "digitos"),
    "minusculas_8":     (lambda: gerar_minusculas(8), "a-z"),
    "minusculas_12":    (lambda: gerar_minusculas(12), "a-z"),
    "alfanumerica_10":  (lambda: gerar_alfanumerica(10), "a-zA-Z0-9"),
    "alfanumerica_14":  (lambda: gerar_alfanumerica(14), "a-zA-Z0-9"),
    "completa_12":      (lambda: gerar_completa(12), "a-zA-Z0-9+simbolos"),
    "completa_16":      (lambda: gerar_completa(16), "a-zA-Z0-9+simbolos"),
    "completa_24":      (lambda: gerar_completa(24), "a-zA-Z0-9+simbolos"),
    "hex_32":           (lambda: gerar_hex(32), "0-9a-f"),
    "base64url_22":     (lambda: gerar_base64url(22), "base64url"),
    "passphrase_3":     (lambda: gerar_passphrase(3), "palavras"),
    "passphrase_4":     (lambda: gerar_passphrase(4), "palavras"),
    "passphrase_5":     (lambda: gerar_passphrase(5), "palavras"),
    "pronunciavel_4":   (lambda: gerar_pronunciavel(4), "silabas cv"),
    "pronunciavel_6":   (lambda: gerar_pronunciavel(6), "silabas cv"),
    "token_urlsafe_16": (lambda: gerar_token_secrets(16), "token_urlsafe"),
    "token_urlsafe_32": (lambda: gerar_token_secrets(32), "token_urlsafe"),
}


def classificar_forca(entropia: float) -> str:
    if entropia < 28:
        return "muito fraca"
    if entropia < 36:
        return "fraca"
    if entropia < 60:
        return "razoavel"
    if entropia < 128:
        return "forte"
    return "muito forte"


# ---------------------------------------------------------------------------
# Geração do dataset
# ---------------------------------------------------------------------------
def gerar_dataset(n_por_tipo: int, arquivo_saida: str) -> None:
    total = 0
    with open(arquivo_saida, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "id", "tipo", "senha", "comprimento",
            "charset", "entropia_bits", "forca",
        ])
        idx = 1
        for tipo, (gerador, charset) in TIPOS.items():
            for _ in range(n_por_tipo):
                senha, ent = gerador()
                writer.writerow([
                    idx, tipo, senha, len(senha),
                    charset, ent, classificar_forca(ent),
                ])
                idx += 1
                total += 1
    print(f"Dataset gerado: {arquivo_saida}")
    print(f"   {total} senhas ({n_por_tipo} de cada um dos {len(TIPOS)} tipos)")


def main():
    parser = argparse.ArgumentParser(description="Gera um dataset de senhas aleatórias.")
    parser.add_argument("-n", "--num", type=int, default=100,
                        help="Quantidade de senhas por tipo (padrão: 100)")
    parser.add_argument("-o", "--output", type=str, default="dataset_senhas.csv",
                        help="Arquivo CSV de saída (padrão: dataset_senhas.csv)")
    args = parser.parse_args()
    gerar_dataset(args.num, args.output)


if __name__ == "__main__":
    main()