from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Dict, Optional
from datetime import datetime

class RolEmpleado(Enum):
    MESERO = "Mesero"
    BARISTA = "Barista"
    GERENTE = "Gerente"

class EstadoPedido(Enum):
    PENDIENTE = "Pendiente"
    EN_PREPARACION = "En Preparación"
    ENTREGADO = "Entregado"

class Persona(ABC):
    def __init__(self, nombre, ine):
        self.nombre = nombre
        self.ine = ine

class Cliente(Persona):
    def __init__(self, nombre, ine):
        super().__init__(nombre, ine)
        self.historial_pedidos = []
        self.puntos_fidelidad = 0
    
    def realizar_pedido(self, productos, promocion = None):
        pedido = Pedido(self, productos, promocion)
        self.historial_pedidos.append(pedido)
        self.puntos_fidelidad += len(productos)  # 1 punto por producto
        return pedido

class Empleado(Persona):
    def __init__(self, nombre, ine, rol):
        super().__init__(nombre, ine)
        self.rol = rol

class ProductoBase(ABC):
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio
        
    @abstractmethod
    def get_descripcion(self):
        pass

class Bebida(ProductoBase):
    def __init__(self, nombre, precio, tamanio, es_caliente):
        super().__init__(nombre, precio)
        self.tamanio = tamanio
        self.es_caliente = es_caliente
        self.personalizaciones = []
    
    def agregar_personalizacion(self, personalizacion):
        self.personalizaciones.append(personalizacion)
    
    def get_descripcion(self):
        desc = f"{self.nombre} ({self.tamanio}, {'caliente' if self.es_caliente else 'frío'})"
        if self.personalizaciones:
            desc += f" con {', '.join(self.personalizaciones)}"
        return desc

class Postre(ProductoBase):
    def __init__(self, nombre, precio, es_vegano, sin_gluten):
        super().__init__(nombre, precio)
        self.es_vegano = es_vegano
        self.sin_gluten = sin_gluten
    
    def get_descripcion(self):
        desc = self.nombre
        if self.es_vegano:
            desc += " (vegano)"
        if self.sin_gluten:
            desc += " (sin gluten)"
        return desc

class Inventario:
    def __init__(self):
        self.ingredientes = {}  # nombre: cantidad
    
    def agregar_ingrediente(self, nombre, cantidad):
        if nombre in self.ingredientes:
            self.ingredientes[nombre] += cantidad
        else:
            self.ingredientes[nombre] = cantidad
    
    def hay_suficiente_stock(self, ingrediente, cantidad_requerida) -> bool:
        return self.ingredientes.get(ingrediente, 0) >= cantidad_requerida
    
    def consumir_ingrediente(self, ingrediente, cantidad):
        if not self.hay_suficiente_stock(ingrediente, cantidad):
            raise ValueError(f"No hay suficiente stock de {ingrediente}")
        self.ingredientes[ingrediente] -= cantidad

class Promocion:
    def __init__(self, nombre, descuento, puntos_requeridos = 0):
        self.nombre = nombre
        self.descuento = descuento  # porcentaje de descuento (0-1)
        self.puntos_requeridos = puntos_requeridos
    
    def es_aplicable(self, cliente) -> bool:
        return cliente.puntos_fidelidad >= self.puntos_requeridos

class Pedido:
    def __init__(self, cliente, productos, promocion = None):
        self.cliente = cliente
        self.productos = productos
        self.promocion = promocion
        self.estado = EstadoPedido.PENDIENTE
        self.fecha = datetime.now()
        self.total = self.calcular_total()
    
    def calcular_total(self):
        subtotal = sum(producto.precio for producto in self.productos)
        if self.promocion and self.promocion.es_aplicable(self.cliente):
            return subtotal * (1 - self.promocion.descuento)
        return subtotal
    
    def actualizar_estado(self, nuevo_estado):
        self.estado = nuevo_estado

# Ejemplo de uso del sistema
if __name__ == "__main__":
    # Crear inventario
    inventario = Inventario()
    inventario.agregar_ingrediente("café", 1000)
    inventario.agregar_ingrediente("leche", 2000)
    inventario.agregar_ingrediente("chocolate", 500)
    
    # Crear productos
    cafe_late = Bebida("Café Latte", 4.50, "Grande", True)
    cafe_late.agregar_personalizacion("leche de almendra")
    cafe_late.agregar_personalizacion("sin azúcar")
    
    brownie = Postre("Brownie", 3.50, False, False)
    
    # Crear cliente
    cliente = Cliente("María García", "87654321B")
    
    # Crear promoción
    promocion = Promocion("Descuento Fidelidad", 0.15, puntos_requeridos=10)
    
    # Realizar pedido
    try:
        pedido = cliente.realizar_pedido([cafe_late, brownie], promocion)
        print(f"Pedido realizado con éxito. Total: ${pedido.total}")
        for producto in pedido.productos:
            print(f"- {producto.get_descripcion()}")
    except ValueError as e:
        print(f"Error al realizar el pedido: {e}")
