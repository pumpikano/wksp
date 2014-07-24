#!/usr/bin/env python

from subprocess import Popen, PIPE, call as sp_call
from time import sleep
import sys
import json
import os

TERMINAL_OSA = """
tell application "Terminal"
   activate
   tell window 1
      do script "sleep 5; exit"
      set background color to {0, 11111, 11111}
      set win_id to id
   end tell

   set w_ids to (id of every window)

   repeat while w_ids contains win_id
     delay 1
     set w_ids to (id of every window)
   end repeat
end tell
"""

DEFAULT_COLOR = '#472E21'
DEFAULT_OPACITY = '80'

OSA_TERMINAL_ACTIVATE = 'tell application "Terminal" to activate'
OSA_TERMINAL_NEW_WINDOW = 'tell application "System Events" to tell process "Terminal" to keystroke "n" using {command down}'
OSA_TERMINAL_NEW_TAB = 'tell application "System Events" to tell process "Terminal" to keystroke "t" using {command down}'
OSA_SET_COLOR = 'tell application "Terminal" to tell window 1 to set background color to %s'
OSA_DO_SCRIPT =  'tell application "Terminal" to do script "%s" in tab %d of window 1'

def hex_color_to_osa_color(hex_color):
	hex_color = hex_color.replace('#', '')

	r = int(float(int(hex_color[0:2], 16)) / 2**8 * 2**16)
	g = int(float(int(hex_color[2:4], 16)) / 2**8 * 2**16)
	b = int(float(int(hex_color[4:6], 16)) / 2**8 * 2**16)

	return '{%d,%d,%d}' % (r,g,b)


def open_terminal_tabs(headed):

	tab_list = headed['tabs']
	if not len(tab_list):
		return

	# Commands to open new window and required tabs with particular color
	osa_cmds = [OSA_TERMINAL_ACTIVATE]
	# osa_cmds += [OSA_TERMINAL_NEW_WINDOW]
	osa_cmds += [OSA_SET_COLOR % (hex_color_to_osa_color(headed['color'] if 'color' in headed else DEFAULT_COLOR))]
	osa_cmds += [OSA_TERMINAL_NEW_TAB for x in range(len(tab_list) - 1)]

	# Execute commands in appropriate tabs
	for i, tab in enumerate(tab_list):
		for tab_cmd in tab['commands']:
			osa_cmds += [OSA_DO_SCRIPT % (' '.join(tab_cmd), i + 1)]

	osa_cmds = "\n".join(osa_cmds)

	# print osa_cmds

	p = Popen(['osascript', '-'], stdin=PIPE)
	p.communicate(input=osa_cmds)

if __name__ == '__main__':

	proj_name = sys.argv[1]
	if not proj_name:
		print 'Please project a project name to open'
		exit(1)

	proj_dir = sys.argv[2]

	filepath = os.path.join(proj_dir, proj_name + '.json')
	if not os.path.isfile(filepath):
		print 'File %s not present' % (filepath)
		exit(1)

	f = open(filepath, 'r')
	proj_data = json.load(f)

	open_terminal_tabs(proj_data['headed'])
	
	for cmd in proj_data['headless']['commands']:
		sp_call(cmd)


