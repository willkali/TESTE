#!/usr/bin/env python

# Nota: Este script executa o Wifite de dentro de um repositório git clonado.
# O script `bin/wifite` foi projetado para ser executado após a instalação (de /usr/sbin), não do cwd.

from wifite import __main__
__main__.entry_point()
