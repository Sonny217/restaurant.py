class Cliente:
    _next_id = 1 # Variable de clase para mantener el siguinete ID


    def __init__(self, tamaño_grupo):
        self.id = f"C{Cliente._next_id:03d}" #formato: c001, c002 etc.
        Cliente._next_id +=1
        self.tamaño_grupo = tamaño_grupo
        self.pedido_actual = None

    def asignar_pedido(self, pedido):
        self.pedido_actual = pedido
    
    def obtener_total_actual(self):
        return self.pedido_actual.total if self.pedido_actual else 0
    
    def limpiar_pedido(self):
        self.pedido_actual = None

    @classmethod
    def reiniciar_comtador(cls):
        cls._next_id = 1

