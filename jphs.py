import os, pwd, sys, pexpect, re, struct, time

home = pwd.getpwuid(os.getuid()).pw_dir + '/SSAK/'
execdir = os.path.dirname(os.path.realpath(sys.argv[0]))

class jphs:

	def jphideit2(self, widget):
		os.environ["WINEDEBUG"] = "warn-all,-heap,-relay,err-all,fixme-all,trace-all"
		os.environ["WINEPREFIX"] = home + "/wineprefix"
		self.sfile = self.file.get_text()
		self.spass = self.password.get_text()
		self.hidefile = self.fchooser.get_filename()
		filetype = self.fileinfo.get_text()
		if self.sfile != '' and str.strip(self.spass) != '' and self.hidefile != None:
			if "JPEG" in filetype:
				head, tail = os.path.split(self.sfile)
				needwin = ("OFF", "ON")[self.checkwin.get_active()]
				if needwin == "ON":
					outdir = home + tail + '/jphidewin'
					progcmd = "/usr/bin/wine " + re.escape(execdir) + "/programs/Win/jphide.exe " 
				else:
					outdir = home + tail + '/jphidelin'
					progcmd = execdir + "/programs/" + self.arch + "/jphide "
				if not os.path.isdir(outdir):
					os.mkdir(outdir)
				self.outfile = outdir + '/' +tail
				if os.path.isfile(self.outfile):
					os.remove(self.outfile)
				cmd = progcmd + re.escape(self.sfile) + " " + re.escape(self.outfile) + " " + re.escape(self.hidefile)
				child = pexpect.spawn(cmd)
				child.expect('Passphrase:')
				child.sendline(self.spass)
				child.expect('Re-enter  :')
				child.sendline(self.spass)
				child.expect(pexpect.EOF)
				self.buffer1.set_text("Output file should be located here: " + self.outfile + "!")
				self.showdiag()
			else:
				self.buffer1.set_text("Input file must be jpeg!")
				self.showdiag()
		else:
			self.buffer1.set_text("You must select a valid input JPEG input file, a valid hide file and a password")
			self.showdiag()

	def jpseekit2(self, widget):
		os.environ["WINEDEBUG"] = "warn-all,-heap,-relay,err-all,fixme-all,trace-all"
		os.environ["WINEPREFIX"] = home + "/wineprefix"
		self.sfile = self.file.get_text()
		self.spass2 = self.password2.get_text()
		filetype = self.fileinfo.get_text()
		if self.sfile != '' and self.spass2 != '':
			if "JPEG" in filetype:
				head, tail = os.path.split(self.sfile)
				needwin = ("OFF", "ON")[self.checkwin2.get_active()]
				if needwin == "ON":
					outdir = home + tail + '/jpseekwin'
					if not os.path.isdir(outdir):
						os.mkdir(outdir)
					self.outfile = outdir + '/' + tail + '.txt'
					if os.path.isfile(self.outfile):
						os.remove(self.outfile)
					cmd = "/usr/bin/wine " + re.escape(execdir) + "/programs/Win/jpseek.exe " + re.escape(self.sfile) + " " + re.escape(self.outfile)

					child = pexpect.spawn(cmd)
					child.expect('Passphrase:')
					child.sendline(self.spass2)
					child.expect(pexpect.EOF)
					self.buffer1.set_text("Output file should be located here: " + self.outfile + "!")
					self.showdiag()
					os.chmod(self.outfile, 0o600)

				else:
					outdir = home + tail + '/jpseeklin'
					if not os.path.isdir(outdir):
						os.mkdir(outdir)
					self.outfile = outdir + '/' + tail + '.txt'
					if os.path.isfile(self.outfile):
						os.remove(self.outfile)
					cmd = execdir + "/programs/" + self.arch + "/jpseek " + re.escape(self.sfile) + " " + re.escape(self.outfile)
					child = pexpect.spawn(cmd)
					child.expect('Passphrase:')
					child.sendline(self.spass2)
					child.expect(pexpect.EOF)
					time.sleep(3)
					os.chmod(self.outfile, 0o600)
					self.ident()
					self.buffer1.set_text("Output file should be located here: " + self.outfile + "!")
					self.showdiag()

			else:
				self.buffer1.set_text("Input file must be jpeg!")
				self.showdiag()
		else:
			self.buffer1.set_text("You must select a valid file, and insert a password")
			self.showdiag()

