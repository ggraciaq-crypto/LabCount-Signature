
import cv2
from ultralytics import YOLO


class DetectorPersonas:

    def __init__(self):
        self.modelo = YOLO("yolov8n.pt")
        self.total_personas = 0

    def detectar(self, imagen):

        resultados = self.modelo.predict(
            source=imagen,
            classes=[0],
            conf=0.55,
            iou=0.40,
            imgsz=640,
            max_det=20,
            verbose=False
        )

        cajas = []

        for resultado in resultados:
            for caja in resultado.boxes:

                x1, y1, x2, y2 = map(
                    int,
                    caja.xyxy[0].tolist()
                )

                cajas.append((x1, y1, x2, y2))

        cajas_filtradas = []

        for caja in cajas:
            x1, y1, x2, y2 = caja

            duplicada = False

            for existente in cajas_filtradas:
                ex1, ey1, ex2, ey2 = existente

                inter_x1 = max(x1, ex1)
                inter_y1 = max(y1, ey1)
                inter_x2 = min(x2, ex2)
                inter_y2 = min(y2, ey2)

                ancho_inter = max(0, inter_x2 - inter_x1)
                alto_inter = max(0, inter_y2 - inter_y1)

                area_inter = ancho_inter * alto_inter

                area_caja = (x2 - x1) * (y2 - y1)
                area_existente = (ex2 - ex1) * (ey2 - ey1)

                area_menor = min(area_caja, area_existente)

                if area_menor > 0:
                    superposicion = area_inter / area_menor

                    if superposicion > 0.60:
                        duplicada = True
                        break

            if not duplicada:
                cajas_filtradas.append(caja)

        self.total_personas = len(cajas_filtradas)

        for x1, y1, x2, y2 in cajas_filtradas:

            cv2.rectangle(
                imagen,
                (x1, y1),
                (x2, y2),
                (0, 200, 100),
                2
            )

            cv2.putText(
                imagen,
                "Persona",
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 200, 100),
                2
            )

        return imagen, self.total_personas
