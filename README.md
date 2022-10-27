Wifite
======

Este repositório é uma reescrita completa do [`wifite`](https://github.com/derv82/wifite), um script Python para auditoria de redes sem fio.

O Wifite executa as ferramentas de auditoria sem fio existentes para você. Pare de memorizar argumentos e opções de comando!

Wifite é projetado para usar todos os métodos conhecidos para recuperar a senha de um ponto de acesso sem fio (roteador). Esses métodos incluem:
1. WPS: O [ataque Offline Pixie-Dust](https://en.wikipedia.org/wiki/Wi-Fi_Protected_Setup#Offline_brute-force_attack)
1. WPS: O [ataque de PIN de força bruta online](https://en.wikipedia.org/wiki/Wi-Fi_Protected_Setup#Online_brute-force_attack)
2. WPA: O [WPA Handshake Capture](https://hashcat.net/forum/thread-7717.html) + offline crack.
3. WPA: A [captura de hash PMKID](https://hashcat.net/forum/thread-7717.html) + offline crack.
4. WEP: Vários ataques conhecidos contra WEP, incluindo fragmentação , chop-chop , aireplay , etc.

Execute wifite, selecione seus alvos e o Wifite começará automaticamente a tentar capturar ou quebrar a senha.

Sistemas operacionais suportados
---------------------------
Wifite é projetado especificamente para a versão mais recente do [**Kali** Linux](https://www.kali.org/). [ParrotSec](https://www.parrotsec.org/) também é suportado.

Outras distribuições de pen-testing (como BackBox ou Ubuntu) têm versões desatualizadas das ferramentas usadas pelo Wifite. Não espere suporte a menos que você esteja usando as versões mais recentes das Ferramentas Necessárias e também [drivers sem fio corrigidos que suportem injeção]().

Ferramentas necessárias
--------------
Em primeiro lugar, você precisará de uma placa wireless capaz de "Modo Monitor" e injeção de pacotes (veja [este tutorial para verificar se sua placa wireless é compatível](http://www.aircrack-ng.org/doku.php?id=compatible_cards) e também [este guia](https://en.wikipedia.org/wiki/Wi-Fi_Protected_Setup#Offline_brute-force_attack)). Existem muitas placas wireless baratas que se conectam ao USB disponíveis em lojas online.

Em segundo lugar, apenas as versões mais recentes desses programas são suportadas e devem ser instaladas para que o Wifite funcione corretamente:

**Requeridos:**

* `python`: Wifite é compatível com `python2` e `python3`.
* [`iwconfig`](https://wiki.debian.org/iwconfig): Para identificar dispositivos sem fio já no Modo Monitor.
* [`ifconfig`](https://en.wikipedia.org/wiki/Ifconfig): Para iniciar/parar dispositivos sem fio.
* [`Aircrack-ng`](http://aircrack-ng.org/) suíte, inclui:
   * [`airmon-ng`](https://tools.kali.org/wireless-attacks/airmon-ng): Para enumerar e habilitar o Modo Monitor em dispositivos sem fio.
   * [`aircrack-ng`](https://tools.kali.org/wireless-attacks/aircrack-ng): Para quebrar arquivos WEP .cap e capturas de handshake WPA.
   * [`aireplay-ng`](https://tools.kali.org/wireless-attacks/aireplay-ng): Para desautenticação de pontos de acesso, reprodução de arquivos de captura, vários ataques WEP.
   * [`airodump-ng`](https://tools.kali.org/wireless-attacks/airodump-ng): Para digitalização de destino e geração de arquivos de captura.
   * [`packetforge-ng`](https://tools.kali.org/wireless-attacks/packetforge-ng): Para forjar arquivos de captura.

**Opcional, mas recomendado:**

* [`tshark`](https://www.wireshark.org/docs/man-pages/tshark.html): Para detectar redes WPS e inspecionar arquivos de captura de handshake.
* [`reaver`](https://github.com/t6x/reaver-wps-fork-t6x): Para WPS Pixie-Dust e ataques de força bruta.
   * Nota: A `wash` ferramenta do Reaver pode ser usada para detectar redes WPS se `tshark` não for encontrada.
* [`bully`](https://github.com/aanarchyy/bully): Para WPS Pixie-Dust e ataques de força bruta.
   * Alternativa ao Reaver. Especifique `--bully` para usar Bully em vez de Reaver.
   * Bully também é usado para buscar PSK se `reaver` não puder depois de quebrar o PIN WPS.
* [`coWPAtty`](https://tools.kali.org/wireless-attacks/cowpatty): Para detectar capturas de handshake.
* [`pyrit`](https://github.com/JPaulMora/Pyrit): Para detectar capturas de handshake.
* [`hashcat`](https://hashcat.net/): Para quebrar hashes PMKID.
   * [`hcxdumptool`](https://github.com/ZerBea/hcxdumptool): Para capturar hashes PMKID.
   * [`hcxpcaptool`](https://github.com/ZerBea/hcxtools): Para converter capturas de pacotes PMKID para `hashcat`o formato 's.


Executar Wifi
----------
```
git clone https://github.com/derv82/wifite2.git
cd wifite2
sudo ./Wifite.py
```

Instalar Wifi
--------------
Para instalar no seu computador (para que você possa executar a `wifite` partir de qualquer terminal), execute:

```bash
sudo python setup.py install
```

Isso irá instalar `wifite` no `/usr/sbin/wifite` qual deve estar no caminho do terminal.

**Nota:** A desinstalação [não é tão fácil](https://stackoverflow.com/questions/1550226/python-setup-py-uninstall#1550235). A única maneira de desinstalar é gravar os arquivos instalados pelo comando acima e remover esses arquivos:

```bash
sudo python setup.py install --record files.txt \
  && cat files.txt | xargs sudo rm \
  && rm -f files.txt
```

Breve Lista de Recursos
------------------
* [Captura de hash PMKID](https://hashcat.net/forum/thread-7717.html) (ativada por padrão, force com: `--pmkid`)
* WPS Offline Brute-Force Attack também conhecido como "Pixie-Dust". (ativado por padrão, force com: `--wps-only --pixie`)
* WPS Online Brute-Force Attack também conhecido como "Ataque PIN". (ativado por padrão, force com: `--wps-only --no-pixie`)
* WPA/2 Offline Brute-Force Attack via captura de handshake de 4 vias (ativado por padrão, force com: `--no-wps`)
* Valida handshakes em relação a `pyrit`, `tshark`, `cowpatty`, e `aircrack-ng` (quando disponível)
* Vários ataques WEP (replay, chopchop, fragment, hirte, p0841, caffe-latte)
* Descobre automaticamente pontos de acesso ocultos durante a varredura ou ataque.
   * Nota: Só funciona quando o canal é fixo. Usar `-c <channel>`
   * Desabilite isso usando `--no-deauths`
* Suporte de 5Ghz para algumas placas wireless (via `-5` switch).
   * Nota: Algumas ferramentas não funcionam bem em canais de 5 GHz (por exemplo, `aireplay-ng`)
* Armazena senhas e handshakes quebrados no diretório atual (`--cracked`)
   * Inclui informações sobre o ponto de acesso quebrado (Nome, BSSID, Data, etc).
* Fácil de tentar quebrar handshakes ou hashes PMKID em uma lista de palavras (`--crack`)

O que há de novo?
-----------
Comparando este repositório com o "antigo wifite" @ https://github.com/derv82/wifite

* **Menos bugs**
   * Gestão de processos mais limpa. Não deixa processos rodando em segundo plano (o antigo `wifite` era ruim nisso).
   * Não mais "um roteiro monolítico". Tem testes de unidade de trabalho. Pull requests são menos dolorosos!
* **Velocidade**
   * Os pontos de acesso de destino são atualizados a cada segundo em vez de a cada 5 segundos.
* **Precisão**
   * Exibe o nível de potência em tempo real do alvo atualmente atacado.
   * Exibe mais informações durante um ataque (por exemplo, % durante ataques WEP chopchop, índice de passos Pixie-Dust, etc)
* **Educacional**
   * A `--verbose` opção (expansível para `-vv` ou `-vvv`) mostra quais comandos são executados e a saída desses comandos.
   * Isso pode ajudar a depurar por que o Wifite não está funcionando para você. Ou então você pode aprender como essas ferramentas são usadas.
* Mais ativamente desenvolvido.
* Suporte ao Python 3.
* Doce novo banner ASCII..

O que se foi?
------------
* Alguns argumentos de linha de comando (`--wept`, `--wpst`, e outras opções confusas).
   * Você ainda pode acessar algumas dessas opções obscuras, tente `wifite -h -v`

O que não é novo?
---------------
* (Principalmente) Retrocompatível com os `wifite` argumentos do original.
* A mesma interface baseada em texto que todos conhecem e amam.

Capturas de tela
-----------
Quebrando o PIN do WPS usando `reaver` o ataque Pixie-Dust e buscando a chave WPA usando `bully`:
![Pixie-Dust with Reaver to get PIN and Bully to get PSK](https://i.imgur.com/Q5KSDbg.gif)

-------------

Quebrando a chave WPA usando o ataque PMKID:
![PMKID attack](https://i.imgur.com/CR8oOp0.gif)

-------------

Decloaking e cracking de um ponto de acesso oculto (através do ataque WPA Handshake):
![Decloaking and Cracking a hidden access point](https://i.imgur.com/F6VPhbm.gif)

-------------

Quebrando uma senha WEP fraca (usando o ataque WEP Replay):
![Cracking a weak WEP password](https://i.imgur.com/jP72rVo.gif)

-------------

Quebrando um aperto de mão pré-capturado usando John The Ripper (através da opção `--crack`):
![--crack option](https://i.imgur.com/iHcfCjp.gif)
