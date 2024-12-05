# SymplaTools SDK

SymplaTools é um SDK para integração com a plataforma Sympla, atualmente incluindo funcionalidades como:

* Validação de QR codes assinados com ECDSA.

---

## Instalação

Para instalar as dependências, use [Poetry](https://python-poetry.org/):

```bash
poetry install
```

## Configuração

Para validar a assinatura, é necessário definir o endereço Ethereum conhecido (`KNOWN_ETHEREUM_ADDRESS`) como uma variável de ambiente. Este será o endereço usado para verificar a autenticidade da assinatura do QR code.

Configure o endereço Ethereum conhecido com o seguinte comando:

```bash
export KNOWN_ETHEREUM_ADDRESS="0x0ff5a47F678e1E490b9c467631Ab84Dc1665a7eA"
```

## Uso

Após configurar o endereço Ethereum, você pode usar o SDK para validar a assinatura de um QR code Ethereum.

### Exemplo de uso via linha de comando

Para validar uma assinatura via linha de comando, execute:

```bash
python -m sympla_tools.tickets.validate "ASSINATURA"
```

Substitua `"ASSINATURA"` pela assinatura que deseja validar. O SDK verificará se a assinatura corresponde ao endereço Ethereum configurado.

### Funções Principais

- **validate_signature**: Função principal para validar uma assinatura Ethereum. A função compara a assinatura com o endereço configurado e retorna se a assinatura é válida.

