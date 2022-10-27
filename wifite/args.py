#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .util.color import Color

import argparse, sys

class Arguments(object):
    ''' Mantém os argumentos usados pelo Wifite '''

    def __init__(self, configuration):
        # Hack: Verifique se há -v antes de analisar argumentos; para que possamos saber quais comandos exibir.
        self.verbose = '-v' in sys.argv or '-hv' in sys.argv or '-vh' in sys.argv
        self.config = configuration
        self.args = self.get_arguments()

    def _verbose(self, msg):
        if self.verbose:
            return Color.s(msg)
        else:
            return argparse.SUPPRESS

    def get_arguments(self):
        ''' Retorna parser.args() contendo todos os argumentos do programa '''

        parser = argparse.ArgumentParser(usage=argparse.SUPPRESS,
                formatter_class=lambda prog: argparse.HelpFormatter(
                    prog, max_help_position=80, width=130))

        self._add_global_args(parser.add_argument_group(Color.s('{C}DEFINIÇÕES{W}')))
        self._add_wep_args(parser.add_argument_group(Color.s('{C}WEP{W}')))
        self._add_wpa_args(parser.add_argument_group(Color.s('{C}WPA{W}')))
        self._add_wps_args(parser.add_argument_group(Color.s('{C}WPS{W}')))
        self._add_pmkid_args(parser.add_argument_group(Color.s('{C}PMKID{W}')))
        self._add_eviltwin_args(parser.add_argument_group(Color.s('{C}GEMEO MAU{W}')))
        self._add_command_args(parser.add_argument_group(Color.s('{C}COMANDOS{W}')))

        return parser.parse_args()


    def _add_global_args(self, glob):
        glob.add_argument('-v',
            '--verbose',
            action='contar',
            default=0,
            dest='verbose',
            help=Color.s('Mostra mais opções ({C}-h -v{W}). Imprime comandos e ' +
                'saídas. (predefinição: {G}tranquilo{W})'))

        glob.add_argument('-i',
            action='store',
            dest='interface',
            metavar='[interface]',
            type=str,
            help=Color.s('Wireless interface to use, e.g. {C}wlan0mon{W} ' +
                '(default: {G}ask{W})'))

        glob.add_argument('-c',
            action='armazenar',
            dest='canal',
            metavar='[canal]',
            type=int,
            help=Color.s('Canal sem fio para escanear (predefinição: {G}todos os canais de 2Ghz{W})'))
        glob.add_argument('--channel', help=argparse.SUPPRESS, action='store',
                dest='canal', type=int)

        glob.add_argument('-5',
            '--5ghz',
            action='armazenar_verdade',
            dest='5ghz',
            help=self._verbose('Incluir canais de 5GHz (predefinição: {G}desligado{W})'))


        glob.add_argument('-mac',
            '--mac-aleatorio',
            action='armazenar_verdade',
            dest='mac-aleatorio',
            help=Color.s('Randomizar o endereço MAC do cartão sem fio (predefinição: {G}desligado{W})'))

        glob.add_argument('-p',
            action='armazenar',
            dest='armazenar_tempo',
            nargs='?',
            const=10,
            metavar='tempo_de_arredura',
            type=int,
            help=Color.s('{G}Pilhagem{W}: Ataque todos os alvos após ' +
                '{C}tempo_de_arredura{W} (segundos)'))
        glob.add_argument('--pillage', help=argparse.SUPPRESS, action='armazenar',
                dest='tempo_de_arredura', nargs='?', const=10, type=int)

        glob.add_argument('--kill',
            action='armazenar_verdade',
            dest='matar_processos_conflitantes',
            help=Color.s('Matar processos que entram em conflito com Airmon/Airodump ' +
                '(predefinição: {G}desligado{W})'))

        glob.add_argument('-b',
            action='armazenar',
            dest='alvo_bssid',
            metavar='[bssid]',
            type=str,
            help=self._verbose('BSSID (por exemplo. {GR}AA:BB:CC:DD:EE:FF{W}) de ponto ' +
                'de acesso para atacar'))
        glob.add_argument('--bssid', help=argparse.SUPPRESS, action='armazenar',
                dest='alvo_bssid', type=str)

        glob.add_argument('-e',
            action='armazenar',
            dest='alvo_essid',
            metavar='[essid]',
            type=str,
            help=self._verbose('ESSID (por exemplo. {GR}NETGEAR07{W}) de ponto de acesso para atacar'))
        glob.add_argument('--essid', help=argparse.SUPPRESS, action='armazenar',
                dest='alvo_essid', type=str)

        glob.add_argument('-E',
            action='armazenar',
            dest='ignorar_essid',
            metavar='[texto]',
            type=str,
            default=None,
            help=self._verbose('Oculta destinos com ESSIDs que correspondem ao texto fornecido'))
        glob.add_argument('--ignore-essid', help=argparse.SUPPRESS, action='armazenar',
                dest='ignorar_essid', type=str)

        glob.add_argument('--clients-only',
            action='armazenar_verdade',
            dest='somente para clientes',
            help=Color.s('Mostrar apenas destinos que tenham clientes associados ' +
                '(predefinição: {G}desligado{W})'))

        glob.add_argument('--showb',
            action='armazenar_verdade',
            dest='mostrar_bssids',
            help=self._verbose('Mostrar BSSIDs de alvos durante a varredura'))

        glob.add_argument('--nodeauths',
            action='armazenar_verdade',
            dest='no_deauth',
            help=Color.s('Passive mode: Never deauthenticates clients ' +
                '(default: {G}deauth targets{W})'))
        glob.add_argument('--no-deauths', action='armazenar_verdade', dest='no_deauth',
                help=argparse.SUPPRESS)
        glob.add_argument('-nd',          action='armazenar_verdade', dest='no_deauth',
                help=argparse.SUPPRESS)

        glob.add_argument('--num-deauths',
            action='store',
            type=int,
            dest='num_deauths',
            metavar='[num]',
            default=None,
            help=self._verbose('Number of deauth packets to send (default: ' +
                '{G}%d{W})' % self.config.num_deauths))


    def _add_eviltwin_args(self, group):
        pass
        '''
        group.add_argument('--eviltwin',
            action='store_true',
            dest='use_eviltwin',
            help=Color.s('Use the "Evil Twin" attack against all targets ' +
                '(default: {G}off{W})'))
        # TODO: Args to specify deauth interface, server port, etc.
        '''


    def _add_wep_args(self, wep):
        # WEP
        wep.add_argument('--wep',
            action='store_true',
            dest='wep_filter',
            help=Color.s('Show only {C}WEP-encrypted networks{W}'))
        wep.add_argument('-wep', help=argparse.SUPPRESS, action='store_true',
                dest='wep_filter')

        wep.add_argument('--require-fakeauth',
            action='store_true',
            dest='require_fakeauth',
            help=Color.s('Fails attacks if {C}fake-auth{W} fails (default: {G}off{W})'))
        wep.add_argument('--nofakeauth', help=argparse.SUPPRESS, action='store_true',
                dest='require_fakeauth')
        wep.add_argument('-nofakeauth', help=argparse.SUPPRESS, action='store_true',
                dest='require_fakeauth')

        wep.add_argument('--keep-ivs',
            action='store_true',
            dest='wep_keep_ivs',
            default=False,
            help=Color.s('Retain .IVS files and reuse when cracking ' +
                '(default: {G}off{W})'))

        wep.add_argument('--pps',
            action='store',
            dest='wep_pps',
            metavar='[pps]',
            type=int,
            help=self._verbose('Packets-per-second to replay (default: ' +
                '{G}%d pps{W})' % self.config.wep_pps))
        wep.add_argument('-pps', help=argparse.SUPPRESS, action='store',
                dest='wep_pps', type=int)

        wep.add_argument('--wept',
            action='store',
            dest='wep_timeout',
            metavar='[seconds]',
            type=int,
            help=self._verbose('Seconds to wait before failing (default: ' +
                '{G}%d sec{W})' % self.config.wep_timeout))
        wep.add_argument('-wept', help=argparse.SUPPRESS, action='store',
                dest='wep_timeout', type=int)

        wep.add_argument('--wepca',
            action='store',
            dest='wep_crack_at_ivs',
            metavar='[ivs]',
            type=int,
            help=self._verbose('Start cracking at this many IVs (default: ' +
                '{G}%d ivs{W})' % self.config.wep_crack_at_ivs))
        wep.add_argument('-wepca', help=argparse.SUPPRESS, action='store',
                dest='wep_crack_at_ivs', type=int)

        wep.add_argument('--weprs',
            action='store',
            dest='wep_restart_stale_ivs',
            metavar='[seconds]',
            type=int,
            help=self._verbose('Restart aireplay if no new IVs appear (default: ' +
                '{G}%d sec{W})' % self.config.wep_restart_stale_ivs))
        wep.add_argument('-weprs', help=argparse.SUPPRESS, action='store',
                dest='wep_restart_stale_ivs', type=int)

        wep.add_argument('--weprc',
            action='store',
            dest='wep_restart_aircrack',
            metavar='[seconds]',
            type=int,
            help=self._verbose('Restart aircrack after this delay (default: ' +
                '{G}%d sec{W})' % self.config.wep_restart_aircrack))
        wep.add_argument('-weprc', help=argparse.SUPPRESS, action='store',
                dest='wep_restart_aircrack', type=int)

        wep.add_argument('--arpreplay',
            action='store_true',
            dest='wep_attack_replay',
            help=self._verbose('Use {C}ARP-replay{W} WEP attack (default: {G}on{W})'))
        wep.add_argument('-arpreplay', help=argparse.SUPPRESS, action='store_true',
                dest='wep_attack_replay')

        wep.add_argument('--fragment',
            action='store_true',
            dest='wep_attack_fragment',
            help=self._verbose('Use {C}fragmentation{W} WEP attack (default: {G}on{W})'))
        wep.add_argument('-fragment', help=argparse.SUPPRESS, action='store_true',
                dest='wep_attack_fragment')

        wep.add_argument('--chopchop',
            action='store_true',
            dest='wep_attack_chopchop',
            help=self._verbose('Use {C}chop-chop{W} WEP attack (default: {G}on{W})'))
        wep.add_argument('-chopchop', help=argparse.SUPPRESS, action='store_true',
                dest='wep_attack_chopchop')

        wep.add_argument('--caffelatte',
            action='store_true',
            dest='wep_attack_caffe',
            help=self._verbose('Use {C}caffe-latte{W} WEP attack (default: {G}on{W})'))
        wep.add_argument('-caffelatte', help=argparse.SUPPRESS, action='store_true',
                dest='wep_attack_caffelatte')

        wep.add_argument('--p0841',
            action='store_true',
            dest='wep_attack_p0841',
            help=self._verbose('Use {C}p0841{W} WEP attack (default: {G}on{W})'))
        wep.add_argument('-p0841', help=argparse.SUPPRESS, action='store_true',
                dest='wep_attack_p0841')

        wep.add_argument('--hirte',
            action='store_true',
            dest='wep_attack_hirte',
            help=self._verbose('Use {C}hirte{W} WEP attack (default: {G}on{W})'))
        wep.add_argument('-hirte', help=argparse.SUPPRESS, action='store_true',
                dest='wep_attack_hirte')


    def _add_wpa_args(self, wpa):
        wpa.add_argument('--wpa',
            action='store_true',
            dest='wpa_filter',
            help=Color.s('Show only {C}WPA-encrypted networks{W} (includes {C}WPS{W})'))
        wpa.add_argument('-wpa', help=argparse.SUPPRESS, action='store_true',
                dest='wpa_filter')

        wpa.add_argument('--hs-dir',
            action='store',
            dest='wpa_handshake_dir',
            metavar='[dir]',
            type=str,
            help=self._verbose('Directory to store handshake files ' +
                '(default: {G}%s{W})' % self.config.wpa_handshake_dir))
        wpa.add_argument('-hs-dir', help=argparse.SUPPRESS, action='store',
                dest='wpa_handshake_dir', type=str)

        wpa.add_argument('--new-hs',
            action='store_true',
            dest='ignore_old_handshakes',
            help=Color.s('Captures new handshakes, ignores existing handshakes ' +
                'in {C}%s{W} (default: {G}off{W})' % self.config.wpa_handshake_dir))

        wpa.add_argument('--dict',
            action='store',
            dest='wordlist',
            metavar='[file]',
            type=str,
            help=Color.s('File containing passwords for cracking (default: {G}%s{W})')
                % self.config.wordlist)

        wpa.add_argument('--wpadt',
            action='store',
            dest='wpa_deauth_timeout',
            metavar='[seconds]',
            type=int,
            help=self._verbose('Time to wait between sending Deauths ' +
                '(default: {G}%d sec{W})' % self.config.wpa_deauth_timeout))
        wpa.add_argument('-wpadt', help=argparse.SUPPRESS, action='store',
                dest='wpa_deauth_timeout', type=int)

        wpa.add_argument('--wpat',
            action='store',
            dest='wpa_attack_timeout',
            metavar='[seconds]',
            type=int,
            help=self._verbose('Time to wait before failing WPA attack ' +
                '(default: {G}%d sec{W})' % self.config.wpa_attack_timeout))
        wpa.add_argument('-wpat', help=argparse.SUPPRESS, action='store',
                dest='wpa_attack_timeout', type=int)

        # TODO: Uncomment the --strip option once it works
        '''
        wpa.add_argument('--strip',
            action='store_true',
            dest='wpa_strip_handshake',
            default=False,
            help=Color.s('Strip unnecessary packets from handshake capture using tshark'))
        '''
        wpa.add_argument('-strip', help=argparse.SUPPRESS, action='store_true',
                dest='wpa_strip_handshake')


    def _add_wps_args(self, wps):
        wps.add_argument('--wps',
            action='store_true',
            dest='wps_filter',
            help=Color.s('Show only {C}WPS-enabled networks{W}'))
        wps.add_argument('-wps', help=argparse.SUPPRESS, action='store_true',
                dest='wps_filter')

        wps.add_argument('--no-wps',
            action='store_true',
            dest='no_wps',
            help=self._verbose('{O}Never{W} use {O}WPS PIN{W} & {O}Pixie-Dust{W}' +
                'attacks on targets (default: {G}off{W})'))

        wps.add_argument('--wps-only',
            action='store_true',
            dest='wps_only',
            help=Color.s('{O}Only{W} use {C}WPS PIN{W} & {C}Pixie-Dust{W} ' +
                'attacks (default: {G}off{W})'))

        wps.add_argument('--pixie',    action='store_true', dest='wps_pixie',
            help=self._verbose('{O}Only{W} use {C}WPS Pixie-Dust{W} attack ' +
                '(do not use {O}PIN attack{W})'))

        wps.add_argument('--no-pixie', action='store_true', dest='wps_no_pixie',
            help=self._verbose('{O}Never{W} use {O}WPS Pixie-Dust{W} attack ' +
                '(use {G}PIN attack{W})'))

        wps.add_argument('--bully',
            action='store_true',
            dest='use_bully',
            help=Color.s('Use {G}bully{W} program for WPS PIN & Pixie-Dust attacks ' +
                '(default: {G}reaver{W})'))
        # Alias
        wps.add_argument('-bully', help=argparse.SUPPRESS, action='store_true',
                dest='use_bully')

        # Ignore lock-outs
        wps.add_argument('--ignore-locks', action='store_true', dest='wps_ignore_lock',
            help=Color.s('Do {O}not{W} stop WPS PIN attack if AP becomes {O}locked{W} ' +
                ' (default: {G}stop{W})'))

        # Time limit on entire attack.
        wps.add_argument('--wps-time',
            action='store',
            dest='wps_pixie_timeout',
            metavar='[sec]',
            type=int,
            help=self._verbose('Total time to wait before failing PixieDust attack ' +
                '(default: {G}%d sec{W})' % self.config.wps_pixie_timeout))
        # Alias
        wps.add_argument('-wpst', help=argparse.SUPPRESS, action='store',
                dest='wps_pixie_timeout', type=int)

        # Maximum number of 'failures' (WPSFail)
        wps.add_argument('--wps-fails',
            action='store',
            dest='wps_fail_threshold',
            metavar='[num]',
            type=int,
            help=self._verbose('Maximum number of WPSFail/NoAssoc errors before ' +
                'failing (default: {G}%d{W})' % self.config.wps_fail_threshold))
        # Alias
        wps.add_argument('-wpsf', help=argparse.SUPPRESS, action='store',
                dest='wps_fail_threshold', type=int)

        # Maximum number of 'timeouts'
        wps.add_argument('--wps-timeouts',
            action='store',
            dest='wps_timeout_threshold',
            metavar='[num]',
            type=int,
            help=self._verbose('Maximum number of Timeouts before failing ' +
                '(default: {G}%d{W})' % self.config.wps_timeout_threshold))
        # Alias
        wps.add_argument('-wpsto', help=argparse.SUPPRESS, action='store',
                dest='wps_timeout_threshold', type=int)

    def _add_pmkid_args(self, pmkid):
        pmkid.add_argument('--pmkid',
                         action='store_true',
                         dest='use_pmkid_only',
                         help=Color.s('{O}Only{W} use {C}PMKID capture{W}, avoids other WPS & ' +
                                      'WPA attacks (default: {G}off{W})'))
        # Alias
        pmkid.add_argument('-pmkid', help=argparse.SUPPRESS, action='store_true', dest='use_pmkid_only')

        pmkid.add_argument('--pmkid-timeout',
                         action='store',
                         dest='pmkid_timeout',
                         metavar='[sec]',
                         type=int,
                         help=Color.s('Time to wait for PMKID capture ' +
                                      '(default: {G}%d{W} seconds)' % self.config.pmkid_timeout))

    def _add_command_args(self, commands):
        commands.add_argument('--cracked',
            action='store_true',
            dest='cracked',
            help=Color.s('Print previously-cracked access points'))
        commands.add_argument('-cracked', help=argparse.SUPPRESS, action='store_true',
                dest='cracked')

        commands.add_argument('--check',
            action='store',
            metavar='file',
            nargs='?',
            const='<all>',
            dest='check_handshake',
            help=Color.s('Check a {C}.cap file{W} (or all {C}hs/*.cap{W} files) ' +
                'for WPA handshakes'))
        commands.add_argument('-check', help=argparse.SUPPRESS, action='store',
                nargs='?', const='<all>', dest='check_handshake')

        commands.add_argument('--crack',
            action='store_true',
            dest='crack_handshake',
            help=Color.s('Show commands to crack a captured handshake'))

if __name__ == '__main__':
    from .util.color import Color
    from .config import Configuration
    Configuration.initialize(False)
    a = Arguments(Configuration)
    args = a.args
    for (key,value) in sorted(args.__dict__.items()):
        Color.pl('{C}%s: {G}%s{W}' % (key.ljust(21),value))

