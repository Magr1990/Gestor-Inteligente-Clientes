import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
from datetime import datetime

class NotificationService:
    
    def __init__(self, config_file=None):
        if config_file is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            if os.path.basename(base_dir) == "api_integrations":
                base_dir = os.path.dirname(base_dir)
            config_file = os.path.join(base_dir, "config", "email_config.json")
            
        self.config = self._cargar_configuracion(config_file)
    
    def _cargar_configuracion(self, config_file):
        config_default = {
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "sender_email": "notificaciones@solutiontech.com",
            "sender_password": "",
            "use_tls": True
        }
        
        try:
            with open(config_file, 'r') as f:
                user_config = json.load(f)
                config_default.update(user_config)
            
            if config_default.get("sender_password"):
                config_default["sender_password"] = config_default["sender_password"].replace(" ", "")
                
        except FileNotFoundError:
            print(f"⚠️ Archivo de configuración no encontrado en: {os.path.abspath(config_file)}")
            print("Usando configuración por defecto (requiere ajustes)")
        
        return config_default
    
    def enviar_email_bienvenida(self, cliente, asunto=None, mensaje_personalizado=None):
        
        if not self.config.get("sender_password"):
            print("Error: Contraseña de email no configurada")
            return False
        
        try:
            msg = MIMEMultipart()
            
            if not asunto:
                asunto = f"¡Bienvenido a SolutionTech, {cliente.nombre}!"
            
            msg['Subject'] = asunto
            msg['From'] = self.config["sender_email"]
            msg['To'] = cliente.email
            
            if not mensaje_personalizado:
                mensaje = self._construir_mensaje_bienvenida(cliente)
            else:
                mensaje = mensaje_personalizado
            
            msg.attach(MIMEText(mensaje, 'html'))
            
            with smtplib.SMTP(self.config["smtp_server"], self.config["smtp_port"]) as server:
                if self.config.get("use_tls", True):
                    server.starttls()
                
                server.login(self.config["sender_email"], self.config["sender_password"])
                server.send_message(msg)
            
            print(f"Email de bienvenida enviado a: {cliente.email}")
            return True
            
        except smtplib.SMTPAuthenticationError:
            print("❌ Error de autenticación: El correo o la contraseña son incorrectos.")
            print("   Si usas Gmail, recuerda usar una 'Contraseña de Aplicación'.")
            return False
        except Exception as e:
            print(f"Error al enviar email: {e}")
            return False
    
    def _construir_mensaje_bienvenida(self, cliente):
        
        tipo_cliente = cliente.obtener_tipo()
        
        mensaje_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #4CAF50; color: white; padding: 10px; text-align: center; }}
                .content {{ padding: 20px; }}
                .benefits {{ background-color: #f9f9f9; padding: 15px; margin: 15px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 0.9em; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>¡Bienvenido a SolutionTech!</h1>
                </div>
                
                <div class="content">
                    <p>Estimado/a <strong>{cliente.nombre}</strong>,</p>
                    
                    <p>Nos complace darle la bienvenida como nuestro nuevo cliente.</p>
                    
                    <div class="benefits">
                        <h3>Detalles de su cuenta:</h3>
                        <ul>
                            <li><strong>Tipo de cliente:</strong> {tipo_cliente}</li>
                            <li><strong>Email registrado:</strong> {cliente.email}</li>
                            <li><strong>Fecha de registro:</strong> {datetime.now().strftime('%d/%m/%Y')}</li>
                        </ul>
                    </div>
                    
                    <p>Como cliente {tipo_cliente.lower()}, usted tiene acceso a:</p>
                    <ul>
                        <li>Gestión completa de su perfil</li>
                        <li>Soporte técnico prioritario</li>
                        <li>Actualizaciones regulares del sistema</li>
                        <li>Beneficios exclusivos según su tipo de cliente</li>
                    </ul>
                    
                    <p>Si tiene alguna pregunta, no dude en contactarnos.</p>
                    
                    <p>Atentamente,<br>
                    <strong>El equipo de SolutionTech</strong></p>
                </div>
                
                <div class="footer">
                    <p>Este es un mensaje automático, por favor no responda a este email.</p>
                    <p>© {datetime.now().year} SolutionTech. Todos los derechos reservados.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return mensaje_html
    
    def enviar_notificacion_general(self, destinatario, asunto, mensaje):
        try:
            msg = MIMEMultipart()
            msg['Subject'] = asunto
            msg['From'] = self.config["sender_email"]
            msg['To'] = destinatario
            
            msg.attach(MIMEText(mensaje, 'plain'))
            
            with smtplib.SMTP(self.config["smtp_server"], self.config["smtp_port"]) as server:
                if self.config.get("use_tls", True):
                    server.starttls()
                
                server.login(self.config["sender_email"], self.config["sender_password"])
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            print(f"Error al enviar notificación: {e}")
            return False