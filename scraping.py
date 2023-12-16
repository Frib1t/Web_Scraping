import signal
import sys
import time
import requests


class WebScraping:
    def __init__(self, url):
        self.url = url
        self.html = documento_html(url)

    def imagenes(self):
        buscar = self.html.find("<img")
        links = []

        while buscar != -1:
            inicio_src = self.html.find("src=", buscar)
            fin_src = self.html.find('"', inicio_src + 5)
            enlace = self.html[inicio_src + 5: fin_src]
            links.append(enlace)
            buscar = self.html.find("<img", fin_src)
        return links

    def enlaces(self):
        buscar = 0  # Inicia la búsqueda desde el principio del HTML
        links = []
        while True:
            inicio_a = self.html.find("<a", buscar)
            if inicio_a == -1:
                break
            inicio_href = self.html.find("href=", inicio_a)
            if inicio_href == -1:
                buscar = inicio_a + 2
                continue
            inicio_link = self.html.find('"', inicio_href)
            fin_link = self.html.find('"', inicio_link + 1)
            enlace = self.html[inicio_link + 1: fin_link]
            links.append(enlace)
            buscar = fin_link

        return links

    def hojas_estilo(self):
        buscar = 0
        links = []

        while True:
            inicio_link = self.html.find("<link", buscar)
            if inicio_link == -1:
                break
            inicio_href = self.html.find("href=", inicio_link)
            if inicio_href == -1:
                buscar = inicio_link + 2
                continue
            inicio_href = self.html.find('"', inicio_href)
            fin_href = self.html.find('"', inicio_href + 1)
            enlace = self.html[inicio_href + 1: fin_href]
            links.append(enlace)
            buscar = fin_href
        return links

    def scripts(self):
        buscar = 0
        links = []

        while True:
            inicio_script = self.html.find("<script", buscar)
            if inicio_script == -1:
                break
            fin_src = self.html.find(">", inicio_script)
            fin_script = self.html.find("</script>", inicio_script)
            if fin_script == -1 or (fin_src != -1 and fin_script > fin_src):
                contenido_script = self.html[fin_src + 1: fin_script]
                links.append(contenido_script)
            else:
                inicio_src = self.html.find("src=", inicio_script)
                if inicio_src != -1 and inicio_src < fin_script:
                    inicio_src = self.html.find('"', inicio_src)
                    fin_src = self.html.find('"', inicio_src + 1)
                    enlace = self.html[inicio_src + 1: fin_src]
                    links.append(enlace)

            buscar = fin_script
        return links


def def_handler(sig, frame):
    print("\n\n[!] Saliendo...\n")
    sys.exit(1)


# Ctrl+C
signal.signal(signal.SIGINT, def_handler)


def menu(w):
    print("¿Que datos desea importar?\nPulse:")
    datos = int(input("\t[1] Imagenes         [3] Hojas de estilo\n "
                      "\t[2] Enlaces          [4] Scripts\n"
                      "-> "))
    if datos == 1:
        imagen = w.imagenes()
        for img in imagen:
            print(img)
        return True
    if datos == 2:
        links = w.enlaces()
        for link in links:
            print(link)
        return True
    if datos == 3:
        hojas = w.hojas_estilo()
        for hoja in hojas:
            print(hoja)
        return True
    if datos == 4:
        scripts = w.scripts()
        for script in scripts:
            print(script)
        return True
    else:
        print("Opción no válida")
        return False


def documento_html(direccion_web):
    pagina_html = requests.get(direccion_web)
    return pagina_html.text


def banner():
    font = """
    _____ _ _ _ _    
    | ___| _ __   (_) | |__   / | |   |_ 
    | |_ | '__|   | | | '_ \    | |   | __| 
    |   _| | |    | | | |_) |   | |   | |_ 
    |_|  |_|  |   |_| |_.__/    |_|    \__|
    """
    return print(font)


if __name__ == "__main__":
    DEFAULT_URL = "https://github.com/Frib1t"
    print("Bienvenido al programa de web scraping\n")
    time.sleep(0.5)
    banner()
    print("{}Created by Frib1t\n".format("\t"*8))

    while True:
        extensiones = [".com", ".es", ".net", ".org"]
        web = str(input(f"\n [+] Introduzca la url de la cual quiere exportar los datos "
                        f"(dejar en blanco para usar {DEFAULT_URL}): "))
        if not web:  # Si el usuario presiona Enter sin ingresar nada
            web = DEFAULT_URL
        if any(ext in web for ext in extensiones):
            if not web.startswith("https://"):
                web = "https://" + web

            w = WebScraping(web)
            if menu(w):
                break
        else:
            print("\n[!] Introduzca una extensión válida\n")
