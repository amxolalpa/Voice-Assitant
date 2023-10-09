import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia

# Opciones de tipo de voz
id1 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES - MX_SABINA_11.0'
id2 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'

# Escuchar nuestro microfono y devolver el audio como texto
def transformar_audio_en_texto():

    # ALmacenar recognizer en variable
    r = sr.Recognizer()

    # Configurar el microfono
    with sr.Microphone() as origen:

        # Tiempo de espera
        r.pause_threshold = 0.8

        # Informar que empezó la grabación
        print("Ya puedes hablar")

        # Guardar lo que escuche como audio
        audio = r.listen(origen)

        try:
            # Buscar en google
            pedido = r.recognize_google(audio, language= "es-mx")

            # Prueba de que pudo ingresar
            print( 'Dijiste: ' + pedido)

            #Devolver pedido
            return pedido

        # en caso de que no comprenda el audio
        except sr.UnknownValueError:

            # Prueba de que no comprendio el audio
            print('ups, no entendi')

            # Devolver error
            return "Sigo esperando"

        # En caso de no resolver el pedido
        except sr.RequestError:

            # Prueba de que no comprendio el audio
            print('ups, no hay servicio')

            # Devolver error
            return "Sigo esperando"

        # En caso de error inesperado
        except:

            # Prueba de que no comprendio el audio
            print('ups, algo ha salido mal')

            # Devolver error
            return "Sigo esperando"

# El Asistente pueda ser escuchado
def hablar (mensaje):
    # Encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice',id1)
   #Pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()

# Informar el dia de la semana
def pedir_dia():
    #Crear variable  con datos de hoy
    dia=datetime.date.today()
    print(dia)
    #crear variables para el dia de la semana
    dia_semana = dia.weekday()
    print(dia_semana)
    # Diccionario con los nombre de los dias
    calendario = {0: "Lunes", 1: "Martes", 2: "Miércoles", 3: "Jueves", 4: "Viernes", 5: "Sábado", 6: "Domingo"}
    # Decir el dia de la semana
    hablar(f"Hoy es {calendario[dia_semana]}")

# Informar la hora que es
def pedir_hora():
    hora = datetime.datetime.now()
    hora = f'En este momento son las {hora.hour} horas con {hora.minute} minutos'
    print (hora)
    hablar(hora)

# Saludo Inicial
def saludo_inicial():
    # Crear variable con datos de hora
    hora=datetime.datetime.now()
    if hora.hour <6 or hora.hour >20:
        momento='Buenas Noches'
    elif 6 <= hora.hour < 12:
        momento='Buenos días'
    else:
        momento='Buenas tardes'


    #Decir el saludo
    hablar(f"Hola {momento}, soy Ily, tú asistente personal. Por favor dime en que te puedo ayudar")

def pedir_cosas():
    #activar saludo inicial
    saludo_inicial()
    #variable de corte
    comenzar = True
    #loop central
    while comenzar:
        # Activar el micro y guardar el pedido en un string
        pedido = transformar_audio_en_texto().lower()
        # Tienen que ser minusculas -----
        if 'abrir youtube' in pedido:
            hablar('Claro, dame un momento')
            webbrowser.open('https://www.youtube.com')
            continue
        elif 'abrir el navegador' in pedido:
            hablar('OK, voy a abrir google')
            webbrowser.open('https://www.google.com')
            continue
        elif 'qué día es hoy' in pedido:
            pedir_dia()
            continue
        elif 'qué hora es' in pedido:
            pedir_hora()
            continue
        elif 'buscar en wikipedia' in pedido:
            hablar('Entro a buscar a wikipedia')
            pedido = pedido.replace('buscar en wikipedia','')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido,sentences=1)
            hablar ('wikipedia dice lo siguiente:')
            hablar(resultado)
            continue
        elif 'busca en internet' in pedido:
            hablar('ok, voy a buscar en internet, recuerda que hay muchas cosas')
            pedido = pedido.replace('busca en internet','')
            pywhatkit.search(pedido)
            hablar('esto es lo que he encontrado:')
            continue
        elif 'reproducir' in pedido:
            hablar('buena idea, comienzo a reproducirlo')
            pywhatkit.playonyt(pedido)
            continue
        elif 'chiste' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {'apple': 'APPL',
                       'amazon': 'AMZN',
                       'google':'GOOGL'}
            try:
                accion_buscada = cartera[accion]
                accion_buscada =yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'La encontré!, el precio es {accion} es {precio_actual}')
                continue
            except:
                hablar('perdón, pero no la he encontrado')
                continue
        elif 've a descansar' in pedido:
            hablar('me voy a descansar, recuerda cualquier cosa me avisas')
            break

pedir_cosas()




