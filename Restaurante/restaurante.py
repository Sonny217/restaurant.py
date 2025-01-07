
from menu import Menu
from pedido import Pedido

class Restaurante:
    def __init__(self):
     self.mesas = []
     self.clientes = []
     self.pedidos_activos = []
     self.menu = Menu()
     self._inicializar_menu()

    def _inicializar_menu(self):
      #agregar algunas entradas
     self.menu.agregar_entrada("Ensalada César", 15.50)
     self.menu.agregar_entrada("Ensalada de lechuga", 10.50)
     self.menu.agregar_entrada("Guacamole Snack", 5.50)

     #agregar platos principales
     self.menu.agregar_plato_principal("PicaPollos", 25.50)
     self.menu.agregar_plato_principal("Pescado Frito", 30.50)
     self.menu.agregar_plato_principal("Solomillo con salsa verde", 20.20)
     
     #agregar postres
     self.menu.agregar_postro("Tarta Sacher", 15.00)
     self.menu.agregar_postro("Torta de manzana", 18.00)
     self.menu.agregar_postro("Copas de crema de vainilla", 12.14)
     
     #agregar bebidas
     self.menu.agregar_bebida("Coca-Cola", 3.50)
     self.menu.agregar_bebida("Agua mineral", 2.50)
     self.menu.agregar_bebida("Coors Light", 16.00)

    def agregar_mesa(self, mesa):
       self.mesas.append(mesa)
       return f"Mesa {mesa.numero} (Capacidad : {mesa.tamaño}) agregada con éxito"

    def asignar_cliente_a_mesa(self, cliente, numero_mesa):
       mesa = self.buscar_mesa(numero_mesa)
       if not mesa:
         return "Mesa no encontrada"
       if mesa.ocupada:
         return "Mesa ocupada"
       if cliente.tamaño_grupo > mesa.tamaño:
         return f"El tamaño del grupo del cliente es mayor que la capacidad de la mesa (Capacidad Máxima: {mesa.tamaño})"
       if mesa.asignar_cliente(cliente):
         self.clientes.append(cliente)
         return f"Cleinte {cliente.id} asignado a mesa {numero_mesa}"
       return " No se  puedo asignar el cliente a la mesa"

    def buscar_mesa(self, numero_mesa):
       for mesa in self.mesas:
         if mesa.numero == numero_mesa:
           return mesa
         return None
       
    def crear_pedido(self, numero_mesa):
      mesa = self.buscar_mesa(numero_mesa)
      if mesa and mesa.ocupada:
        Pedido= Pedido(mesa)
        self.pedidos_activos.append(Pedido)
        mesa.pedidos_actual = Pedido
        mesa.cliente.asignar_pedido(Pedido)
        return Pedido
      return None
    
    def liberar_mesa(self, numero_mesa):
      mesa =self.buscar_mesa(numero_mesa)
      if mesa:
        cliente = mesa.cliente
        if cliente:
          cliente.limpiar_pedido()
          if cliente in self.clientes:
            self.clientes.remove(cliente)
          if mesa.pedido_actual in self.pedidos_activos:
            self.pedidos_activos.remove(mesa.pedido_actual)
        mesa.liberar()
        return f"Mesa{numero_mesa} liberada"
      return "Mesa No encontrada"
    
    
    def obtener_item_menu(self, tipo, nombre):
      return self.menu.obtener_item(tipo, nombre)