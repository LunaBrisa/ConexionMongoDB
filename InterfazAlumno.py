from conexion import conectar_mongo
from alumno import Alumno
import os

class InterfazAlumno:
    def __init__(self):
        self.archivo = "alumnos.json"
        self.archivo_offline = "alumnos_offline.json"
        self.alumnos = Alumno()
        self.alumnos_offline = Alumno()
        
        # Cargar datos existentes sin mensajes redundantes
        if os.path.exists(self.archivo):
            self.alumnos.cargarArchivo(self.archivo, Alumno)
        if os.path.exists(self.archivo_offline):
            self.alumnos_offline.cargarArchivo(self.archivo_offline, Alumno)
        
        # Sincronizar silenciosamente al iniciar
        self._sincronizar_silencioso()

    def _sincronizar_silencioso(self):
        """Sincronización automática sin mensajes"""
        if self.alumnos_offline.items and conectar_mongo():
            for alumno in list(self.alumnos_offline.items):
                if self._guardar_en_mongo(alumno):
                    self.alumnos_offline.eliminar(item=alumno)
            self._guardar_datos()

    def _guardar_en_mongo(self, alumno):
        """Intenta guardar en MongoDB devolviendo True/False"""
        try:
            db = conectar_mongo()
            if db:
                db.Alumnos.insert_one(alumno.convertir_dict_mongo())
                return True
        except:
            return False
        return False

    def _guardar_datos(self):
        """Guarda los datos sin mensajes redundantes"""
        self.alumnos.guardarArchivo(self.archivo)
        self.alumnos_offline.guardarArchivo(self.archivo_offline)

    def menu(self):
        while True:
            print("\n--- Menú de Alumnos ---")
            print("1. Mostrar alumnos")
            print("2. Agregar alumno")
            print("3. Eliminar alumno")
            print("4. Actualizar alumno")
            print("5. Sincronizar ahora")
            print("6. Salir")

            opcion = input("Seleccione una opción: ")
            
            if opcion == "1":
                self._mostrar_alumnos()
            elif opcion == "2":
                self._agregar_alumno()
            elif opcion == "3":
                self._eliminar_alumno()
            elif opcion == "4":
                self._actualizar_alumno()
            elif opcion == "5":
                self._sincronizar_manual()
            elif opcion == "6":
                self._guardar_datos()
                break

    def _mostrar_alumnos(self):
        print("\nLISTA DE ALUMNOS:")
        for i, alumno in enumerate(self.alumnos.items, 1):
            print(f"{i}. {alumno.nombre} {alumno.apellido} - Matrícula: {alumno.matricula}")

    def _agregar_alumno(self):
        print("\nNUEVO ALUMNO")
        alumno = Alumno(
            input("Nombre: "),
            input("Apellido: "),
            int(input("Edad: ")),
            input("Matrícula: "),
            input("Sexo (M/F): ").upper()
        )

        if not self._guardar_en_mongo(alumno):
            self.alumnos_offline.agregar(alumno)
            print("(Guardado localmente - Se sincronizará automáticamente)")
        
        self.alumnos.agregar(alumno)
        self._guardar_datos()

    def _eliminar_alumno(self):
        self._mostrar_alumnos()
        try:
            idx = int(input("Número de alumno a eliminar: ")) - 1
            if 0 <= idx < len(self.alumnos.items):
                self.alumnos.eliminar(indice=idx)
                self._guardar_datos()
        except:
            print("Selección inválida")

    def _actualizar_alumno(self):
        self._mostrar_alumnos()
        try:
            idx = int(input("Número de alumno a actualizar: ")) - 1
            if 0 <= idx < len(self.alumnos.items):
                alumno = self.alumnos.items[idx]
                nuevos = {
                    'nombre': input(f"Nuevo nombre ({alumno.nombre}): ") or alumno.nombre,
                    'apellido': input(f"Nuevo apellido ({alumno.apellido}): ") or alumno.apellido,
                    'edad': int(input(f"Nueva edad ({alumno.edad}): ") or alumno.edad),
                    'matricula': input(f"Nueva matrícula ({alumno.matricula}): ") or alumno.matricula,
                    'sexo': input(f"Nuevo sexo ({alumno.sexo}): ").upper() or alumno.sexo
                }
                self.alumnos.actualizar(alumno, **nuevos)
                self._guardar_datos()
        except:
            print("Error en los datos")

    def _sincronizar_manual(self):
        pendientes = len(self.alumnos_offline.items)
        if pendientes == 0:
            print("No hay alumnos pendientes por sincronizar")
            return
        
        sincronizados = 0
        for alumno in list(self.alumnos_offline.items):
            if self._guardar_en_mongo(alumno):
                self.alumnos_offline.eliminar(item=alumno)
                sincronizados += 1
        
        self._guardar_datos()
        print(f"Alumnos sincronizados: {sincronizados}/{pendientes}")

if __name__ == "__main__":
    InterfazAlumno().menu()