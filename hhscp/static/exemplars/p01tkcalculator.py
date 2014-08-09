__author__ = 'ericdennison'

import tkinter as tk

class Calculator(tk.Tk):

    # keys are keycap
    keys = (('7', '8', '9', '/'),
            ('4', '5', '6', 'X'),
            ('1', '2', '3', '-'),
            ('0', '.','','+'),
            ('',  '',  '',  '='))

    nums = ['0','1','2','3','4','5','6','7','8','9','.']
    ops = ['/','X','-','+']
    opsmap = {'/':'/', 'X':'*', '-':'-', '+':'+'}
    keymap = {'0':'0','1':'1','2':'2','3':'3','4':'4','5':'5',
              '6':'6','7':'7','8':'8','9':'9','.':'.',
              '\r':'=','/':'/','*':'X','-':'-','+':'+'}

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Calculator")
        self.curval = tk.StringVar()
        self.curval.set('0')
        self.display = tk.Label(self, textvariable = self.curval, justify=tk.LEFT)
        self.display.grid(row=0, columnspan=4, sticky=tk.W)
        self.accum = 0.0
        self._clearop()
        self.state = 'getfirst'
        rownum = 0
        for row in Calculator.keys:
            rownum += 1
            colnum = -1
            for keycap in row:
                colnum += 1
                if keycap != "":
                    but = tk.Button(self, text=keycap, command = lambda x=keycap: self.keyhandler(x))
                    but.grid(row=rownum, column=colnum)
        self.bind('<Key>', self.keycallback)

    def _clearop(self):
        self.operation = ''

    def _curfloat(self):
        return float(self.curval.get())

    def _setcurfloat(self, val):
        self.curval.set("{0:.8}".format(val))

    def keycallback(self, event):
        try:
            self.keyhandler(Calculator.keymap[event.char])
        except KeyError:
            pass

    def numhandler(self, num):
        if self.state == 'getfirst' or (self.curval == '0' and num != '.'):
            self.curval.set('')
        if num != '.' or not self.curval.get().count('.'):
            self.curval.set(self.curval.get()+num)
        if self.state == 'getfirst':
            self.state = 'getnext'

    def ophandler(self, op):
        try:
            self.accum = float(self.curval.get())
        except ValueError:
            self.accum = 0.0
        self.operation = op
        self.state = 'getfirst'

    def eqhandler(self):
        curval = self._curfloat()
        try:
            result = eval('self.accum'+self.opsmap[self.operation]+'curval')
            self._setcurfloat(result)
        except ZeroDivisionError:
            self.curval.set('ERROR')
        except (SyntaxError, KeyError):
            pass
        self.state = 'getfirst'
        self._clearop()

    def neghandler(self):
        self._setcurfloat(-self._curfloat())

    def keyhandler(self, keycap):
        if keycap in Calculator.nums:
            self.numhandler(keycap)
        elif keycap in Calculator.ops:
            self.ophandler(keycap)
        elif keycap == '=':
            self.eqhandler()
        elif keycap == '(-)':
            self.neghandler()

app = Calculator()
app.mainloop()

