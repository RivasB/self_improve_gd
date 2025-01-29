# Parámetro ajustable (valor inicial: 5.0)
x = 5.0

# Tasa de aprendizaje (¡ajusta este valor para controlar la convergencia!)
learning_rate = 0.1

# Función a minimizar: f(x) = x² (su derivada es f'(x) = 2x)
def f(x):
    return x ** 2

# Calcular valor actual y gradiente
current_value = f(x)
gradiente = 2 * x  # Derivada de f(x)

# Paso de optimización: x_new = x - learning_rate * gradiente
x_new = x - learning_rate * gradiente

# Evaluar si hay mejora
if f(x_new) < current_value:
    x = x_new
    print(f"✅ Mejorado: x = {x:.4f}, f(x) = {f(x):.4f}")
else:
    print("⛔ Sin mejora (¡revisa la tasa de aprendizaje!)")

# Auto-modificación: Actualizar el valor de x en el código fuente
with open("self_improve_gd.py", "r") as file:
    code = file.readlines()

# Buscar la línea que define x y reemplazarla
for i, line in enumerate(code):
    if line.startswith("x = "):
        code[i] = f"x = {x}  # Auto-updated\n"
        break

# Guardar cambios
with open("self_improve_gd.py", "w") as file:
    file.writelines(code)
