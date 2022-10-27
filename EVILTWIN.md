Uma ideia de Sandman: Incluir o ataque "Evil Twin" no Wifite.

Esta página rastreia os requisitos para esse recurso.

Gémeo mau
=========

O [Fluxion](https://github.com/FluxionNetwork/fluxion) é um exemplo popular desse ataque.

O ataque requer várias placas wireless:

1. Hospeda o gêmeo.
2. Desautentica clientes.

À medida que os clientes se conectam ao Evil Twin, eles são redirecionados para uma página de login do roteador falsa.

Os clientes inserem a senha no AP de destino. O Gêmeo Maligno então:

1. Captura a senha do Wifi,
2. Verifica a senha do Wifi em relação ao AP de destino,
3. Se válido, todos os clientes são desautenticados do Evil Twin para que eles voltem a se juntar ao AP alvo.
4. Caso contrário, diga ao usuário que a senha é inválida e "tente novamente". GOTO passo #1.

Abaixo estão todos os requisitos/componentes que o Wifite precisaria para esse recurso.


DHCP
====
Precisamos atribuir automaticamente endereços IP aos clientes à medida que eles se conectam (via DHCP?).


Redirecionamentos de DNS
========================
Todas as solicitações de DNS precisam redirecionar para o servidor web:

1. Então nós clientes somos encorajados a fazer o login.
2. Para que possamos interceptar verificações de integridade da Apple/Google


Rogue AP, endereço IP do servidor, etc
======================================
Provavelmente algumas maneiras de fazer isso no Linux; deve usar o método mais confiável e suportado.

Principalmente precisamos:

1. Rode o servidor Web em alguma porta (8000)
2. Inicie o Rogue AP
3. Atribuir localhost na porta 8000 a algum IP de sub-rede (192.168.1.254)
4. Inicie o redirecionamento de DNS de todos os nomes de host para 192.168.1.254.
5. Inicie o DHCP para atribuir IPs automaticamente aos clientes de entrada.
6. Inicie a desautenticação de clientes do AP real.

Acho que as etapas 3-5 podem ser aplicadas a uma placa sem fio específica (interface).

* FAÇAM~: Mais detalhes sobre como iniciar o AP falso, atribuir IPs, DHCP, DNS, etc.
   * Fluxion usando `hostapd`: [código](https://github.com/FluxionNetwork/fluxion/blob/16965ec192eb87ae40c211d18bf11bb37951b155/lib/ap/hostapd.sh#L59-L64)
   * Kali "Evil Wireless AP" (usa `hostapd`): [artigo](https://www.offensive-security.com/kali-linux/kali-linux-evil-wireless-access-point/)
   * Fluxion usando `airbase-ng`: [código](https://github.com/FluxionNetwork/fluxion/blob/16965ec192eb87ae40c211d18bf11bb37951b155/lib/ap/airbase-ng.sh#L76-L77)
* FAÇAM: O Evil Twin deve falsificar o endereço MAC do hardware do AP real?
   * Sim, parece que é isso que o Fluxion faz ([código](https://github.com/FluxionNetwork/fluxion/blob/16965ec192eb87ae40c211d18bf11bb37951b155/lib/ap/hostapd.sh#L66-L74)).


ROGUE AP
========
Recolhi esta informação de:

* ["Configurando ponto de acesso sem fio em Kali"](https://www.psattack.com/articles/20160410/setting-up-a-wireless-access-point-in-kali/) por PSAttack
* ["Ponto de acesso sem fio Kali Linux Evil"](https://www.offensive-security.com/kali-linux/kali-linux-evil-wireless-access-point/) por OffensiveSecurity
* [Script hostapd "SniffAir"](https://github.com/Tylous/SniffAir/blob/master/module/hostapd.py)


HOSTAPD
-------
* Inicia o ponto de acesso.
* Não incluído no Kali por padrão.
* Instalável através de `apt-get install hostapd`.
* [Documentos](https://wireless.wiki.kernel.org/en/users/documentation/hostapd)

Formato do arquivo de configuração (por exemplo `~/hostapd.conf`):

```
driver=nl80211   # 'nl80211' appears in all hostapd tutorials I've found.
ssid=$EVIL_SSID  # SSID/name of Evil Twin (should match target's)
hw_mode=$BAND    # Wifi Band, e.g. "g" or "g+n"
channel=$CHANNEL # Numeric, e.g. "6'
```

Run:

```
hostapd ~/hostapd.conf -i wlan0
```


DNSMASQ
-------

* Incluído em Kali.
* Instalável via `apt-get install dnsmasq`
* Manipula DNS e DHCP.
* [Instalação e visão geral](http://www.thekelleys.org.uk/dnsmasq/doc.html), página de [manual](http://www.thekelleys.org.uk/dnsmasq/docs/dnsmasq-man.html)

Formato do arquivo de configuração (por exemplo `~/dnsmasq.conf`):

```
interface=wlan0
dhcp-range=10.0.0.10,10.0.0.250,12h
dhcp-option=3,10.0.0.1
dhcp-option=6,10.0.0.1
#no-resolv
server=8.8.8.8
log-queries
log-dhcp

# Redirect all requests (# is wildcard) to IP of evil web server:
# TODO: We should rely on iptables, right? Otherwise this redirects traffic from all ports...
#address=/#/192.168.1.254
```

Formato de arquivo "Entradas DNS"  (`~/dns_entries`):

```
[DNS Name] [IP Address]
# TODO: Are wildcards are supported?
* 192.168.1.254 # IP of web server
```

Run:

```
dnsmasq -C ~/dnsmasq.conf -H ~/dns_entries
```

IPTABLES
--------
A partir [deste tópico em raspberrypi.org](https://www.raspberrypi.org/forums/viewtopic.php?p=288263&sid=b6dd830c0c241a15ac0fe6930a4726c9#p288263)

> *Use iptables to redirect all traffic directed at port 80 to the http server on the Pi*
> `sudo iptables -t nat -A PREROUTING -d 0/0 -p tcp –dport 80 -j DNAT –to 192.168.1.254:80`

E de Andreas Wiese no [UnixExchange](https://unix.stackexchange.com/a/125300)

> *You could get this with a small set of iptables rules redirecting all traffic to port 80 and 443 your AP's address:*
> `# iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination localhost:80`
> `# iptables -t nat -A PREROUTING -p tcp --dport 443 -j DNAT --to-destination localhost:80`

FAÇAM:

* E o tráfego HTTPS (porta 443)?
   * Queremos evitar avisos do navegador (assustadores no Chrome e Firefox).
   * Não pense que podemos enviar um redirecionamento 302 para a porta 80 sem acionar o problema de certificado inválido.
   * sslstrip pode contornar isso...


DEAUTHING
=========
Ao hospedar o Evil Twin + Web Server, precisamos desautenticar os clientes do AP de destino para que eles se juntem ao Evil Twin.

Ouvindo
-------
Precisamos ouvir mais clientes e iniciar automaticamente a eliminação de novos clientes à medida que eles aparecem.

Isso pode ser suportado por ferramentas existentes...

MDK
---
Deauthing & DoS é fácil de fazer usando [MDK](https://tools.kali.org/wireless-attacks/mdk3) ou `aireplay-ng`.

Acho que o MDK é uma ferramenta melhor para este trabalho, mas o Wifite já requer a `aircrack` suíte, então devemos oferecer suporte a ambos.

FAÇAM: Exigir MDK se estiver milhas à frente de `aireplay-ng`
FAÇAM: Descobrir comandos MDK para deauths persistentes; se pudermos fornecer uma lista de endereços MAC e BSSIDs de clientes.


Local na rede Internet
======================

Páginas de login do roteador
----------------------------
Estes são diferentes para cada fornecedor.

O Fluxion tem um repositório com páginas de login falsas para muitos fornecedores de roteadores populares ([FluxionNetwork/sites](https://github.com/FluxionNetwork/sites)). Esse repositório inclui sites em vários idiomas.

Precisamos apenas do HTML da página básica do roteador (Título/logotipo) e CSS (cores/fonte) para fornecedores populares.

Também precisamos de uma página de login "genérica" caso não tenhamos a página de um fornecedor.

1. Servidor Web para hospedar HTML, imagens, fontes e CSS que o fornecedor usa.
2. Javascript para enviar a senha para o servidor web


Suporte de linguas
------------------
Nota: Os usuários devem escolher o idioma para hospedar; eles sabem melhor do que qualquer detecção de script.

Cada página do roteador terá uma mensagem de aviso informando ao cliente que eles precisam inserir a senha do Wifi:
   * "A senha é necessária após uma atualização de firmware do roteador"

O conteúdo da página de login (HTML/imagens/css) pode ser reduzido apenas ao logotipo e mensagem de aviso. Sem navbars/sidebars/links para qualquer outra coisa.

Então, apenas a mensagem de aviso precisa ser modelada por idioma (só precisamos de uma frase por idioma).

Isso evitaria a necessidade de "sites" separados para cada Fornecedor e idioma.

Mas provavelmente precisamos que outros rótulos sejam traduzidos também:

* Título da página ("Página de login do roteador")
* "Senha:"
* "Digite novamente a senha:"
* "Reconectar" ou "Login"

...Então 5 frases por idioma. Nada mal.

O servidor web pode enviar um arquivo Javascript contendo os valores da variável de idioma:

```javascript
document.title = 'Router Login';
document.querySelector('#warn').textContent('You need to login after router firmware upgrade.');
document.querySelector('#pass').textContent('Password:');
// ...
```


Um arquivo HTML
---------------
Podemos compactar tudo em um único arquivo HTML:

1. CSS embutido
2. Imagens em linha (imagem base64/jpg)
3. Alguns espaços reservados para a mensagem de aviso, etiqueta de senha, botão de login.

Isso evitaria o problema de "muitas pastas"; uma pasta para todos os arquivos .html.

Por exemplo `ASUS.html` pode ser escolhido quando o fornecedor MAC de destino contém arquivos `ASUS`.


Envio de senha AJAX
-------------------
O site precisa enviar a senha para o servidor web, provavelmente por meio de algum endpoint (por exemplo `./login.cgi?password1=...&password2=...`).

Fácil de fazer em Javascript (através de um simples `<form>` ou até mesmo `XMLHttpRequest`).


Servidor web
============
Os sites atendidos pelo servidor web são dinâmicos e dependem de inúmeras variáveis.

Queremos utilizar o CGIHTTPServer em Python, o que tornaria a lógica mais fácil de rastrear.


Falsificação de verificações de integridade
-------------------------------------------
Alguns dispositivos (Android, iOS, Windows?) verificam se o AP tem uma conexão com a Internet solicitando alguma página da Web hospedada externamente.

Queremos falsificar essas páginas exatamente para que o dispositivo do cliente mostre o Evil Twin como "online".

O Fluxion faz isso [aqui](https://github.com/FluxionNetwork/fluxion/tree/master/attacks/Captive%20Portal/lib/connectivity%20responses) (chamado "Respostas de conectividade" ).

Especificamente [no `lighttpd.conf` aqui](https://github.com/FluxionNetwork/fluxion/blob/16965ec192eb87ae40c211d18bf11bb37951b155/attacks/Captive%20Portal/attack.sh#L687-L698).

Requisitos:

* O Webserver detecta solicitações para essas páginas de verificação de integridade e retorna a resposta esperada (HTML, 204, etc).

FAÇAM: Passe pelo Fluxion para saber nomes de host/caminhos e respostas esperadas para dispositivos Apple e Google.


HTTPS
-----
E se o Google, a Apple exigir HTTPS? Podemos falsificar os certificados de alguma forma? Ou redirecionar para HTTP?


Falsificação de páginas de login do roteador
--------------------------------------------
Podemos detectar o fornecedor do roteador com base no endereço MAC.

Se tivermos uma página de login falsa para esse fornecedor, nós a serviremos.

Caso contrário, servimos uma página de login genérica.

FAÇAM: Podemos usar o macchanger para detectar o fornecedor ou ter algum mapeamento de `BSSID_REGEX -> HTML_FILE`?


Captura de senha
----------------
O servidor Web precisa saber quando um cliente digita uma senha.

Isso pode ser feito por meio de um endpoint CGI simples ou script Python.

Por exemplo `login.cgi` que lê `password1` e `password2` da string de consulta.


Validação de senha
------------------
O servidor Web precisa saber quando a senha é válida.

Isso requer a conexão ao AP de destino em uma placa sem fio não utilizada:

1. O primeiro cartão está hospedando o servidor web. Seria estranho se isso acontecesse.
2. O segundo cartão são os clientes Deauthing. Isso pode ser 'pausado' durante a validação da senha, mas isso pode permitir que os clientes se conectem ao AP de destino.
3. ...Uma terceira placa wifi pode tornar isso mais limpo.

FAÇAM: Os comandos exatos para verificar senhas Wifi no Linux; Eu estou supondo que nós temos que usar `wpa_supplicant` e afins.
FAÇAM: Escolha o método mais rápido e confiável para verificar senhas wifi


Servidor Web do mal & Comunicação Deauth
----------------------------------------
O ponto de acesso que hospeda o Evil Twin precisa se comunicar com o mecanismo Deauth:

1. Quais BSSIDs apontar para o Gêmeo do Mal,
2. Quais BSSIDs apontar para o AP real.

Como o servidor da web precisa ser executado durante todo o ataque, poderíamos controlar o estado do ataque dentro do servidor da web.

Portanto, o servidor da Web precisaria manter:

1. Lista de BSSIDs para deauth do AP real (assim eles se juntam ao Evil Twin),
2. Lista de BSSIDs para deauth do Evil Twin (para que eles se juntem ao AP real),
3. Processo em segundo plano que desabilita os BSSIDs acima em uma placa sem fio separada.

Não tenho certeza de quão viável isso é em Python; também podemos recorrer ao uso de arquivos estáticos para armazenar o estágio (por exemplo, arquivo JSON com BSSIDs e etapa atual - por exemplo, "Desligando" ou "Aguardando senha").

FAÇAM: Veja se o CGIHTTPServer tem alguma forma de manter/alterar threads em segundo plano.
FAÇAM: Veja como seria difícil manter o estado no CGIHTTPServer (temos que usar o sistema de arquivos?)


Sucesso e limpeza
-----------------
Quando a senha for encontrada, queremos enviar uma mensagem de "sucesso" para a solicitação AJAX, para que o usuário receba um feedback instantâneo (e talvez uma mensagem "Reconectando...").

Durante o desligamento, precisamos desativar todos os clientes do Evil Twin para que eles se juntem ao AP real.

Essa desautenticação deve continuar até que todos os clientes sejam desautenticados do Evil Twin.

Em seguida, o script pode ser interrompido.


Prova de conceito
=================

Inicie o AP e capture todo o tráfego da porta 80:

```
ifconfig wlan0 10.0.0.1/24 up

# start dnsmasq for dhcp & dns resolution (runs in background)
killall dnsmasq
dnsmasq -C dnsmasq.conf

# reroute all port-80 traffic to our machine
iptables -N internet -t mangle
iptables -t mangle -A PREROUTING -j internet
iptables -t mangle -A internet -j MARK --set-mark 99
iptables -t nat -A PREROUTING -m mark --mark 99 -p tcp --dport 80 -j DNAT --to-destination 10.0.0.1
echo "1" > /proc/sys/net/ipv4/ip_forward
iptables -A FORWARD -i eth0 -o wlan0 -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A FORWARD -m mark --mark 99 -j REJECT
iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# start wifi access point (new terminal)
killall hostapd
hostapd ./hostapd.conf -i wlan0

# start webserver on port 80 (new terminal)
python -m SimpleHTTPServer 80
```

Limpar:

```
# stop processes
# ctrl+c hostapd
# ctrl+c python simple http server
killall dnsmasq

# reset iptables
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X
iptables -t mangle -F
iptables -t mangle -X
```

