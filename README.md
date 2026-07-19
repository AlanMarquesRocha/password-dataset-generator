# Password Dataset Generator
 
Gerador de datasets de senhas aleatórias em Python. A ferramenta cria senhas sintéticas de **vários tipos e níveis de complexidade** e as exporta em formatos prontos para análise (CSV e JSON), acompanhadas de metadados úteis como comprimento, entropia estimada e rótulo de força.
 
Ideal para **testes de sistemas de autenticação**, **treinamento de classificadores de força de senha**, **benchmarks de validadores** e **pesquisa em segurança**. Tudo com dados 100% gerados e sintéticos, sem qualquer vazamento real.
 
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-ativo-brightgreen)
 
---
 
## Funcionalidades
 
- Geração de **múltiplos tipos** de senha em uma única execução
- Uso do módulo **`secrets`** (CSPRNG) para aleatoriedade criptograficamente segura
- Cálculo de **entropia** (bits) e classificação de **força** de cada senha
- Exportação para **CSV** e **JSON**
- Quantidade, comprimento e tipos totalmente **configuráveis** via linha de comando
- Reprodutibilidade opcional através de *seed*
- Código sem dependências externas (apenas biblioteca padrão)
---
 
## Tipos de senha suportados
 
| Tipo | Descrição | Exemplo |
|------|-----------|---------|
| `numeric` | Apenas dígitos (PINs, códigos) | `4820` |
| `alpha` | Apenas letras (maiúsculas + minúsculas) | `KpjWmZ` |
| `alphanumeric` | Letras e números | `x7Kp2mQ9` |
| `strong` | Letras, números e símbolos | `T7$k#9pL!2` |
| `memorable` | Passphrase de palavras separadas | `tigre-nuvem-forte-42` |
| `pronounceable` | Alternância consoante/vogal, mais fácil de ler | `kabolina` |
| `pattern` | Padrão fixo definido pelo usuário (ex: `Lldd-dddd`) | `Ab12-3456` |
 
---
 
## Instalação
 
```bash
git clone https://github.com/AlanMarquesROcha/password-dataset-generator.git
cd password-dataset-generator
```
 
Requer apenas Python 3.8 ou superior. Nenhuma dependência adicional é necessária.
 
---
 
## Uso
 
Geração básica (dataset com todos os tipos):
 
```bash
python generate_passwords.py --count 1000 --output dataset
```
 
Escolhendo tipos específicos e comprimento:
 
```bash
python generate_passwords.py --count 500 --types strong,memorable --length 16
```
 
Principais argumentos:
 
| Argumento | Descrição | Padrão |
|-----------|-----------|--------|
| `--count` | Número de senhas por tipo | `100` |
| `--types` | Tipos separados por vírgula (ou `all`) | `all` |
| `--length` | Comprimento base das senhas | `12` |
| `--output` | Nome-base dos arquivos de saída | `dataset` |
| `--format` | `csv`, `json` ou `both` | `both` |
| `--seed` | Semente para reprodutibilidade | `None` |
 
---
 
## Estrutura do dataset
 
Cada registro exportado contém:
 
| Coluna | Descrição |
|--------|-----------|
| `password` | A senha gerada |
| `type` | Tipo/categoria da senha |
| `length` | Número de caracteres |
| `entropy_bits` | Entropia estimada em bits |
| `strength` | Rótulo de força (`weak`, `medium`, `strong`, `very_strong`) |
| `has_upper` / `has_lower` / `has_digit` / `has_symbol` | Flags de composição |
 
Exemplo (CSV):
 
```csv
password,type,length,entropy_bits,strength,has_upper,has_lower,has_digit,has_symbol
T7$k#9pL!2,strong,10,65.5,very_strong,True,True,True,True
4820,numeric,4,13.3,weak,False,False,True,False
tigre-nuvem-forte-42,memorable,20,72.1,very_strong,False,True,True,True
```
 
---
 
## Estrutura do projeto
 
```
password-dataset-generator/
├── generate_passwords.py   # Script principal
├── dataset.csv             # Saída gerada (exemplo)
├── dataset.json            # Saída gerada (exemplo)
├── README.md
└── LICENSE
```
 
---
 
## Casos de uso
 
- Treinar e avaliar modelos de **classificação de força de senha**
- Testar **validadores** e regras de política de senha
- **Benchmark** de desempenho de sistemas de hashing/autenticação
- Popular ambientes de **teste/QA** com dados sintéticos realistas
- Estudos acadêmicos sobre **entropia** e composição de senhas
---
 
## Uso responsável
 
Este projeto gera **senhas sintéticas e aleatórias** apenas para fins legítimos de teste, pesquisa e desenvolvimento. O dataset **não** contém dados reais de usuários nem senhas provenientes de vazamentos. Utilize a ferramenta de forma ética e em conformidade com as leis e políticas aplicáveis.
 
---
 
## Contribuindo
 
Contribuições são bem-vindas! Sinta-se à vontade para abrir uma *issue* ou enviar um *pull request* com melhorias, novos tipos de senha ou correções.
 
1. Faça um *fork* do projeto
2. Crie uma *branch* (`git checkout -b feature/nova-funcionalidade`)
3. *Commit* das suas alterações (`git commit -m 'Adiciona nova funcionalidade'`)
4. *Push* para a *branch* (`git push origin feature/nova-funcionalidade`)
5. Abra um *Pull Request*
---
 
## 📄 Licença
 
Distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
