import sublime
import sublime_plugin
import re
import urllib.request
import threading

class DeleteSpaceCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		for region in self.view.sel():
			s1 = self.view.substr(region)
			s2 = re.sub(r'\s+', '', s1)
			if s1 != s2:
				self.view.replace(edit, region, s2)

class TranslateCommand(sublime_plugin.TextCommand):
	def __init__(self, view):
		sublime_plugin.TextCommand.__init__(self, view)
		self.pattern = re.compile(r'<div class="trans-container">\s*(<ul>.*?</ul>)', re.DOTALL)

	def run(self, edit):
		selection = self.view.sel()
		if len(selection) > 0:
			region = selection[0]
			text = self.view.substr(region)
			thread = threading.Thread(target=self.translate, args=(text,))
			thread.start()

	def translate(self, text):
		url = 'http://dict.youdao.com/w/' + text
		req = urllib.request.Request(url)
		res = urllib.request.urlopen(req)
		content = res.read().decode('utf-8')
		start_index = 6000
		while start_index > 0:
			match = self.pattern.search(content[6000:])
			if match:
				result = match.group(1)
				self.view.show_popup(result, sublime.HIDE_ON_MOUSE_MOVE_AWAY, -1, 600, 400)
				return
			start_index -= 1000