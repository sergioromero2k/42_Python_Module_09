# 42_Python_Module_09
42_Python_Module_09

## Cosmic Data Observatory: Pydantic Validation

¡Bienvenido al Cosmic Data Observatory! Este proyecto ha sido diseñado para dominar Pydantic v2, la librería de validación de datos más potente de Python, a través de una serie de escenarios espaciales realistas.

Como Ingeniero de Datos Junior, tu misión es asegurar la integridad de los flujos de datos provenientes de misiones espaciales, reportes de contactos alienígenas y sistemas de monitoreo de estaciones.

### Objetivo del Proyecto

El fin principal es aprender a transformar datos crudos y potencialmente corruptos en estructuras de datos robustas, validadas y tipadas utilizando:
- Modelos base (BaseModel).
- Restricciones de campo con Field.
- Validación lógica compleja con @model_validator.
- Manejo de estructuras anidadas y Enums.

### Ejercicios y Niveles de Dificultad

| Ejercicio | Título                  | Nivel | Conceptos Clave                                      |
|-----------|-------------------------|-------|-----------------------------------------------------|
| Ex 0      | Space Station Data      | 🟢 Fácil | BaseModel, Field, Tipos básicos.                   |
| Ex 1      | Alien Contact Logs      | 🟡 Medio | Enum, @model_validator, Lógica de negocio.         |
| Ex 2      | Space Crew Management   | 🔴 Difícil | Modelos anidados, validación de listas, lógica avanzada. |

### Detalles de los Ejercicios

#### Ejercicio 0: Space Station Data
- **Objetivo:** Validar estadísticas vitales de estaciones espaciales (ID, tripulación, niveles de oxígeno y energía).
- **Reto:** Implementar conversiones automáticas de tipos (ej. strings a datetime) y límites numéricos estrictos.

#### Ejercicio 1: Alien Contact Logs
- **Objetivo:** Gestionar reportes de contacto extraterrestre con reglas de negocio dinámicas.
- **Reglas Críticas:**
  - Los reportes físicos deben estar verificados.
  - Contactos telepáticos requieren al menos 3 testigos.
  - Señales fuertes (> 7.0) deben incluir un mensaje.

#### Ejercicio 2: Space Crew Management
- **Objetivo:** Validar misiones completas que contienen listas de tripulantes.
- **Reglas Críticas:**
  - Toda misión debe tener al menos un Capitán o Comandante.
  - Misiones largas (> 365 días) exigen que el 50% de la tripulación sea experimentada.

### Normas y Requisitos

#### Obligatorio
- **Versión de Python:** 3.10 o superior.
- **Librería:** Pydantic 2.x (prohibido usar sintaxis de la v1 como @validator).
- **Estructura:** Cada ejercicio debe estar en su carpeta correspondiente (ex0/, ex1/, ex2/).
- **Función Main:** Todos los archivos deben incluir una función main() que demuestre casos de éxito y casos de error de validación.

#### Prohibido / Restricciones
- **Importaciones:** Solo se permite la librería estándar de Python (json, datetime, csv, etc.) y las herramientas de generación de datos proporcionadas.
- **Decoradores obsoletos:** No utilizar @validator; usar exclusivamente @model_validator(mode='after').

### Guía de Resolución: Pasos a seguir
1. **Configuración:** Crea un entorno virtual e instala Pydantic 2.x (pip install pydantic).
2. **Modelado:** Define tus clases heredando de BaseModel.
3. **Restricciones:** Usa Field(ge=..., le=..., min_length=...) para las validaciones básicas de cada atributo.
4. **Lógica Cruzada:** Para reglas que dependan de varios campos (ej. "si el contacto es físico, entonces verificado"), implementa el @model_validator.
5. **Pruebas:** Usa las herramientas data_generator.py incluidas para testear tus modelos con datos masivos.

### Entrega
Asegúrate de que los nombres de los archivos sean exactos:
- `ex0/space_station.py`
- `ex1/alien_contact.py`
- `ex2/space_crew.py`