from fastapi import FastAPI, HTTPException


app = FastAPI()

class Primeros100:
    def __init__(self):
        # Creamos el conjunto de los primeros 100 números
        self.conjunto_modificable = set(range(0, 100))
        self.conjunto_original = set(range(0, 100))

    def extract(self, n: int):
        """Extrae un número del conjunto si es válido"""
        
        if n < 0 or n > 99:
            raise ValueError("El número debe estar entre 0 y 99")
       
        self.conjunto_modificable.remove(n)
        

    def find_missing(self):
        """Devuelve el número que fue extraído"""
        numero_extraido= self.conjunto_original- self.conjunto_modificable
        if not numero_extraido :
            return "No se ha extraído ningún número aún"
        return numero_extraido


# Instancia global de la clase
conjunto = Primeros100()

@app.get("/")
def root():
    return {
        "mensaje": "Bienvenido a la API de Primeros 100 números",
        "instrucciones": "Usa el endpoint /extract/{numero} para extraer un número. Ejemplo: /extract/42"
    }

@app.get("/extract/{numero}")
def extraer_numero(numero: int):
    """Extrae un número del conjunto y devuelve el faltante"""
    try:
        conjunto.extract(numero)
        numero_extraido= conjunto.find_missing()
        conjunto.conjunto_modificable = set(range(0, 100))
        return {
            "mensaje": f"Se extrajo el número {numero_extraido}",
                   }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))