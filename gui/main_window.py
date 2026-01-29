import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import tkinter.font as tkfont
from datetime import datetime
import threading

from models.cliente_regular import ClienteRegular
from models.cliente_premium import ClientePremium
from models.cliente_corporativo import ClienteCorporativo
from database.db_manager import DatabaseManager
from database.json_manager import JSONManager
from api_integrations.email_validator import SimpleEmailValidator, APIBasedEmailValidator
from api_integrations.notification_service import NotificationService
from utils.validators import Validators
from utils.logger import Logger

class GICApp:
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Gestor Inteligente de Clientes - SolutionTech")
        self.root.geometry("1200x700")
        self.root.configure(bg='#f0f0f0')
        
        self.db_manager = DatabaseManager()
        self.json_manager = JSONManager()
        self.email_validator = SimpleEmailValidator()
        self.validators = Validators()
        self.logger = Logger()
        
        try:
            self.root.iconbitmap('assets/icon.ico')
        except:
            pass
        
        self.title_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
        self.normal_font = tkfont.Font(family="Helvetica", size=10)
        
        self.clientes = []
        self.cliente_seleccionado = None
        
        self._crear_widgets()
        self._cargar_clientes()
        
    def _crear_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        ttk.Label(main_frame, text="Gestor Inteligente de Clientes", 
                 font=self.title_font, foreground="#2c3e50").grid(
                 row=0, column=0, columnspan=3, pady=(0, 20))
        
        left_frame = ttk.LabelFrame(main_frame, text="Clientes", padding="10")
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(1, weight=1)
        
        btn_frame = ttk.Frame(left_frame)
        btn_frame.grid(row=0, column=0, pady=(0, 10), sticky=(tk.W, tk.E))
        
        ttk.Button(btn_frame, text="Nuevo Cliente", 
                  command=self._nuevo_cliente, width=15).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Refrescar", 
                  command=self._cargar_clientes, width=10).pack(side=tk.LEFT)
        
        search_frame = ttk.Frame(left_frame)
        search_frame.grid(row=1, column=0, pady=(0, 10), sticky=(tk.W, tk.E))
        
        ttk.Label(search_frame, text="Buscar:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20)
        self.search_entry.pack(side=tk.LEFT, padx=(5, 5))
        ttk.Button(search_frame, text="Buscar", 
                  command=self._buscar_clientes, width=10).pack(side=tk.LEFT)
        
        self.client_listbox = tk.Listbox(left_frame, height=20, font=self.normal_font)
        self.client_listbox.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, 
                                 command=self.client_listbox.yview)
        scrollbar.grid(row=2, column=1, sticky=(tk.N, tk.S))
        self.client_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.client_listbox.bind('<<ListboxSelect>>', self._seleccionar_cliente)
        
        center_frame = ttk.LabelFrame(main_frame, text="Detalles del Cliente", padding="10")
        center_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        center_frame.columnconfigure(1, weight=1)
        
        row = 0
        
        ttk.Label(center_frame, text="ID:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.id_var = tk.StringVar()
        ttk.Entry(center_frame, textvariable=self.id_var, state='readonly', 
                 width=30).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
        row += 1
        
        ttk.Label(center_frame, text="Tipo:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.tipo_var = tk.StringVar(value="Regular")
        tipo_combo = ttk.Combobox(center_frame, textvariable=self.tipo_var, 
                                 values=["Regular", "Premium", "Corporativo"], 
                                 state="readonly", width=27)
        tipo_combo.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
        tipo_combo.bind('<<ComboboxSelected>>', self._cambiar_tipo_cliente)
        row += 1
        
        ttk.Label(center_frame, text="Nombre:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.nombre_var = tk.StringVar()
        ttk.Entry(center_frame, textvariable=self.nombre_var, 
                 width=30).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
        row += 1
        
        ttk.Label(center_frame, text="Email:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.email_var = tk.StringVar()
        email_entry = ttk.Entry(center_frame, textvariable=self.email_var, 
                               width=30)
        email_entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
        ttk.Button(center_frame, text="Validar", 
                  command=self._validar_email, width=8).grid(row=row, column=2, padx=(5, 0))
        row += 1
        
        ttk.Label(center_frame, text="Teléfono (+56):").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.telefono_var = tk.StringVar()
        ttk.Entry(center_frame, textvariable=self.telefono_var, 
                 width=30).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
        row += 1
        
        ttk.Label(center_frame, text="Dirección:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.direccion_var = tk.StringVar()
        ttk.Entry(center_frame, textvariable=self.direccion_var, 
                 width=30).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
        row += 1
        
        ttk.Label(center_frame, text="RUT:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.rut_var = tk.StringVar()
        ttk.Entry(center_frame, textvariable=self.rut_var, 
                 width=30).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
        row += 1
        
        self.specific_frame = ttk.Frame(center_frame)
        self.specific_frame.grid(row=row, column=0, columnspan=3, 
                                sticky=(tk.W, tk.E), pady=10)
        row += 1
        
        button_frame = ttk.Frame(center_frame)
        button_frame.grid(row=row, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="Guardar", 
                  command=self._guardar_cliente, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Eliminar", 
                  command=self._eliminar_cliente, width=12).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Limpiar", 
                  command=self._limpiar_formulario, width=12).pack(side=tk.LEFT, padx=5)
        
        right_frame = ttk.LabelFrame(main_frame, text="Registro de Actividad", padding="10")
        right_frame.grid(row=1, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(10, 0))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(right_frame, height=25, 
                                                 font=('Consolas', 9))
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        log_btn_frame = ttk.Frame(right_frame)
        log_btn_frame.grid(row=1, column=0, pady=(10, 0), sticky=(tk.W, tk.E))
        
        ttk.Button(log_btn_frame, text="Actualizar Logs", 
                  command=self._actualizar_logs, width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(log_btn_frame, text="Exportar JSON", 
                  command=self._exportar_json, width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(log_btn_frame, text="Exportar CSV", 
                  command=self._exportar_csv, width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(log_btn_frame, text="Backup", 
                  command=self._crear_backup, width=12).pack(side=tk.LEFT, padx=2)
        
        self.status_var = tk.StringVar(value="Sistema listo")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self._actualizar_frame_especifico()
        self._actualizar_logs()
    
    def _cargar_clientes(self):
        try:
            self.clientes = self.db_manager.obtener_todos_clientes()
            self._actualizar_lista_clientes()
            self._actualizar_status(f"Clientes cargados: {len(self.clientes)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los clientes: {str(e)}")
    
    def _actualizar_lista_clientes(self):
        self.client_listbox.delete(0, tk.END)
        
        for cliente in self.clientes:
            display_text = f"{cliente.id:04d} - {cliente.nombre} ({cliente.obtener_tipo()})"
            self.client_listbox.insert(tk.END, display_text)
    
    def _seleccionar_cliente(self, event):
        seleccion = self.client_listbox.curselection()
        
        if seleccion:
            indice = seleccion[0]
            if indice < len(self.clientes):
                self.cliente_seleccionado = self.clientes[indice]
                self._mostrar_detalles_cliente()
    
    def _mostrar_detalles_cliente(self):
        if not self.cliente_seleccionado:
            return
        
        cliente = self.cliente_seleccionado
        
        self.id_var.set(str(cliente.id))
        self.nombre_var.set(cliente.nombre)
        self.email_var.set(cliente.email)
        
        telefono = cliente.telefono
        if telefono.startswith("+56"):
            telefono = telefono[3:]
        self.telefono_var.set(telefono)
        self.direccion_var.set(cliente.direccion)
        self.rut_var.set(cliente.rut)
        
        tipo = cliente.obtener_tipo()
        if "Regular" in tipo:
            self.tipo_var.set("Regular")
        elif "Premium" in tipo:
            self.tipo_var.set("Premium")
        elif "Corporativo" in tipo:
            self.tipo_var.set("Corporativo")
        
        self._actualizar_frame_especifico()
    
    def _cambiar_tipo_cliente(self, event=None):
        self._actualizar_frame_especifico()
    
    def _actualizar_frame_especifico(self):
        for widget in self.specific_frame.winfo_children():
            widget.destroy()
        
        tipo = self.tipo_var.get()
        
        if tipo == "Regular":
            self._crear_frame_regular()
        elif tipo == "Premium":
            self._crear_frame_premium()
        elif tipo == "Corporativo":
            self._crear_frame_corporativo()
    
    def _crear_frame_regular(self):
        ttk.Label(self.specific_frame, text="Puntos Fidelidad:").grid(
            row=0, column=0, sticky=tk.W, pady=2)
        
        self.puntos_var = tk.StringVar(value="0")
        if self.cliente_seleccionado and isinstance(self.cliente_seleccionado, ClienteRegular):
            self.puntos_var.set(str(self.cliente_seleccionado.puntos_fidelidad))
        
        ttk.Entry(self.specific_frame, textvariable=self.puntos_var, 
                 width=15).grid(row=0, column=1, sticky=tk.W, pady=2)
    
    def _crear_frame_premium(self):
        ttk.Label(self.specific_frame, text="Nivel:").grid(
            row=0, column=0, sticky=tk.W, pady=2)
        
        self.nivel_var = tk.StringVar(value="oro")
        if self.cliente_seleccionado and isinstance(self.cliente_seleccionado, ClientePremium):
            self.nivel_var.set(self.cliente_seleccionado.nivel)
        
        nivel_combo = ttk.Combobox(self.specific_frame, textvariable=self.nivel_var,
                                  values=["oro", "plata", "platino"], 
                                  state="readonly", width=12)
        nivel_combo.grid(row=0, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(self.specific_frame, text="Beneficios Extra:").grid(
            row=1, column=0, sticky=tk.W, pady=2)
        
        self.beneficios_var = tk.StringVar()
        if self.cliente_seleccionado and isinstance(self.cliente_seleccionado, ClientePremium):
            beneficios = ", ".join(self.cliente_seleccionado.beneficios_extra)
            self.beneficios_var.set(beneficios)
        
        ttk.Entry(self.specific_frame, textvariable=self.beneficios_var, 
                 width=25).grid(row=1, column=1, sticky=tk.W, pady=2)
    
    def _crear_frame_corporativo(self):
        row = 0
        
        ttk.Label(self.specific_frame, text="Empresa:").grid(
            row=row, column=0, sticky=tk.W, pady=2)
        
        self.empresa_var = tk.StringVar()
        if self.cliente_seleccionado and isinstance(self.cliente_seleccionado, ClienteCorporativo):
            self.empresa_var.set(self.cliente_seleccionado.empresa)
        
        ttk.Entry(self.specific_frame, textvariable=self.empresa_var, 
                 width=25).grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1
        
        ttk.Label(self.specific_frame, text="Contacto Alterno:").grid(
            row=row, column=0, sticky=tk.W, pady=2)
        
        self.contacto_var = tk.StringVar()
        if self.cliente_seleccionado and isinstance(self.cliente_seleccionado, ClienteCorporativo):
            self.contacto_var.set(self.cliente_seleccionado.contacto_alterno or "")
        
        ttk.Entry(self.specific_frame, textvariable=self.contacto_var, 
                 width=25).grid(row=row, column=1, sticky=tk.W, pady=2)
    
    def _nuevo_cliente(self):
        self.cliente_seleccionado = None
        self._limpiar_formulario()
        
        if self.clientes:
            nuevo_id = max(c.id for c in self.clientes) + 1
        else:
            nuevo_id = 1001
        
        self.id_var.set(str(nuevo_id))
        self._actualizar_status("Listo para nuevo cliente")
    
    def _limpiar_formulario(self):
        self.id_var.set("")
        self.nombre_var.set("")
        self.email_var.set("")
        self.telefono_var.set("")
        self.direccion_var.set("")
        self.rut_var.set("")
        self.tipo_var.set("Regular")
        
        if hasattr(self, 'puntos_var'):
            self.puntos_var.set("0")
        if hasattr(self, 'nivel_var'):
            self.nivel_var.set("oro")
        if hasattr(self, 'beneficios_var'):
            self.beneficios_var.set("")
        if hasattr(self, 'empresa_var'):
            self.empresa_var.set("")
        if hasattr(self, 'contacto_var'):
            self.contacto_var.set("")
        
        self._actualizar_frame_especifico()
        self._actualizar_status("Formulario limpiado")
    
    def _validar_email(self):
        email = self.email_var.get().strip()
        
        if not email:
            messagebox.showwarning("Validación", "Ingrese un email para validar")
            return
        
        try:
            resultado = self.email_validator.validar_email(email)
            
            if resultado['valido']:
                messagebox.showinfo("Email Válido", 
                                  f"✅ {resultado['mensaje']}\n\n"
                                  f"Detalles: {resultado['detalles']}")
            else:
                messagebox.showerror("Email Inválido", 
                                   f"❌ {resultado['mensaje']}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error en validación: {str(e)}")
    
    def _guardar_cliente(self):
        try:
            if not self.nombre_var.get().strip():
                messagebox.showwarning("Validación", "El nombre es obligatorio")
                return
            
            if not self.email_var.get().strip():
                messagebox.showwarning("Validación", "El email es obligatorio")
                return
            
            if not self.telefono_var.get().strip():
                messagebox.showwarning("Validación", "El teléfono es obligatorio")
                return
            
            if not self.direccion_var.get().strip():
                messagebox.showwarning("Validación", "La dirección es obligatoria")
                return
            
            if not self.rut_var.get().strip():
                messagebox.showwarning("Validación", "El RUT es obligatorio")
                return
            
            cliente_id = int(self.id_var.get()) if self.id_var.get() else 0
            nombre = self.nombre_var.get().strip()
            email = self.email_var.get().strip()
            
            telefono_input = self.telefono_var.get().strip()
            if telefono_input and not telefono_input.startswith('+'):
                telefono = f"+56{telefono_input}"
            else:
                telefono = telefono_input
                
            direccion = self.direccion_var.get().strip()
            tipo = self.tipo_var.get()
            rut = self.rut_var.get().strip()
            
            fecha_registro = None
            if self.cliente_seleccionado and self.cliente_seleccionado.id == cliente_id:
                fecha_registro = self.cliente_seleccionado.fecha_registro
            
            if tipo == "Regular":
                puntos = int(self.puntos_var.get() or 0)
                cliente = ClienteRegular(cliente_id, nombre, email, telefono, direccion, rut, puntos, fecha_registro)
                
            elif tipo == "Premium":
                nivel = self.nivel_var.get()
                cliente = ClientePremium(cliente_id, nombre, email, telefono, direccion, rut, nivel, fecha_registro)
                
                beneficios = self.beneficios_var.get().strip()
                if beneficios:
                    for benef in beneficios.split(','):
                        benef_limpio = benef.strip()
                        if benef_limpio:
                            cliente.agregar_beneficio(benef_limpio)
                            
            elif tipo == "Corporativo":
                empresa = self.empresa_var.get().strip()
                contacto = self.contacto_var.get().strip() or None
                
                cliente = ClienteCorporativo(cliente_id, nombre, email, telefono, 
                                           direccion, rut, empresa, contacto, fecha_registro)
            
            else:
                messagebox.showerror("Error", "Tipo de cliente no válido")
                return
            
            if self.db_manager.guardar_cliente(cliente):
                self._actualizar_status(f"Cliente {nombre} guardado correctamente")
                self._cargar_clientes()
                
                if messagebox.askyesno("Email de Bienvenida", 
                                      "¿Desea enviar un email de bienvenida al cliente?"):
                    self._enviar_email_bienvenida(cliente)
                
                messagebox.showinfo("Éxito", f"Cliente {nombre} guardado correctamente")
            else:
                messagebox.showerror("Error", "No se pudo guardar el cliente")
            
        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar cliente: {str(e)}")
            self.logger.log_error_detallado(e, "Guardar cliente")
    
    def _enviar_email_bienvenida(self, cliente):
        try:
            def enviar_email():
                service = NotificationService()
                if service.enviar_email_bienvenida(cliente):
                    self.root.after(0, lambda: messagebox.showinfo(
                        "Email Enviado", 
                        f"Email de bienvenida enviado a {cliente.email}"
                    ))
                else:
                    self.root.after(0, lambda: messagebox.showwarning(
                        "Email No Enviado", 
                        "No se pudo enviar el email de bienvenida"
                    ))
            
            threading.Thread(target=enviar_email, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo enviar el email: {str(e)}")
    
    def _eliminar_cliente(self):
        if not self.cliente_seleccionado:
            messagebox.showwarning("Selección", "Seleccione un cliente para eliminar")
            return
        
        nombre = self.cliente_seleccionado.nombre
        cliente_id = self.cliente_seleccionado.id
        
        if messagebox.askyesno("Confirmar Eliminación", 
                              f"¿Está seguro de eliminar al cliente {nombre}?"):
            if self.db_manager.eliminar_cliente(cliente_id):
                self._actualizar_status(f"Cliente {nombre} eliminado")
                self._cargar_clientes()
                self._limpiar_formulario()
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
            else:
                messagebox.showerror("Error", "No se pudo eliminar el cliente")
    
    def _buscar_clientes(self):
        criterio = self.search_var.get().strip()
        
        if not criterio:
            self._cargar_clientes()
            return
        
        try:
            clientes_nombre = self.db_manager.buscar_clientes("nombre", criterio)
            clientes_email = self.db_manager.buscar_clientes("email", criterio)
            
            todos_ids = set()
            resultados = []
            
            for cliente in clientes_nombre + clientes_email:
                if cliente.id not in todos_ids:
                    todos_ids.add(cliente.id)
                    resultados.append(cliente)
            
            self.clientes = resultados
            self._actualizar_lista_clientes()
            self._actualizar_status(f"Búsqueda completada: {len(resultados)} resultados")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en búsqueda: {str(e)}")
    
    def _actualizar_logs(self):
        try:
            logs = self.db_manager.obtener_logs(20)
            
            self.log_text.delete(1.0, tk.END)
            
            for log in logs:
                log_id, timestamp, accion, detalles, usuario = log
                linea = f"{timestamp} - {accion}"
                if detalles:
                    linea += f" - {detalles}"
                self.log_text.insert(tk.END, linea + "\n")
            
            self.log_text.insert(tk.END, "\n=== LOGS DEL SISTEMA ===\n")
            logs_sistema = self.logger.obtener_logs_recientes(10)
            for log_line in logs_sistema:
                self.log_text.insert(tk.END, log_line)
            
        except Exception as e:
            self.log_text.insert(tk.END, f"Error al cargar logs: {str(e)}\n")
    
    def _exportar_json(self):
        try:
            if not self.clientes:
                messagebox.showwarning("Exportar", "No hay clientes para exportar")
                return
            
            ruta = self.json_manager.exportar_clientes(self.clientes)
            
            if ruta:
                messagebox.showinfo("Exportación Exitosa", 
                                  f"Clientes exportados a:\n{ruta}")
                self._actualizar_status(f"Exportación completada: {ruta}")
            else:
                messagebox.showerror("Error", "No se pudo exportar los clientes")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error en exportación: {str(e)}")
    
    def _exportar_csv(self):
        try:
            if not self.clientes:
                messagebox.showwarning("Exportar", "No hay clientes para exportar")
                return
            
            ruta = self.json_manager.exportar_clientes_csv(self.clientes)
            
            if ruta:
                messagebox.showinfo("Exportación Exitosa", f"Clientes exportados a CSV:\n{ruta}")
                self._actualizar_status(f"Exportación CSV completada: {ruta}")
            else:
                messagebox.showerror("Error", "No se pudo exportar a CSV")
        except Exception as e:
            messagebox.showerror("Error", f"Error en exportación CSV: {str(e)}")

    def _crear_backup(self):
        try:
            ruta = self.json_manager.crear_backup(self.db_manager)
            
            if ruta:
                messagebox.showinfo("Backup Completado", 
                                  f"Backup creado exitosamente:\n{ruta}")
                self._actualizar_status(f"Backup creado: {ruta}")
                
                self.logger.crear_backup_logs()
            else:
                messagebox.showerror("Error", "No se pudo crear el backup")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear backup: {str(e)}")
    
    def _actualizar_status(self, mensaje):
        self.status_var.set(mensaje)
        self.logger.log(mensaje, "INFO")
    
    def run(self):
        self._actualizar_status("Sistema GIC iniciado correctamente")
        self.root.mainloop()