#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from .config import Configuration
except (ValueError, ImportError) as e:
    raise Exception('Você pode precisar executar wifite a partir do diretório raiz (que inclui README.md)', e)

from .util.color import Color

import os
import sys


class Wifite(object):

    def __init__(self):
        '''
        Inicializa o Wifite. Verifica as permissões de root e garante que as dependências sejam instaladas.
        '''

        self.print_banner()

        Configuration.initialize(load_interface=False)

        if os.getuid() != 0:
            Color.pl('{!} {R}erro: {O}wifite{R} deve ser executado como {O}root{W}')
            Color.pl('{!} {R}rexecutar novamente com {O}sudo{W}')
            Configuration.exit_gracefully(0)

        from .tools.dependency import Dependency
        Dependency.run_dependency_check()


    def start(self):
        '''
        Inicia a varredura de destino + loop de ataque ou inicia utilitários dependendo da entrada do usuário.
        '''
        from .model.result import CrackResult
        from .model.handshake import Handshake
        from .util.crack import CrackHelper

        if Configuration.show_cracked:
            CrackResult.display()

        elif Configuration.check_handshake:
            Handshake.check()

        elif Configuration.crack_handshake:
            CrackHelper.run()

        else:
            Configuration.get_monitor_mode_interface()
            self.scan_and_attack()


    def print_banner(self):
        '''Exibe arte ASCII do mais alto calibre.'''
        Color.pl(r' {G}  .     {GR}{D}     {W}{G}     .    {W}')
        Color.pl(r' {G}.´  ·  .{GR}{D}     {W}{G}.  ·  `.  {G}wifite {D}%s{W}' % Configuration.version)
        Color.pl(r' {G}:  :  : {GR}{D} (¯) {W}{G} :  :  :  {W}{D}auditor sem fio automatizado{W}')
        Color.pl(r' {G}`.  ·  `{GR}{D} /¯\ {W}{G}´  ·  .´  {C}{D}https://github.com/derv82/wifite2{W}')
        Color.pl(r' {G}  `     {GR}{D}/¯¯¯\{W}{G}     ´    {W}')
        Color.pl('')


    def scan_and_attack(self):
        '''
        1) Procura alvos, pede ao usuário para selecionar alvos
        2) Ataca cada alvo
        '''
        from .util.scanner import Scanner
        from .attack.all import AttackAll

        Color.pl('')

        # Scan
        s = Scanner()
        targets = s.select_targets()

        # Attack
        attacked_targets = AttackAll.attack_multiple(targets)

        Color.pl('{+} Ataque finalizado {C}%d{W} alvo(s), saindo' % attacked_targets)


##############################################################


def entry_point():
    try:
        wifite = Wifite()
        wifite.start()
    except Exception as e:
        Color.pexception(e)
        Color.pl('\n{!} {R}saindo{W}\n')

    except KeyboardInterrupt:
        Color.pl('\n{!} {O}Interrompido, Desligando...{W}')

    Configuration.exit_gracefully(0)


if __name__ == '__Principal__':
    entry_point()
