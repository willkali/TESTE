# FAÇAM

Este arquivo é um braindump de ideias para melhorar o Wifite2 (ou prospectivo para "Wifite3")

------------------------------------------------------

### Melhor Tratamento de Dependências
Eu posso confiar em `pip` + `requirements.txt` para bibliotecas python, mas a maioria das dependências do wifite são programas instalados.

Quando uma dependência não é encontrada, o Wifite deve orientar o usuário durante a instalação de todas as dependências necessárias, e talvez as dependências opcionais também.

O passo a passo de instalação de dependência deve fornecer ou executar automaticamente os comandos de instalação (`git clone`, `wget | tar && ./config`, etc).

Como temos um script Python para cada dependência (sob `wifite/tools/` ou `wifite/util/`), usamos a herança múltipla do Python para conseguir isso.

Requisitos:

1. Uma classe de *dependência* básica
   * `@abstractmethods` para `exists()`, `name()`, `install()`, `print_install()`
2. Atualize todas as dependências para herdar a *dependência*
   * Substituir métodos abstratos
3. Verificador de dependência para ser executado na inicialização do Wifite.
   * Verifique se todas as dependências necessárias existem.
   * Se os deps necessários estiverem ausentes, solicite a instalação de todos (opcional + obrigatório) ou apenas o necessário, ou continue sem a instalação com aviso.
   * Se faltarem dependências opcionais, sugira `--install` sem avisar.
   * Caso contrário, continue em silêncio.

------------------------------------------------------

### Suporte a outras distribuições (não apenas Kali x86/64)

Em cima da minha cabeça:

* Raspberry Pi (ou qualquer distribuição Debian)
* Raspberry Pi + Kali (?)
* Kali Nethunter
* Várias outras distribuições (backbox, pentoo, blackarch, etc)

Descontinuação de programas "principais":

* `iwconfig` é descontinuada em favor de `iw`
* `ifconfig` é descontinuada em favor de `ip`

Problemas de versionamento:

* A saída do Pixiewps difere dependendo da versão
  * Da mesma forma para reaver & bully
* Os argumentos de Reaver e Bully mudaram significativamente ao longo dos anos (adicionado/removido/obrigatório)
* airodump-ng --write-interval=1 não funciona em versões mais antigas
  * O mesmo com with --wps e algumas outras opções :(
* saída airmon-ng é diferente, wifite vê "phy0" em vez do nome da interface.

Problemas diversos:

* Algumas pessoas têm problemas com várias placas wifi conectadas
  * Solução: Solicitação do usuário quando nenhum dispositivo estiver no modo monitor (pergunte primeiro).
* Algumas pessoas querem que o wifite mate o gerenciador de rede, outras não.
  * Solução: prompt do usuário para matar processos
* Algumas pessoas precisam --ignore-negative-one em algumas placas wifi.

------------------------------------------------------

### Argumentos de linha de comando

WWifite é um script 'Spray and Pray', 'Big Red Button'. O Wifite não deve fornecer opções obscuras que apenas usuários avançados possam entender. Usuários avançados podem simplesmente usar as dependências do Wifite diretamente.

--------------------------------

Cada opção no Wifite deve:

1. Afeta significativamente o comportamento do Wifite (por exemplo `pillage`, `5ghz`, '--no-wps', '--nodeauths')
2. Ou reduza a lista de alvos (por exemplo filtering --wps --wep --channel)
3. Ou defina algum sinalizador exigido por determinado hardware (pacotes por segundo)

Quaisquer opções que não se enquadrem nos buckets acima devem ser removidas.

--------------------------------

Atualmente, existem muitas opções de linha de comando:

* 8 opções para configurar um tempo limite em segundos (wpat, wpadt, pixiet, pixiest, wpst, wept, weprs, weprc)
  * Eu nem sei o que são ou se funcionam mais.
* 5 opções para configurar limites (WPS retry/fail/timeout, WEP pps/ivs)
  * E as opções WPS NÃO são consistentes entre Bully & Reaver.
* "Num deauths" etc

Para a maioria deles, podemos apenas definir um valor padrão sensato para evitar o `--help` Wall-of-Text.

--------------------------------

Os "Comandos" (`cracked`, `crack`, `check`) provavelmente não devem começar com `--`, por exemplo `--crack` devem ser simplesmente `crack`

------------------------------------------------------

### Implementações nativas do Python

Algumas dependências do Wifite (suite aircrack, tshark, etc) podem ser substituídas por implementações nativas do Python.

O *Scapy* permite ouvir e inspecionar pacotes, gravar arquivos pcap e outros recursos.

Existem maneiras de alterar canais sem fio, enumerar dispositivos sem fio, enviar pacotes Deauth, etc. tudo dentro do Python.

Ainda podemos utilizar bibliotecas quando é mais problemático do que vale a pena portar para Python, como alguns aircrack (chopchop, packetforge-ng).

E algumas implementações nativas do Python podem ser multiplataforma, o que permitiria...

------------------------------------------------------

### Suporte não Linux (OSX e Windows)

Algumas das dependências do Wifite funcionam em outros sistemas operacionais (airodump), mas outras não (airmon).

Se for possível executar esses programas no Windows ou OSX, o Wifite deve oferecer suporte a isso.

------------------------------------------------------

### Ataques WPS

A saída de status de ataque Pixie-Dust do Wifite difere entre Reaver e Bully. E as opções de linha de comando não são nem usadas pelo valentão?

Idealmente para Pixie-Dust, teríamos:

1. Alterne para definir o tempo limite de bully/reaver
2. Contadores idênticos entre bully/reaver (failures, timeouts, lockouts)
  * Não acho que os usuários devam poder definir limites de falha/tempo limite (sem opções).
3. Status idênticos entre bully/reaver.
  * Erros: "WPSFail", "Timeout", "NoAssoc", etc
  * Status: "Aguardando alvo", "Tentando PIN", "Enviando mensagem M2", "Executando pixiewps", etc.
  * "Passo X/Y" é bom, mas não totalmente preciso.
  * É estranho quando passamos de (6/8) para (5/8) sem explicação. E os 4 primeiros geralmente não são exibidos.
3. Temporizador de contagem regressiva até que o ataque seja abortado (por exemplo, 5min)
4. Temporizador de contagem regressiva no "tempo limite da etapa" (tempo desde o último status alterado, por exemplo, 30s)

Ordem de status:
1. Aguardando o farol
2. Associando ao destino
3. Tentando iniciar PIN / EAPOL / resposta de identidade / M1,M2 (M3,M4)
4. pixiewps em execução
5. Rachado ou Falhado

E quanto à quebra de PIN .. hum .. Nem tenho certeza de que isso deve ser uma opção no Wifite TBH. A quebra do PIN leva dias e a maioria
dos APs bloqueia automaticamente após 3 tentativas. Ataques de vários dias (possivelmente de vários meses) não são uma boa opção para o
Wifite. Usuários com esse tipo de dedicação podem executar o bullying/reaver eles mesmos.

------------------------------------------------------

### Estrutura de diretórios

**Nota: Isso foi feito principalmente na grande refatoração do final de março de 2018**

Muito modular em alguns lugares, não modular o suficiente em outros.

Não "/py":

* **aircrack/**
  * `aircrack.py` <- processo
  * `airmon.py` <- processo
  * `airodump.py` <- processo
  * `aireplay.py` <- processo
* **attack/**
  * `decloak.py` <- aireplay, airodump
  * `wps-pin.py` <- reaver, bully
  * `wps-pixie.py` <- reaver, bully
  * `wpa.py` (handshake only)  <- aireplay, airodump
  * `wep.py` (relay, chopchop) <- aireplay, airodump
* `config.py`
* **crack/**
  * `crackwep.py` <- alvo, result, aireplay, aircrack
  * `crackwpa.py` <- alvo, handshake, result, aircrack
* **handshake/**
  * `tshark.py` <- processo
  * `cowpatty.py` <- processo
  * `pyrit.py` <- processo
  * `handshake.py` <- tshark, cowpatty, pyrit, aircrack
* `output.py` (cor/impressão) <- configuração
* `process.py` <- configuração
* `scan.py` (saída do airodump para o destino) <- configuração, alvo, airodump
* **target/**
  * `target.py` (ssid, pcap file) <- airodump, tshark
  * `result.py` (PIN/PSK/KEY)

------------------------------------------------------

### Injeção de dependência

* Inicialize cada dependência na inicialização ou quando possível.
* Passe dependências para módulos que as requerem.
  * Módulos que chamam aircrack esperam aircrack.py
  * Módulos que imprimem esperam output.py
* Teste de unidade usando dependências simuladas.

------------------------------------------------------

### Dependências

**AIRMON**

* Detectar interfaces no modo monitor.
* Verifique se o nome da interface de configuração foi encontrado.
* Ative ou desative o modo de monitor em um dispositivo.

**AIRODUMP**
* Executar como daemon (thread em segundo plano)
* Aceite sinalizadores como entrada (--ivs, --wps, etc)
* Construa um alvo para todos os APs encontrados
  * Cada Alvo inclui uma lista de Clientes associados
  * Pode analisar CSV para encontrar linhas com APs e linhas com Clientes
  * Opção para ler de 1) Stdout ou 2) um CapFile
* Identifique os atributos do Alvo: ESSID, BSSID, AUTH
* Identificar alvos camuflados (ESSID=null)
* Retornar lista filtrada de destinos com base em AUTH, ESSID, BSSID
* XXX: A leitura de STDOUT pode não corresponder ao que está no arquivo Cap...
* XXX: Mas STDOUT nos dá WPS e evita WASH...

**TARGET**
* Construído via CSV passado (airodump-ng --output-format=csv)
  * Precisa de informações sobre o AP atual (1 linha) e TODOS os clientes (n linhas)
* Acompanhe BSSID, ESSID, Canal, AUTH, outros attrs
* Construir clientes de destino
* Inicie e retorne um Airodump Daemon (por exemplo, WEP precisa de --ivs sinalizador)

**AIREPLAY**
* Fakeauth
  * (Daemon) Inicie o processo de autenticação falsa
  * Detectar o status do fakeauth
  * Finalizar o processo de autenticação falsa
* Deauth
  * Chame aireplay-ng para desautenticar um cliente BSSID+ESSID
  * Status de retorno de deauth
* Chopchop & Fragment
  1. (Daemon) Inicie aireplay-ng --chopchop ou --fragment no Target
  2. LOOP
    1. Detectar status de chopchop/fragment (.xor ou EXCEPTION)
    2. Se .xor for criado:
      * Chame packetforge-ng para forjar cap
      * Arpreplay em forged cap
    3. Se o tempo de execução > limite, EXCEÇÃO
* Arpreplay
  1. (Daemon) Inicie o aireplay-ng para reproduzir um determinado capfile
  2. Detectar o status do replay (# de pacotes)
  3. Se o tempo de execução > limite e/ou velocidade do pacote < limite, EXCEÇÃO

**AIRCRACK**
* Iniciar aircrack-ng para WEP: precisa de arquivo pcap com IVS
* Iniciar aircrack-ng para WPA: Precisa de arquivo pcap contendo Handshake
* Verifique o status do aircrack-ng (`percenage`, `keys-tried`)
* Devolver chave quebrada

**CONFIG**
* Armazenamentos de chave/valor: 1) padrões e 2) definidos pelo cliente
* Lê de argumentos de linha de comando (+validação de entrada)
* Chaves para filtrar alvos verificados por algum atributo
  * Filtrar por AUTH: --wep, --wpa
  * Filtrar por WPS: --wps
  * Filtrar por canal: --channel
  * Filtrar por bssid: --bssid
  * Filtrar por essid: --essid
* Chaves para especificar ataques
  * WEP: arp-replay, chopchop, fragmentation, etc
  * WPA: Apenas aperto de mão?
  * WPS: pin, pixie-dust
* Chaves para especificar limites (tempo de execução, tempos limite)
Chave para especificar o comando a ser executado:
  * SCAN (padrão), CRACK, INFO

------------------------------------------------------

### Fluxo de trabalho do processo

**PRINCIPAL**: Inicia tudo
1. Analisar argumentos de linha de comando, substituir padrões
2. Inicie o COMANDO apropriado (SCAN, ATTACK, CRACK, INFO)

**SCAN**: (Scan + Ataque + Resultado)
1. Encontre a interface, inicie o modo monitor (airmon.py)
2. CICLO
   1. Obter lista de destinos filtrados (airodump.py)
     * Opção: Leia do CSV a cada segundo ou analise o airodump STDOUT
   2. Desclamufar SSIDs se possivel (decloak.py)
   3. Classificar alvos; Prefira WEP sobre WPS sobre WPA (1+ clientes) sobre WPA (sem cliente)
   4. Imprimir destinos para tela (ESSID, Canal, Energia, WPS, # de clientes)
   5. Imprimir ESSIDs sem camuflagem (se houver)
   6. Aguarde 5 segundos ou até que o usuário interrompa
3. Solicitar ao usuário que selecione o alvo ou intervalo de alvos
4. PARA CADA alvo:
   1. Destino de ATAQUE baseado em CONFIG (WEP/WPA/WPS)
   2. Imprimir status do ataque (crackeado ou erro)
   3. Somente WPA: comece a quebrar o Handshake
   4. Se estiver quebrado, teste as credenciais conectando-se ao roteador (?).

**ATTACK** (Todos os tipos)
Retorna informações de alvo quebradas ou lança exceção

**ATTACK WEP**:
0. Espera: Alvo
1. Inicie o Airodump para capturar IVS do AP (airodump)
2. CICLO
   1. (Daemon) Fakeauth com AP se necessário (aireplay, config)
   2. (Daemon?) Execute o ataque WEP apropriado (aireplay, packetforge)
   3. Se airodump IVS > limite:
      1. (Daemon) Se o daemon Aircrack não estiver em execução, inicie-o. (aéreo)
      2. Se for bem-sucedido, adicione a senha ao Target e retorne.
   4. Se aireplay/others e IVS não mudaram em N segundos, reinicie o ataque.
   5. Se o tempo de execução > limite, EXCEÇÃO

**ATTACK WPA**: Retorna alvo quebrado ou handshake de alvo
0. Espera: alvo
1. Inicie o Airodump para capturar o PCAP do AP de destino
2. CICLO
   1. Obter lista de todos os Clientes associados, adicionar "*BROADCAST*"
   2. (Daemon) Deauth um único cliente na lista.
   3. Status de impressão (tempo restante, clientes, deauths enviados)
   4. Copie o PCAP e verifique o Handshake
   5. Se o handshake for encontrado, salve em ./hs/ e BREAK
   6. Se o tempo de execução > limite, EXCEÇÃO
3. (Daemon) Se o Config tiver uma lista de palavras, tente crackear handshake (airodump)
   1. Se for bem-sucedido, adicione PSK ao destino e retorne
4. Se não rachar ou o crack não for bem sucedido, marque PSK como "Handshake" e retorne

**ATTACK WPS**
0. Espera: Alvo
1. Para cada ataque (PIN e/ou Pixie-Dust baseado em CONFIG):
   1. (Daemon) Iniciar Reaver/Bully (PIN/Pixie-Dust)
   2. CICLO
      1. Imprimir status do Pixie
      2. Se o Pixie for bem-sucedido, adicione PSK+PIN ao Alvo e retorne
      3. Se as falhas do Pixie > limite, EXCEÇÃO
      4. Se o Pixie estiver bloqueado == CONFIG, EXCEPTION
      5. Se o tempo de execução > limite, EXCEÇÃO

**CRACK WEP**
0. Espera: String pcap arquivo contendo IVS
1. PARA CADA opção de Aircrack:
   1. (Daemon) Iniciar Aircrack
   2. CILCO
      1. Imprimir status do Aircrack
      2. Se o Aircrack for bem sucedido, imprima o resultado
      3. Se não tiver sucesso, EXCEÇÃO

**CRACK WPA**
0. Espera: Arquivo pcap de string contendo Handshake (opcional: BSSID/ESSID)
1. Selecione a opção Cracking (Aircrack, Cowpatty, Pyrit)
2. (Daemon) Iniciar ataque
3. CICLO
   1. Print attack status if possible
   2. Se for bem sucedido, imprima o resultado
   3. Se não tiver sucesso, EXCEÇÃO

**INFORMAÇÕES**
* Imprima a lista de arquivos de handshake com ESSIDs, datas, etc.
  * Mostrar opções para `--crack` handshakes (ou executar esses comandos diretamente)
* Imprimir lista de alvos quebrados (incluindo chave WEP/WPA/WPS)

------------------------------------------------------
