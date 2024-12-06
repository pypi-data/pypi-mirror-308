import openSIMS as S
import tkinter as tk
import tkinter.ttk as ttk
import os.path
from . import Main

class ListWindow(tk.Toplevel):

    def __init__(self,top,button):
        super().__init__(top)
        self.title('Select standards')

        samples = S.get('samples')
        snames = list(samples.keys())
        refmats = ['sample'] + self.shared_refmats()
        self.combo_labels = []
        self.combo_vars = []
        self.combo_boxes = []
        Main.offset(button,self)
        canvas = tk.Canvas(self)
        canvas.grid(row=0,column=0,sticky="nsew")
        if len(samples)>20:
            canvas.configure(width=400,height=600)
            scrollbar = tk.Scrollbar(self,orient="vertical",
                                     command=canvas.yview)
            scrollbar.grid(row=0,column=1,sticky="ns")
            canvas.configure(yscrollcommand=scrollbar.set)

        row = 0
        for sname, sample in samples.items():
            label = ttk.Label(canvas,text=sname)
            label.grid(row=row,column=0,padx=1,pady=1)
            var = tk.StringVar()
            combo = ttk.Combobox(canvas,values=refmats,textvariable=var)
            combo.set(sample.group)
            combo.grid(row=row,column=1,padx=1,pady=1)
            combo.bind("<<ComboboxSelected>>",self.on_change)
            self.combo_labels.append(label)
            self.combo_vars.append(var)
            self.combo_boxes.append(combo)
            row += 1

        button = ttk.Button(self,text='Save',command=self.on_click)
        button.grid(row=1,column=0)

        self.protocol("WM_DELETE_WINDOW",self.on_closing)

    def on_closing(self):
        setattr(self.master,'standard_window',None)
        self.destroy()

    def on_change(self,event):
        i = self.combo_boxes.index(event.widget)
        changed = self.combo_labels[i].cget('text')
        ignored = S.get('ignore')
        if event.widget.get() == 'sample':
            ignored.add(changed)
        elif changed in ignored:
            ignored.remove(changed)
        else:
            pass
        prefixes = self.get_prefixes()
        self.set_prefixes(prefixes)

    def get_prefixes(self):
        groups = self.all_groups()
        prefixes = dict.fromkeys(groups,None)
        ignored = S.get('ignore')
        for i, box in enumerate(self.combo_boxes):
            sname = self.combo_labels[i].cget('text')
            group = box.get()
            if sname not in ignored and group != 'sample':
                if prefixes[group] is None:
                    prefixes[group] = sname
                else:
                    prefixes[group] = os.path.commonprefix([sname,prefixes[group]])
        return prefixes

    def set_prefixes(self,prefixes):
        ignored = S.get('ignore')
        for i, box in enumerate(self.combo_boxes):
            sname = self.combo_labels[i].cget('text')
            if sname not in ignored:
                group = self.match_prefix(sname,prefixes)
                box.set(group)

    def match_prefix(self,sname,prefixes):
        for group, prefix in prefixes.items():
            if sname.startswith(prefix):
                return group
        return 'sample'

    def all_groups(self):
        out = set()
        for i, box in enumerate(self.combo_boxes):
            group = box.get()
            if group != 'sample':
                out.add(group)
        return out

    def shared_refmats(self):
        method_list = S.list_methods()
        refmats = set(S.settings(method_list[0])['refmats'].index)
        for method in method_list:
            refmats = refmats & set(S.settings(method)['refmats'].index)
        return list(refmats)

    def on_click(self):
        groups = dict()
        for i, var in enumerate(self.combo_vars):
            group = var.get()
            if group == 'sample':
                pass
            elif group in groups:
                groups[group].append(i)
            else:
                groups[group] = [i]
        blocks = []
        for group, indices in groups.items():
            blocks.append(group + "=[" + ",".join(map(str,indices)) + "]")
        cmd = "S.standards(" + ",".join(blocks) + ")"
        self.master.run(cmd)
