import flet as ft
from restaurante import Restaurante
from mesa import Mesa
from cliente import Cliente


class RestauranteGUI:
    def __init__(self):
        self.restaurante = Restaurante()
        capacidades = [2,4,6,8,10,12,14,16]
        for i in range(1, 8):
            self.restaurante.agregar_mesa(Mesa(i, capacidades[i -1]))

    def main(self, page: ft.Page):
        page.padding= 20
        page.theme_mode = "dark"

        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Mesera",
                    icon=ft.icons.PERSON,
                    content= self.crear_vista_mesera(),
                ),
                 ft.Tab(
                    text="Cocina",
                    icon=ft.icons.RESTAURANT,
                    # content=
                ),
                 ft.Tab(
                    text="Cajero",
                    icon=ft.icons.POINT_OF_SALE,
                    # content=
                ),
                 ft.Tab(
                    text="Administrador",
                    icon=ft.icons.ADMIN_PANEL_SETTINGS,
                    # content=
                ),
            ],
            expand=1,
        )

        page.add(self.tabs)

    # Metodos de Vistas
    def crear_vista_mesera(self):
        self.grid_container = ft.Container(
            content=self.crear_grid_mesas(),
            width=700,
            expand=True,
        )

        return ft.Row(
            controls=[
                ft.Container(
                    width=700,
                    content=ft.Column(
                        [
                            ft.Text(
                                "Mesera del Restaurante",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                            ),
                            self.grid_container,
                        ],
                        expand=True,
                    ),
                    expand=True,
                ),
                ft.VerticalDivider(),
                ft.Container(
                    width=400,
                    content=self.crear_panel_gestion(),
                    expand=True
                )
            ],
            expand=True,
            spacing=0,
        )

    # Metodos internos de vistas
    def crear_grid_mesas(self):
        grid = ft.GridView(
            expand=1,
            runs_count=2,
            max_extent=200,
            child_aspect_ratio=1.0,
            spacing=10,
            run_spacing=10,
            padding=10
        )

        for mesa in self.restaurante.mesas:
            color = ft.colors.GREEN_700 if not mesa.ocupada else ft.colors.RED_700
            estado = "Libre" if not mesa.ocupada else "Ocupada"

            grid.controls.append(
                ft.Container(
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=5,
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Icon(
                                        ft.icons.TABLE_RESTAURANT,
                                        color=ft.colors.AMBER_400,
                                    ),
                                    ft.Text(
                                        f"Mesa {mesa.numero}",
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                ],
                            ),
                            ft.Text(f"Capacidad: {mesa.tamaño} personas", size=14),
                            ft.Text(
                                estado,
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.WHITE
                            ),
                        ]
                    ),
                    bgcolor=color,
                    border_radius=10,
                    padding=15,
                    ink =True,
                    on_click= lambda e, mesa=mesa: self.seleccionar_mesa(e, mesa)
                )
            )
        return grid
    
    def actualizar_ui(self, page):
        nuevo_grid = self.crear_grid_mesas()
        self.grid_container.content = nuevo_grid

        if self.mesa_seleccionada:
            if self.mesa_seleccionada.ocupada and self.mesa_seleccionada.pedido_actual:
                self.resume_pedido.value = self.mesa_seleccionada.pedido_actual.obtener_resumen()
            else:
                self.resume_pedido.value = ""

            self.asignar_btn.disabled = self.mesa_seleccionada.ocupada
            self.agregar_item_btn.disabled = not self.mesa_seleccionada.ocupada
            self.liberar_btn.disabled = not self.mesa_seleccionada.ocupada
        page.update()

    def seleccionar_mesa(self, e, mesa):
      self.mesa_seleccionada = mesa
      self.mesa_info.value = f"Mesa {mesa.numero} - Capacidad: {mesa.tamaño} personas"
      self.asignar_btn.disabled = mesa.ocupada

    # Actualiza la UI
      e.page.update()

    
    def crear_panel_gestion(self):
        self.mesa_seleccionada = None
        self.mesa_info = ft.Text("", size=16, weight=ft.FontWeight.BOLD)
        self.tamaño_grupo_input = ft.TextField(
            label="Tamaño del Grupo",
            input_filter=ft.NumbersOnlyInputFilter(),
            prefix_icon=ft.icons.PEOPLE
        )

        self.tipo_item_dropdown= ft.Dropdown(
            label="Tipo de Item",
            options=[
                ft.dropdown.Option("Entrada"),
                ft.dropdown.Option("Postre"),
                ft.dropdown.Option("Bebida"),
                ft.dropdown.Option("Plato Principal"),
            ],
            width=200,
            on_change=self.actualizar_items_menu
        )

        self.items_dropdown = ft.Dropdown(
            label="Selecionar Item",
            width=200,
        )

        self.asignar_btn = ft.ElevatedButton(
            text="Asignar Cliente",
            on_click=self.asignar_cliente,
            disabled=True,
            style=ft.ButtonStyle(
                bgcolor=ft.colors.GREEN_700,
                color=ft.colors.WHITE,
            )
        )
        self.agregar_item_btn = ft.ElevatedButton(
            text="Agregar Item",
            on_click=self.agregar_item_pedido,
            disabled=True,
            style=ft.ButtonStyle(
                bgcolor=ft.colors.BLUE_600,
                color=ft.colors.WHITE,
            )
        )

        self.liberar_btn= ft.ElevatedButton(
            text="Liberar Mesa",
            on_click=self.liberar_mesa,
            disabled=True,
            style=ft.ButtonStyle(
                bgcolor=ft.colors.RED_700,
                color=ft.colors.WHITE,
            )
        )

        self.resumen_pedido = ft.Text("", size=14)

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=self.mesa_info,
                        bgcolor=ft.colors.BLUE_GREY_900,
                        padding=10,
                        border_radius=10,
                    ),
                    #Panel de Gestion.
                    ft.Container(height=20),
                    self.tamaño_grupo_input,
                    self.asignar_btn,
                    ft.Divider(),
                    self.tipo_item_dropdown,
                    self.items_dropdown,
                    self.agregar_item_btn,
                    ft.Divider(),
                    self.liberar_btn,
                    ft.Divider(),
                    ft.Text("Resumen del pedido:", size=16, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=self.resumen_pedido,
                        bgcolor=ft.colors.BLUE_GREY_900,
                        padding=10,
                        border_radius=10,
                    ),
                  
                ],
                spacing=10,
                expand=True,
            ),
            padding=20,
            expand=True,
        )

    def asignar_cliente(self, e):
        if not self.mesa_seleccionada:
            return

        try:
            tamaño_grupo = int(self.tamaño_grupo_input.value)
            if tamaño_grupo <= 0:
                return

            cliente = Cliente(tamaño_grupo)
            resultado = self.restaurante.asignar_cliente_a_mesa(
                    cliente, self.mesa_seleccionada.numero
                )

            if "asignar" in resultado:
                self.restaurante.crear_pedido(self.mesa_seleccionada.numero)
                self.tamaño_grupo_input.value = ""
                self.actualizar_ui(e.page)
                
        except ValueError:
            print("Error de pedido vuelva a intentarlo")

    def actualizar_items_menu(self, e):
        tipo= self.tipo_item_dropdown.value
        self.items_dropdown.options=[]

        if tipo == "Entrada":
            items = self.restaurante.menu.entradas
        elif tipo == "Plato Principal":
            items = self.restaurante.menu.platos_principales
        elif tipo == "Postre":
            items = self.restaurante.menu.postres
        elif tipo == "Bebida":
            items = self.restaurante.menu.bebidas
        else:
            items =[]

        self.items_dropdown.options=[
            ft.dropdown.Option(item.nombre) for item in items
        ]
        if e and e.page:
            e.page.update()
    
    def agregar_item_pedido(self,e):
        if not self.mesa_seleccionada or not self.mesa_seleccionada.pedido_actual:
            return
        
        tipo = self.tipo_item_dropdown.value
        nombre_item = self.nombre_item_dropdown.value

        if tipo and nombre_item:
            item= self.restaurante.obtener_item_menu(tipo, nombre_item)
            if item:
                self.mesa_seleccionada.pedido_actual.agregar_item(item)
                self.actualizar_ui(e.page)

    def liberar_mesa(self, e):
        if self.mesa_seleccionada:
           self.restaurante.liberar_mesa(self.mesa_seleccionada.numero)
           self.actualizar_ui(e.page)



def main():
    app = RestauranteGUI()
    ft.app(target=app.main)

if __name__ == "__main__":
    main()

