# SymplaTools SDK

SymplaTools é um SDK para integração com a plataforma Sympla, atualmente incluindo funcionalidades como:

* Validação de QR codes assinados com ECDSA.

---

# Pypi

Este projeto está em um repositório público, e tem como objetivo facilitar o uso das funcionalidades da Sympla.

https://pypi.org/project/sympla_tools/

###  Também disponível no package registry do gitlab

https://gitlab.com/symplax/sympla-tools/-/packages

---

## Instalação

Para instalar as dependências, use [Poetry](https://python-poetry.org/):

```bash
### Pypy
poetry add sympla-tools


### Package registry Gitlab
poetry add git+ssh://git@gitlab.com:gitlab.com/symplax/sympla-tools/-/packages#0.1.5
```

## Configuração

Para validar a assinatura, é necessário definir o endereço Ethereum conhecido (`KNOWN_ETHEREUM_ADDRESS`) como uma variável de ambiente. Este será o endereço usado para verificar a autenticidade da assinatura do QR code.

Configure o endereço Ethereum conhecido com o seguinte comando:

```bash
export KNOWN_ETHEREUM_ADDRESS="0x0ff5a47F678e1E490b9c467631Ab84Dc1665a7eA"
```

## Uso

Após configurar o endereço Ethereum, você pode usar o SDK para validar a assinatura de um QR code Ethereum.


### Você vai precisar ler o Qrcode

Para realizar a validação, será necessário construir o json contendo os campo em ordem:

* address
* ItemTypeId

Além do json, é necessário resgatar a assinatura (signature)

### Exemplo de uso via linha de comando

Para validar uma assinatura via linha de comando, execute:

```bash
python -m sympla_tools.tickets.signature.token validate '{"address": "0x3e3857e99BE213aA914942C6482c33161Df51E16", "ItemTypeId": "37884525610813"}' '0x1e6912e765694db61b5291c94469ba339f1b7da3e921d5c3acd8ced279565053120e3e866c0158fe0eeddefdd113303adc1e56e79a9f1503386251786d4881f31b'
```

Substitua `"ASSINATURA"` pela assinatura que deseja validar. O SDK verificará se a assinatura corresponde ao endereço Ethereum configurado.

### Funções Principais

- **validate**: Função principal para validar uma assinatura Ethereum. A função compara a assinatura com o endereço configurado e retorna se a assinatura é válida.

