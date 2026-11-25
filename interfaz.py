import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class Interfaz(tk.Tk):
    def __init__(self, controlador, algoritmos, recomendaciones, predeterminado):
        super().__init__()
        self.ctrl = controlador
        self.algoritmos = algoritmos
        self.recomendaciones = recomendaciones
        self.title("Procesamiento y Ordenamiento Masivo de Datos")
        alto = min(780, max(560, self.winfo_screenheight() - 90))
        self.geometry(f"1060x{alto}")
        self.minsize(900, 600)
        self._estilos()
        self._construir(predeterminado)

    def _estilos(self):
        s = ttk.Style(self)
        if "clam" in s.theme_names():
            s.theme_use("clam")
        s.configure("Titulo.TLabel", font=("Segoe UI", 15, "bold"))
        s.configure("Sub.TLabel", foreground="#555")
        s.configure("Paso.TLabelframe.Label", font=("Segoe UI", 10, "bold"))
        s.configure("Accion.TButton", font=("Segoe UI", 10, "bold"), padding=6)
        s.configure("Treeview", rowheight=22)

    def _construir(self, predeterminado):
        cab = ttk.Frame(self, padding=(12, 10, 12, 0))
        cab.pack(fill="x")
        ttk.Label(cab, text="Sistema de Procesamiento y Ordenamiento Masivo de Datos",
                  style="Titulo.TLabel").pack(anchor="w")
        ttk.Label(cab, text="Siga los pasos de izquierda a derecha: cargar → ordenar → buscar → exportar.",
                  style="Sub.TLabel").pack(anchor="w")

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=12, pady=10)
        tab_proc = ttk.Frame(nb, padding=8)
        tab_comp = ttk.Frame(nb, padding=12)
        nb.add(tab_proc, text="  Procesamiento  ")
        nb.add(tab_comp, text="  Comparación de algoritmos  ")
        self._tab_procesamiento(tab_proc, predeterminado)
        self._tab_comparacion(tab_comp)

        self.barra = ttk.Label(self, text="Listo.", relief="sunken", anchor="w", padding=(8, 3))
        self.barra.pack(fill="x", side="bottom")

    def _tab_procesamiento(self, tab, predeterminado):
        tab.columnconfigure(1, weight=1)
        tab.rowconfigure(0, weight=1)
        izq = self._panel_con_scroll(tab)

        f1 = ttk.LabelFrame(izq, text=" 1. Cargar archivo ", style="Paso.TLabelframe", padding=8)
        f1.pack(fill="x", pady=(0, 8))
        ttk.Button(f1, text="📂  Seleccionar archivo (TXT / XLSX)", style="Accion.TButton",
                   command=lambda: self.ctrl.cargar()).pack(fill="x")
        self.lbl_archivo = ttk.Label(f1, text="Ningún archivo cargado", wraplength=250, style="Sub.TLabel")
        self.lbl_archivo.pack(anchor="w", pady=(6, 0))

        f2 = ttk.LabelFrame(izq, text=" 2. Ordenar datos ", style="Paso.TLabelframe", padding=8)
        f2.pack(fill="x", pady=(0, 8))
        ttk.Label(f2, text="Algoritmo:").pack(anchor="w")
        self.cb_algo = ttk.Combobox(f2, values=[t for _, t in self.algoritmos], state="readonly", width=34)
        self.cb_algo.current([c for c, _ in self.algoritmos].index(predeterminado))
        self.cb_algo.pack(fill="x", pady=(2, 6))
        ttk.Label(f2, text="Orden:").pack(anchor="w")
        self.var_orden = tk.StringVar(value="asc")
        fr = ttk.Frame(f2)
        fr.pack(anchor="w")
        ttk.Radiobutton(fr, text="Ascendente", variable=self.var_orden, value="asc").pack(side="left")
        ttk.Radiobutton(fr, text="Descendente", variable=self.var_orden, value="desc").pack(side="left", padx=10)
        self.btn_ordenar = ttk.Button(f2, text="⚙  Ordenar", style="Accion.TButton", command=self._ordenar)
        self.btn_ordenar.pack(fill="x", pady=(8, 0))
        self.lbl_orden = ttk.Label(f2, text="", wraplength=250)
        self.lbl_orden.pack(anchor="w", pady=(6, 0))

        f3 = ttk.LabelFrame(izq, text=" 3. Buscar un valor ", style="Paso.TLabelframe", padding=8)
        f3.pack(fill="x", pady=(0, 8))
        ttk.Label(f3, text="Valor entero:").pack(anchor="w")
        self.var_valor = tk.StringVar()
        ent = ttk.Entry(f3, textvariable=self.var_valor)
        ent.pack(fill="x", pady=(2, 6))
        ent.bind("<Return>", lambda e: self._buscar())
        ttk.Label(f3, text="Método:").pack(anchor="w")
        self.cb_busq = ttk.Combobox(f3, state="readonly",
                                    values=["Secuencial", "Binaria (requiere ordenado)", "Hash"])
        self.cb_busq.current(0)
        self.cb_busq.pack(fill="x", pady=(2, 6))
        self.btn_buscar = ttk.Button(f3, text="🔍  Buscar", style="Accion.TButton", command=self._buscar)
        self.btn_buscar.pack(fill="x")
        self.lbl_busq = ttk.Label(f3, text="", wraplength=250)
        self.lbl_busq.pack(anchor="w", pady=(6, 0))

        f4 = ttk.LabelFrame(izq, text=" 4. Exportar resultados ", style="Paso.TLabelframe", padding=8)
        f4.pack(fill="x")
        ttk.Label(f4, text="Formato del archivo ordenado:").pack(anchor="w")
        self.var_fmt = tk.StringVar(value="txt")
        ff = ttk.Frame(f4)
        ff.pack(anchor="w", pady=(2, 8))
        ttk.Radiobutton(ff, text="TXT", variable=self.var_fmt, value="txt").pack(side="left")
        ttk.Radiobutton(ff, text="XLSX (Excel)", variable=self.var_fmt, value="xlsx").pack(side="left", padx=10)
        self.btn_exp = ttk.Button(f4, text="💾  Guardar ordenado + reporte", style="Accion.TButton",
                                  command=self._exportar)
        self.btn_exp.pack(fill="x")

        der = ttk.LabelFrame(tab, text=" Resultados ", style="Paso.TLabelframe", padding=8)
        der.grid(row=0, column=1, sticky="nsew")
        der.columnconfigure((0, 1), weight=1, uniform="c")
        der.rowconfigure(2, weight=1)
        self.lbl_resumen = ttk.Label(der, text="", font=("Segoe UI", 10), justify="left")
        self.lbl_resumen.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 6))
        ttk.Label(der, text="Primeros 20 elementos", font=("Segoe UI", 10, "bold")).grid(row=1, column=0, sticky="w")
        ttk.Label(der, text="Últimos 20 elementos", font=("Segoe UI", 10, "bold")).grid(row=1, column=1, sticky="w")
        self.tv_ini = self._tabla(der, 2, 0)
        self.tv_fin = self._tabla(der, 2, 1)

    def _panel_con_scroll(self, tab):
        marco = ttk.Frame(tab)
        marco.grid(row=0, column=0, sticky="ns", padx=(0, 10))
        marco.rowconfigure(0, weight=1)
        canvas = tk.Canvas(marco, highlightthickness=0, borderwidth=0, width=300)
        barra = ttk.Scrollbar(marco, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=barra.set)
        canvas.grid(row=0, column=0, sticky="ns")
        barra.grid(row=0, column=1, sticky="ns")
        interior = ttk.Frame(canvas)
        ventana = canvas.create_window((0, 0), window=interior, anchor="nw")

        def ajustar(_e=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfigure(ventana, width=canvas.winfo_width())

        interior.bind("<Configure>", ajustar)
        canvas.bind("<Configure>", ajustar)

        def rueda(e):
            if interior.winfo_reqheight() <= canvas.winfo_height():
                return
            if getattr(e, "num", None) == 4:
                canvas.yview_scroll(-1, "units")
            elif getattr(e, "num", None) == 5:
                canvas.yview_scroll(1, "units")
            else:
                canvas.yview_scroll(-1 if e.delta > 0 else 1, "units")

        def activar(_e):
            canvas.bind_all("<MouseWheel>", rueda)
            canvas.bind_all("<Button-4>", rueda)
            canvas.bind_all("<Button-5>", rueda)

        def desactivar(_e):
            canvas.unbind_all("<MouseWheel>")
            canvas.unbind_all("<Button-4>")
            canvas.unbind_all("<Button-5>")

        marco.bind("<Enter>", activar)
        marco.bind("<Leave>", desactivar)
        return interior

    def _tabla(self, padre, fila, col):
        cont = ttk.Frame(padre)
        cont.grid(row=fila, column=col, sticky="nsew", padx=(0, 6) if col == 0 else (0, 0))
        tv = ttk.Treeview(cont, columns=("pos", "valor"), show="headings", height=20)
        tv.heading("pos", text="Posición")
        tv.heading("valor", text="Valor")
        tv.column("pos", width=80, anchor="center")
        tv.column("valor", width=140, anchor="e")
        sb = ttk.Scrollbar(cont, orient="vertical", command=tv.yview)
        tv.configure(yscrollcommand=sb.set)
        tv.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        return tv

    def _tab_comparacion(self, tab):
        ttk.Label(tab, text="Algoritmo recomendado según el escenario", style="Titulo.TLabel").pack(anchor="w")
        tv = ttk.Treeview(tab, columns=("esc", "alg", "por"), show="headings", height=5)
        for c, t, w in (("esc", "Escenario", 220), ("alg", "Algoritmo recomendado", 280), ("por", "Justificación", 460)):
            tv.heading(c, text=t)
            tv.column(c, width=w, anchor="w")
        for fila in self.recomendaciones:
            tv.insert("", "end", values=fila)
        tv.pack(fill="x", pady=(8, 12))

        caja = ttk.LabelFrame(tab, text=" Medición en vivo con los datos cargados ",
                              style="Paso.TLabelframe", padding=8)
        caja.pack(fill="both", expand=True)
        ttk.Label(caja, style="Sub.TLabel", wraplength=900, text=(
            "Ordena una copia de los datos cargados (ascendente) con cada algoritmo, mide el tiempo "
            "de ejecución y verifica que el resultado quede ordenado.")).pack(anchor="w")
        self.btn_comparar = ttk.Button(caja, text="⏱  Comparar algoritmos", style="Accion.TButton",
                                       command=self._comparar)
        self.btn_comparar.pack(anchor="w", pady=8)
        self.lbl_comparacion = ttk.Label(caja, text="", wraplength=900)
        self.lbl_comparacion.pack(anchor="w", pady=(0, 6))
        cont = ttk.Frame(caja)
        cont.pack(fill="both", expand=True)
        self.tv_comp = ttk.Treeview(cont, columns=("pos", "alg", "tipo", "tiempo", "ok"),
                                    show="headings", height=10)
        for c, t, w, a in (("pos", "#", 50, "center"), ("alg", "Algoritmo", 240, "w"),
                           ("tipo", "Tipo", 100, "center"), ("tiempo", "Tiempo (s)", 140, "e"),
                           ("ok", "Resultado", 140, "center")):
            self.tv_comp.heading(c, text=t)
            self.tv_comp.column(c, width=w, anchor=a)
        sb = ttk.Scrollbar(cont, orient="vertical", command=self.tv_comp.yview)
        self.tv_comp.configure(yscrollcommand=sb.set)
        self.tv_comp.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

    def _ordenar(self):
        clave = self.algoritmos[self.cb_algo.current()][0]
        self.ctrl.ordenar(clave, self.var_orden.get() == "desc")

    def _buscar(self):
        self.ctrl.buscar(self.var_valor.get(), self.cb_busq.current())

    def _exportar(self):
        self.ctrl.exportar(self.var_fmt.get())

    def _comparar(self):
        self.ctrl.comparar()

    def pedir_archivo(self):
        return filedialog.askopenfilename(
            title="Seleccione el archivo de datos",
            initialdir="datos" if os.path.isdir("datos") else ".",
            filetypes=[("Datos (TXT, XLSX)", "*.txt *.xlsx"), ("Texto", "*.txt"), ("Excel", "*.xlsx")])

    def pedir_guardar(self, fmt):
        ext = "." + fmt
        tipos = [("Excel (XLSX)", "*.xlsx")] if fmt == "xlsx" else [("Texto (TXT)", "*.txt")]
        return filedialog.asksaveasfilename(
            title=f"Guardar archivo ordenado ({fmt.upper()})",
            initialdir="salida" if os.path.isdir("salida") else ".",
            initialfile="resultado_ordenado", defaultextension=ext, filetypes=tipos)

    def error(self, titulo, texto):
        messagebox.showerror(titulo, texto)

    def aviso(self, titulo, texto):
        messagebox.showwarning(titulo, texto)

    def info(self, titulo, texto):
        messagebox.showinfo(titulo, texto)

    def estado(self, texto):
        self.barra.config(text=texto)

    def actualizar(self):
        self.update()

    def ocupado(self, activo):
        est = "disabled" if activo else "normal"
        for b in (self.btn_ordenar, self.btn_buscar, self.btn_exp, self.btn_comparar):
            b.config(state=est)
        self.config(cursor="watch" if activo else "")
        self.update_idletasks()

    def refrescar(self, hay_datos, hay_ordenado, primeros, ultimos, resumen):
        self.btn_ordenar.config(state="normal" if hay_datos else "disabled")
        self.btn_buscar.config(state="normal" if hay_datos else "disabled")
        self.btn_comparar.config(state="normal" if hay_datos else "disabled")
        self.btn_exp.config(state="normal" if hay_ordenado else "disabled")
        for tv, filas in ((self.tv_ini, primeros), (self.tv_fin, ultimos)):
            tv.delete(*tv.get_children())
            for fila in filas:
                tv.insert("", "end", values=fila)
        self.lbl_resumen.config(text=resumen)

    def mostrar_archivo(self, texto):
        self.lbl_archivo.config(text=texto)

    def mostrar_tiempo_orden(self, texto):
        self.lbl_orden.config(text=texto, foreground="#1a5fb4")

    def mostrar_busqueda(self, texto, encontrado=True):
        self.lbl_busq.config(text=texto, foreground="#1a7f37" if encontrado else "#b42318")

    def resaltar(self, posicion):
        for tv in (self.tv_ini, self.tv_fin):
            for item in tv.get_children():
                if str(tv.item(item, "values")[0]) == str(posicion):
                    tv.selection_set(item)
                    tv.see(item)

    def mostrar_comparacion(self, filas, nota):
        self.tv_comp.delete(*self.tv_comp.get_children())
        for fila in filas:
            self.tv_comp.insert("", "end", values=fila)
        self.lbl_comparacion.config(text=nota)
