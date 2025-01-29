import numpy as np
import os
from datetime import datetime

# ===== CONFIGURACIÓN INICIAL =====
SIMULATION_MODE = False  # Cambiar a True para pruebas sin auto-modificación
MAX_ITERATIONS = 100     # Máximo de ejecuciones permitidas
SAFETY_BACKUP = True     # Hacer copia de seguridad del código
ETHICAL_CONSTRAINT = True  # Bloquear valores negativos de x

# Parámetros iniciales
x = 5.0                  # Valor inicial
learning_rate = 0.1      # Tasa de aprendizaje inicial
beta1 = 0.9              # Parámetro de momento (Adam)
beta2 = 0.999            # Parámetro de adaptación (Adam)
epsilon = 1e-8           # Estabilidad numérica
m = 0.0                  # Primer momento (Adam)
v = 0.0                  # Segundo momento (Adam)
iteration = 0            # Contador de iteraciones

# Función a optimizar
def f(x):
    return x ** 2

# Gradiente de la función
def gradient(x):
    return 2 * x

# ===== OPTIMIZACIÓN =====
current_value = f(x)
grad = gradient(x)

# Algoritmo Adam (adaptación de tasa de aprendizaje)
m = beta1 * m + (1 - beta1) * grad
v = beta2 * v + (1 - beta2) * (grad ** 2)
m_hat = m / (1 - beta1 ** (iteration + 1))
v_hat = v / (1 - beta2 ** (iteration + 1))
x_new = x - learning_rate * m_hat / (np.sqrt(v_hat) + epsilon)

# Validación ética: x no puede ser negativo
if ETHICAL_CONSTRAINT and x_new < 0:
    x_new = 0.0

# Verificar mejora
improved = f(x_new) < current_value

# ===== REGISTRO DE MÉTRICAS =====
log_entry = (
    f"{datetime.now()}, Iteración: {iteration}, "
    f"x: {x:.4f}, f(x): {current_value:.4f}, "
    f"Learning Rate: {learning_rate:.6f}, Mejora: {improved}\n"
)

with open("optimization_log.csv", "a") as log_file:
    log_file.write(log_entry)

# ===== CONDICIÓN DE PARADA =====
if np.abs(x) < 1e-5 or iteration >= MAX_ITERATIONS:
    print("🔴 Condición de parada alcanzada!")
    print(f"x_final = {x:.6f}, f(x) = {f(x):.6f}")
    exit()

# ===== AUTO-MODIFICACIÓN DEL CÓDIGO =====
if not SIMULATION_MODE:
    try:
        # Crear backup del código
        if SAFETY_BACKUP:
            backup_name = f"backup_self_improve_{datetime.now().strftime('%Y%m%d%H%M%S')}.py"
            os.system(f"cp self_improve_advanced.py {backup_name}")

        # Leer el código actual
        with open("self_improve_advanced.py", "r") as file:
            code_lines = file.readlines()

        # Actualizar parámetros en el código
        updates = {
            "x = ": f"x = {x_new}  # Auto-updated\n",
            "learning_rate = ": f"learning_rate = {learning_rate}  # Auto-updated\n",
            "iteration = ": f"iteration = {iteration + 1}\n",
            "m = ": f"m = {m}\n",
            "v = ": f"v = {v}\n"
        }

        # Buscar y reemplazar líneas
        for i, line in enumerate(code_lines):
            for key in updates:
                if line.startswith(key):
                    code_lines[i] = updates[key]
                    break

        # Guardar cambios
        with open("self_improve_advanced.py", "w") as file:
            file.writelines(code_lines)

        print(f"🟢 Código actualizado: x = {x_new:.4f}")

    except Exception as e:
        print(f"🔴 Error: {e}. Restaurando backup...")
        if SAFETY_BACKUP:
            os.system(f"cp {backup_name} self_improve_advanced.py")
        exit()

else:
    print(f"🔵 Simulación: Nuevo x sería {x_new:.4f} (no se modificó el archivo)")
