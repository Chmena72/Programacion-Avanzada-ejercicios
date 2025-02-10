from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from enum import Enum

class EstadoMaterial(Enum):
    DISPONIBLE = "Disponible"
    PRESTADO = "Prestado"
    EN_REPARACION = "En Reparación"

class Material(ABC):
    def __init__(self, titulo, codigo):
        self.titulo = titulo
        self.codigo = codigo
        self.estado = EstadoMaterial.DISPONIBLE
    
    @abstractmethod
    def get_info(self):
        pass

class Libro(Material):
    def __init__(self, titulo, codigo, autor, genero):
        super().__init__(titulo, codigo)
        self.autor = autor
        self.genero = genero
    
    def get_info(self):
        return f"{self.titulo} por {self.autor} ({self.genero})"

class Revista(Material):
    def __init__(self, titulo, codigo, edicion, periodicidad):
        super().__init__(titulo, codigo)
        self.edicion = edicion
        self.periodicidad = periodicidad
    
    def get_info(self):
        return f"{self.titulo} - Edición {self.edicion} ({self.periodicidad})"

class MaterialDigital(Material):
    def __init__(self, titulo, codigo, tipo_archivo, url):
        super().__init__(titulo, codigo)
        self.tipo_archivo = tipo_archivo
        self.url = url
    
    def get_info(self):
        return f"{self.titulo} ({self.tipo_archivo}) - {self.url}"

class Persona(ABC):
    def __init__(self, nombre, ine):
        self.nombre = nombre
        self.ine = ine

class Usuario(Persona):
    def __init__(self, nombre, ine):
        super().__init__(nombre, ine)
        self.historial_prestamos = []
        self.reservas = []
    
    def realizar_prestamo(self, material, fecha_devolucion):
        if material.estado != EstadoMaterial.DISPONIBLE:
            raise ValueError("El material no está disponible para préstamo")
        prestamo = Prestamo(self, material, fecha_devolucion)
        self.historial_prestamos.append(prestamo)
        material.estado = EstadoMaterial.PRESTADO
        return prestamo
    
    def reservar_material(self, material):
        if material.estado != EstadoMaterial.DISPONIBLE:
            raise ValueError("El material no está disponible para reserva")
        reserva = Reserva(self, material)
        self.reservas.append(reserva)
        return reserva

class Prestamo:
    def __init__(self, usuario, material, fecha_devolucion):
        self.usuario = usuario
        self.material = material
        self.fecha_prestamo = datetime.now()
        self.fecha_devolucion = fecha_devolucion
    
    def devolver_material(self):
        self.material.estado = EstadoMaterial.DISPONIBLE

class Reserva:
    def __init__(self, usuario, material):
        self.usuario = usuario
        self.material = material
        self.fecha_reserva = datetime.now()

class Biblioteca:
    def __init__(self):
        self.materiales = []
        self.usuarios = []
    
    def agregar_material(self, material):
        self.materiales.append(material)
    
    def registrar_usuario(self, usuario):
        self.usuarios.append(usuario)
    
    def listar_materiales(self):
        for material in self.materiales:
            print(material.get_info())

# Ejemplo de uso del sistema
if __name__ == "__main__":
    biblioteca = Biblioteca()
    
    # Crear materiales
    libro = Libro("Cien Años de Soledad", "001", "Gabriel García Márquez", "Realismo Mágico")
    revista = Revista("National Geographic", "002", "Marzo 2023", "Mensual")
    material_digital = MaterialDigital("Curso de Python", "003", "PDF", "http://example.com/curso-python")
    
    # Agregar materiales a la biblioteca
    biblioteca.agregar_material(libro)
    biblioteca.agregar_material(revista)
    biblioteca.agregar_material(material_digital)
    
    # Crear un usuario
    usuario = Usuario("Juan Pérez", "12345678A")
    biblioteca.registrar_usuario(usuario)
    
    # Realizar un préstamo
    try:
        prestamo = usuario.realizar_prestamo(libro, datetime.now() + timedelta(days=14))
        print(f"Préstamo realizado con éxito. Devolución el {prestamo.fecha_devolucion}.")
    except ValueError as e:
        print(f"Error al realizar el préstamo: {e}")
    
    # Reservar un material
    try:
        reserva = usuario.reservar_material(revista)
        print("Reserva realizada con éxito.")
    except ValueError as e:
        print(f"Error al realizar la reserva: {e}")
    
    # Listar materiales de la biblioteca
    print("Materiales en la biblioteca:")
    biblioteca.listar_materiales()