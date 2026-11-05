
import cv2
from detector.camara import DetectorPersonas


# Inicializar el detector de personas
detector = DetectorPersonas()

# Abrir la cámara principal de la computadora
camara = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not camara.isOpened():
    print("ERROR: No se pudo abrir la cámara.")
    exit()

print("Cámara iniciada correctamente.")
print("Presiona la tecla Q para cerrar la prueba.")

while True:
    # Capturar un fotograma
    correcto, imagen = camara.read()

    if not correcto:
        print("No se pudo capturar la imagen.")
        break

    # Detectar personas con YOLOv8
    imagen, total = detector.detectar(imagen)

    # Mostrar la cantidad detectada
    cv2.putText(
        imagen,
        f"Personas detectadas: {total}",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 200, 100),
        2
    )

    # Mostrar video en una ventana
    cv2.imshow("LabCount - Prueba de Camara", imagen)

    # Presionar Q para salir
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Liberar los recursos
camara.release()
cv2.destroyAllWindows()

print("Prueba finalizada.")
