import os, pwd, sys, gi, re, time, fcntl, pty
from gi.repository import Gtk, GObject
from subprocess import Popen, PIPE

home = pwd.getpwuid(os.getuid()).pw_dir + '/SSAK/'
execdir = os.path.dirname(os.path.realpath(sys.argv[0]))
stegprog = 'java -jar ' + re.escape(execdir) + '/programs/noarch/openstego.jar '

class openstego:

	def togglepass(self, widget, data=None):
		value=''
		value = ("OFF", "ON")[widget.get_active()]
		if value == "OFF":
			self.pass2.set_property("editable", False)
		if value == "ON":
			self.pass2.set_property("editable", True)

	def togglepass2(self, widget, data=None):
		value=''
		value = ("OFF", "ON")[widget.get_active()]
		if value == "OFF":
			self.pass4.set_property("editable", False)
		if value == "ON":
			self.pass4.set_property("editable", True)

	def ostegembed2(self, widget):
		value = ("OFF", "ON")[self.checkbutton3.get_active()]
		value2 = ("OFF", "ON")[self.checkbutton2.get_active()]
		self.sfile = self.file.get_text()
		self.spass = self.pass2.get_text()
		self.alg = (self.algorithm.get_active())
		if self.alg == 0:
			self.algorithm2 = "RandomLSB"
		elif self.alg == 1:
			self.algorithm2 = "LSB"
		self.fchooser2.connect("delete-event", lambda window, event: self.fchooser2.destroy() or True)
		self.hidefile2 = str(self.fchooser2.get_filename())
		head, tail = os.path.split(self.sfile)
		outdir = home + tail + '/openstegembed'
		self.outfile2 = outdir + '/' + tail + '.png'
		if not os.path.isdir(outdir):
			os.mkdir(outdir)
		self.outfile2 = outdir + '/' + tail + '.png'
		if os.path.isfile(self.outfile2):
			os.remove(self.outfile2)
		if self.hidefile2 != "None" and self.sfile != '':
			if value =="ON" and str.strip(self.spass) == '':
				self.buffer1.set_text("If you select the password option you must fill in the password entry!")
				self.showdiag()
			else:			
				cmd = stegprog + ' --embed --algorithm ' + self.algorithm2 + ' --messagefile ' + re.escape(self.hidefile2) + ' --coverfile ' + re.escape(self.sfile) + ' --stegofile ' + re.escape(self.outfile2)
				if value2 == "ON":
					cmd += ' --compress '
				elif value2 == "OFF":
					cmd += ' --nocompress '
				if value == "ON":
					cmd += ' --encrypt --password ' + self.spass
				elif value == "OFF":
					cmd += ' --noencrypt'
				proc = Popen(cmd, shell = True, stderr=PIPE, stdout=PIPE)
				line = str(proc.communicate()[1])
				if str.strip(line) == '':
					self.buffer1.set_text("Output file should exist here: \n" + self.outfile2)
				else:
					self.buffer1.set_text(line)
				self.showdiag()
		else:
			self.buffer1.set_text("You must select a valid image file and a file to be hidden.")
			self.showdiag()	

	def ostegextract2(self, widget):
		self.sfile = self.file.get_text()
		value3 = ("OFF", "ON")[self.checkbutton4.get_active()] 
		self.spass = self.pass3.get_text()
		self.alg2 = (self.algorithm2.get_active())	
		self.info = self.fileinfo.get_text()
		ostegattack = ("OFF", "ON")[self.passattack.get_active()]
		if self.alg2 == 0:
			self.algorithm3 = "RandomLSB"
		elif self.alg2 == 1:
			self.algorithm3 = "LSB"
		head, tail = os.path.split(self.sfile)
		outdir = home + tail + '/openstegextract'
		if not os.path.isdir(outdir):
			os.mkdir(outdir)
		if self.sfile != '' and "PNG" in self.info:
			self.buffer2.set_text("Please Wait \n")		
			self.ostegdictionary = str(self.passfilechoose.get_filename())
			if ostegattack == "ON":
				if self.ostegdictionary != "None":
					head, tail = os.path.split(self.sfile)
					outdir = home + tail + '/openstegattack'
					if not os.path.isdir(outdir):
						os.mkdir(outdir)
					print re.escape(outdir)
					master, slave = pty.openpty()
					cmd = "python " + re.escape(execdir) + "/breakosteg.py " + re.escape(self.ostegdictionary) + " " + re.escape(self.sfile) + " " + re.escape(outdir)
					print cmd
					proc = Popen("exec " + cmd, shell=True, stdout=slave)
					pid = proc.pid

					def showprogress():
						def hideprogress(widget):
							os.system("kill " + str(pid))
							self.showstatus.hide()
						self.statusbutton.connect("clicked",hideprogress)
						self.showstatus.show()
					showprogress()
					def test_io_watch(f, cond):
						out = f.readline()
						end_iter = self.buffer2.get_end_iter()
						self.buffer2.insert(end_iter, out)
						adj = self.sw.get_vadjustment()
						adj.set_value(adj.get_upper() - adj.get_page_size())
						if "Extracted" in out:
							print out
						if out == '':
							return False
						return True
	
					GObject.io_add_watch(os.fdopen(master), GObject.IO_IN | GObject.IO_HUP, test_io_watch)
				else:
					self.buffer1.set_text("You must select a dictionary if you want to perform a dictionary attack!")
					self.showdiag()
			else:
				if value3 == "ON" and str.strip(self.spass) == '':
					self.buffer1.set_text("If you select the password option you must fill in the password entry!")
					self.showdiag()
				else:
					cmd = stegprog + ' extract --algorithm=' + self.algorithm3 + ' --stegofile=' + re.escape(self.sfile) + ' --extractdir=' + re.escape(outdir)
					if value3 == "ON":
						cmd += ' --password=' + self.spass
					proc = Popen(cmd, shell=True, stderr=PIPE, stdout=PIPE)
					line = str(proc.communicate()[1])
					self.buffer1.set_text(line)
					self.showdiag()
		else:
			self.buffer1.set_text("You must select a valid PNG file before performing any operations. Please select a valid PNG file using the file menu!")
			self.showdiag()
			

