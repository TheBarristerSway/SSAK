import os, pwd, sys, re, urlparse, time, fcntl, struct
from gi.repository import Gtk, GObject
from subprocess import Popen, PIPE

home = pwd.getpwuid(os.getuid()).pw_dir + '/SSAK/'
execdir = os.path.dirname(os.path.realpath(sys.argv[0]))

class steghide:
	
	def stegembed(self, widget):
		compress = ("OFF", "ON")[self.checkcompress.get_active()]
		sumit = ("OFF", "ON")[self.checksum.get_active()]
		nameit = ("OFF", "ON")[self.checkname.get_active()]
		self.enc = (self.enctype.get_active_text())
		self.hpass = self.steghpass.get_text()
		self.steghchooser.connect("delete-event", lambda window, event: self.steghchooser.destroy() or True)
		self.steghidefile = str(self.steghchooser.get_filename())
		self.sfile = self.file.get_text()
		options = " -f "
		if compress == "OFF":
			options += " -Z "
		if sumit == "OFF":
			options += " -K "
		if nameit == "OFF":
			options += " -N "
		encryption = ""
		if self.steghidefile != "None" and self.sfile != "":
			if self.enc == "none":
				encryption = " -e none"
			else:
				if self.enc == "wake" or self.enc == "arcfour" or self.enc == "enigma":
					encryption = " -e " + self.enc + " stream "
				else:
					encryption = " -e " + self.enc + " cbc "
			head, tail = os.path.split(self.sfile)
			outdir = home + tail + '/steghide_embed'
			self.outfile2 = outdir + '/' + tail
			if not os.path.isdir(outdir):
				os.mkdir(outdir)
			cmd = re.escape(execdir) + "/programs/" + self.arch +"/steghide --embed -ef " + re.escape(self.steghidefile) + options + encryption + " -cf " + re.escape(self.sfile) + " -sf " + re.escape(self.outfile2) + " -p '" + self.hpass + "'"
			proc = Popen(cmd, shell=True, stderr=PIPE, stdout=PIPE)
			embedline = str(proc.communicate()[1])
			self.buffer1.set_text(embedline)
			self.showdiag()
		else:
			self.buffer1.set_text("You must select a cover file from the file menu and a message file")
			self.showdiag()

	def steghcrackstatus(self):
		def hidestatus(widget):
			os.system("kill " + str(self.pid))
			self.dontshow = "yes"
			self.progresswindow.hide()
		self.quitbutton.connect("clicked", hidestatus)
		self.progresswindow.show()

	def stegextract(self, widget):
		self.xpass = self.stegxpass.get_text()
		self.sfile = self.file.get_text()
		head, tail = os.path.split(self.sfile)
		outdir = home + tail + '/steghide_extract'
		self.outfile = outdir + '/' + tail
		self.stegpassfile = str(self.stegxchooser.get_filename())
		if not os.path.isdir(outdir):
			os.mkdir(outdir)
		self.dontshow = "no"
		if self.sfile == "":
			self.buffer1.set_text("You must select a steg file to analyze/extract")
			self.showdiag()
		elif "button1" in self.activeradio:
			if self.stegpassfile == "None":
				self.buffer1.set_text("You must select a password dictionary to perform a password attack!")				
				self.showdiag()
			else:
				self.line = ''
				cmd = re.escape(execdir) + "/programs/" + self.arch + "/steghide extract -sf " + re.escape(self.sfile) + " -f -pf " + re.escape(self.stegpassfile) + " -xf " + re.escape(self.outfile)
				self.steghcrackstatus()			
				proc = Popen("exec " + cmd, shell=True, stderr=PIPE, stdout=PIPE)
				self.pid = proc.pid
				def test_io_watch(f, cond):
					out = f.readline()
					if out == '':
						return False
					self.line += out
					if "Done" in self.line:
						line2 = out
						outpass = self.line.split ("'")
						outpass = outpass[3]
						cmd = re.escape(execdir) + "/programs/" + self.arch + "/steghide info " + re.escape(self.sfile) + " -p '" + outpass + "'''"
						proc = Popen(cmd, shell=True, stderr=PIPE, stdout=PIPE)
						line = ''
						for append in proc.stdout:
							line += append
						for append in proc.stderr:
							line += append
						if "embedded file" in line:
							outfile2 = line.split ('"')
							outfile2 = outdir + "/" + outfile2[3]
							cmd = re.escape(execdir) + "/programs/" + self.arch + "/steghide extract -sf " + re.escape(self.sfile) + " -p '" + re.escape(outpass) + "' -f -xf " + re.escape(outfile2)
							proc = Popen(cmd, shell=True, stderr=PIPE, stdout=PIPE)
							for append in proc.stdout:
								line2 += append
							for append in proc.stderr:
								line2 += append
							os.remove(self.outfile)
							self.buffer1.set_text(line2)
						elif "embedded data" in line:
							self.ident()
							self.buffer1.set_text(line2 + "Output file is " + self.outfile)
					else:
						self.buffer1.set_text("Unable to find password with provided dictionary")
					return True
				def tester():
					if proc.poll() is None:
						self.progressbar.set_pulse_step(.25)
						self.progressbar.pulse()
						time.sleep(.5)
						return True	
					else:
						self.progresswindow.hide()
						if not "yes" in self.dontshow:	
			
							self.showdiag()
				GObject.io_add_watch(proc.stderr, GObject.IO_IN | GObject.IO_HUP, test_io_watch)
				GObject.io_add_watch(proc.stdout, GObject.IO_IN | GObject.IO_HUP, test_io_watch)
				GObject.idle_add(tester)
		elif "button2" in self.activeradio:
			cmd = re.escape(execdir) + "/programs/" + self.arch + "/steghide info " + re.escape(self.sfile) + " -p '" + self.xpass + "'''"
			proc = Popen(cmd, shell=True, stderr=PIPE, stdout=PIPE)
			line = ''
			for append in proc.stdout:
				line += append
			for append in proc.stderr:
				line += append
			if "embedded file" in line:
				outfile = line.split ('"')
				outfile = outdir + "/" + outfile[3]
				cmd = re.escape(execdir) + "/programs/" + self.arch + "/steghide extract -sf " + re.escape(self.sfile) + " -p '" + self.xpass + "' -f -xf " + re.escape(outfile)
				proc = Popen(cmd, shell=True, stderr=PIPE, stdout=PIPE)
				line = ''
				for append in proc.stdout:
					line += append
				for append in proc.stderr:
					line += append
				self.buffer1.set_text(line)
				self.showdiag()
			elif "embedded data" in line:
				cmd = re.escape(execdir) + "/programs/" + self.arch + "/steghide extract -sf " + re.escape(self.sfile) + " -p '" + self.xpass + "' -f -xf " + re.escape(self.outfile)
				proc = Popen(cmd, shell=True, stderr=PIPE, stdout=PIPE)
				line = ''
				for append in proc.stdout:
					line += append
				for append in proc.stderr:
					line += append
				self.ident()
				self.buffer1.set_text("wrote extracted data to " + self.outfile)
				self.showdiag()
			else:
				self.buffer1.set_text(line)
				self.showdiag()
		elif "button3" in self.activeradio:
			cmd = re.escape(execdir) + "/programs/" + self.arch + "/steghide info " + re.escape(self.sfile) + " -p '" + self.xpass + "'''"
			proc = Popen(cmd, shell=True, stderr=PIPE, stdout=PIPE)
			line = ''
			for append in proc.stdout:
				line += append
			for append in proc.stderr:
				line += append
			self.buffer1.set_text(line)
			self.showdiag()
