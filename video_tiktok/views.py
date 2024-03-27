# la funcion render es utilizada en Django ara renderizar plantillas HTML y
# pasar contexto (variables) a esas plantillas.
import glob
import json
import uuid
from django.shortcuts import render, redirect
# Autenticacion
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, logout, authenticate

# from usuario.models import CreditosUsuario
from usuario.models import UsuarioPersonalizado

import pdb
# Librerias para whisper
import shutil
import warnings
import whisper  # pip install -U openai-whisper

# Librerias para los subtitulos
import pysrt  # pip install pysrt
from django.utils.text import get_valid_filename
from pysrt import SubRipTime

# Convierte srt a ass: aplica estilos al archivo ass
import pysubs2  # pip install pysubs2
import datetime

# Correccion subtitulos
import srt  # pip install srt

# Librerias - Api chatgpt
from django.templatetags.static import static
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from sympy import true

from ProyectoTikTok.config import OPENAI_API_KEY

import openai
from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)

# Efecto zoom in/out, redimensionamiento proporcional
from PIL import Image  # pip install Pillow
import cv2  # pip install opencv-python-headless
from django.conf import settings
import subprocess

# Libreria de expresion regular
import re

# Libreria para bajar volumen
from pydub import AudioSegment  # pip install pydub

# Librerias para descargar imagenes
import requests  # pip install requests
import os
import base64

# Libreria para combinar audio y musica
import moviepy.editor as mpe  # pip install moviepy

# Librerias para generacion de video
from moviepy.video import fx as vfx
from moviepy.video.compositing import transitions
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip  # combinar audio y musica
from moviepy.editor import transfx, concatenate_videoclips
from moviepy.video.fx import rotate
import random
from moviepy.audio.io.AudioFileClip import AudioFileClip

# Libreria para audio
import time

# Libreria para inserta musica a video
import moviepy.editor as mymovie

# Librerias para audio-video
import numpy as np  # pip install numpy moviepy, np es una biblioteca para la computación numérica en Python
from moviepy.audio.AudioClip import AudioArrayClip  # crear un clip de audio a partir de una matriz
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips

# Libreria de voces EleveLabs
from elevenlabs import generate, play

# Funcion de vista
'''
def index(request):
    if request.user.is_authenticated:
        return render(request, 'video_tiktok/index.html')
    else:
        # Redirigir al usuario a la página de inicio de sesión si no está autenticado
        #return redirect('usuario/login.html')
        return redirect('loguear')
'''


@login_required
def index(request):
    return render(request, 'video_tiktok/index.html')


# API CHATGPT
@login_required
def generate_script(request):
    # Clave API

    generated_script = ""
    if request.method == "POST":
        title = request.POST.get('videoTitle')
        script = request.POST.get('videoScript')

        # f'Basado en el siguiente guión, ¿lo categorizarías como "relajante" o "divertida"? ' \

        tema = f'Genera SOLO un guión destinado a una narración de voz en off para un video sobre el tema: {script}. ' \
               f'Este guión debe tener una duración de aproximadamente 90 segundos cuando se lee en voz alta.' \
               f'El tono del guión debe ser creativo, llamativo y fluido, un flujo continuo y sin interrupciones.' \
               f'El enfoque debe estar únicamente en el contenido narrativo.' \
               f'Evita agregar al guión "elementos de escena" o "notas de dirección" así como "indicaciones de locutor en off", "marcas de tiempo, "' \
               f'o similares, detalles sobre la visualización del video, como música, transiciones o imágenes al inicio del guion.'

        tema2 = f'Genera un guión para un video corto de 60 segundos sobre: {script} donde solo hay una voz en off, ' \
                f'no hay personajes en este guion, céntrate en que el guión sea solo el texto del libreto, ' \
                f'no incluyas descripciones de escenas, efectos de transiciones, musica, intro, resumen, ' \
                f'imagenes y cualquier referencia a notas de dirección o indicaciones de donde comienza la voz en off.' \
                f'El guion debe ser creativo, llamativo para el usuario y fluido, con flujo continuo y sin interrupciones.' \
                f'El texto generado no debe llevar instrucciones adicionales que no sea el guión en sí.' \

        guion = (f'Genera un guión de voz en off para un video de redes sociales que dure 90 segundos. El tema es: {script}. '
                 f'El guión debe comenzar con: 1) Una introducción atrapante:  la redacción debe ser entre 12 y 20 palabras. '
                 f'Debes ser muy bueno sintetizando. Utiliza una pregunta retórica o una afirmación sorprendente sobre '
                 f'el tema para captar la atención del público inmediatamente. '
                 f'Estas son algunas de las maneras en que podrías comenzar:'
                 f'"Top 5 Consejos para...'
                 f'¿Sabías Qué...?'
                 f'Las 3 Cosas que...'
                 f'Lo Que Nadie Sabe de...'
                 f'Top 5 Lugares de...'
                 f'¿Qué Pasa Cuando...?'
                 f'Las 3 Historias Impactantes de...'
                 f'Descubre [Número] Datos Asombrosos sobre...'
                 f'Top 5 Hábitos Diarios para...'
                 f'¿Cuál es el Secreto de...?'
                 f'Las 3 Mejores Apps para...'
                 f'Lo Que Debes Saber Antes de...'
                 f'Top 5 Trucos para Mejorar...'
                 f'¿Sabías Que Puedes...?'
                 f'Las 3 Maneras Más Rápidas de...'
                 f'Lo Que Nadie Te Dice Sobre...'
                 f'Top 5 Ideas Creativas para...'
                 f'¿Sabías Que Existe...?'
                 f'Las 3 Tendencias Actuales en...'
                 f'Descubre [Número] Recetas Fáciles de...'
                 f'¿Cómo Hacer... en [Número] Pasos?'
                 f'Las 3 Reglas de Oro para...'
                 f'Lo Que Nadie Te Cuenta Sobre...'
                 f'Top 5 Ejercicios para...'
                 f'¿Sabías Que Hay...?'
                 f'Las 3 Maneras de Aprender...'
                 f'Descubre [Número] Beneficios de...'
                 f'¿Cuál es el Mejor Momento para...?'
                 f'Lo Que Nadie Te Dice Sobre el Mundo de...'
                 f'Top 5 Consejos de Expertos en...'
                 f'¿Sabías Que Puedes Lograr...?'
                 f'Las 3 Cosas Más Extrañas de...'
                 f'Descubre [Número] Lugares Secretos de...'
                 f'¿Cómo Resolver... en [Número] Pasos?'
                 f'Top 5 Curiosidades de...'
                 f'Las 3 Formas de Cambiar...'
                 f'¿Qué Hacer Cuando...?'
                 f'Lo Que Nadie Sabe Sobre el Arte de...'
                 f'Descubre [Número] Tips para...'
                 f'¿Sabías Que Existen...?'
                 f'Las 3 Historias Asombrosas de...'
                 f'Top 5 Formas de Ahorrar...'
                 f'¿Cuál es el Secreto para...?'
                 f'Lo Que Nadie Te Cuenta Sobre la Vida de...'
                 f'Descubre [Número] Datos Interesantes sobre...'
                 f'¿Sabías Que Puedes Aprender...?'
                 f'Las 3 Estrategias para Superar...'
                 f'Top 5 Ideas Innovadoras en...'
                 f'¿Qué Sucede Cuando...?'
                 f'Lo Que Nadie Te Dice Sobre el Éxito en..."'
                 f'-----'
                 f'Después, 2) el guión debe seguir con una oración CORTA, de no más de 12 palabras, y MUY ingeniosa, '
                 f'que vincule la introducción con la importancia que tiene para la audiencia el terminar de ver el video. '
                 f'Esto debe lograrse de una manera subliminal, y eficiente.'
                 f'La tercera parte es 3) El desarrollo. El desarrollo debe ser educativo e interactivo, debe explicar '
                 f'el tema central de manera sucinta, clara y sin rodeos. Navega en toda la red de internet para '
                 f'descubrir los datos menos conocidos relacionados con el tema. Una vez que se aproxima un tema, '
                 f'se da por concluido y no se aborda más. Encuentra el tema central y explícalo de la manera más '
                 f'impresionante posible sin llegar a la rídicula exageración. Esta parte no debe ser mayor a 33 palabras.'
                 f'El guion debe ser creativo, interesante, claro y profesional, adaptando información de fuentes de '
                 f'internet sobre el tema para ser entretenido y accesible, manteniendo un enfoque educativo.'
                 f'Entrega el texto únicamente dividido por párrafos y no en secciones como "inicio, desarrollo y cierre".'
                 f'El cierre es una llamada a la acción, por lo que debes darme una sugerencia de la palabra a considerar '
                 f'para activar la automatización y dame sugerencias de lo que debo responder a los usuarios que '
                 f'comenten la palabra clave.'
                 f'Usa un lenguaje casual para causar más cercanía a la audiencia, usa slangs regiomontanos con grado '
                 f'de moderación del 30% para que el guión no suene muy exagerado con los modismos y trata de incluir '
                 f'información más detallada.'
                 f'Básate en el siguiente guión, sigue la misma estructura, congruencia, síntesis, estilo y extensión:'
                 f'1. Introducción: “¿Caíste en un bache? Ponte buzo. El municipio debe pagarte los daños.”'
                 f'2. Oración que reafirme la introducción y explique por qué es relevante para la audiencia: “Mucha gente '
                 f'asume que cobrar la reparación de su suspensión, de sus llantas o rines es un martirio y tienen algo '
                 f'de razón, pero eso no significa que no puedes cobrarle al municipio.”'
                 f'3. Desarrollo de un mensaje relacionado con la audiencia que sea de utilidad: '
                 f'“Lo primero que debes hacer es:'
                 f'Tomar video del bache que causó'
                 f'los daños, también toma fotos de lo que provocó a tu vehículo.'
                 f'Después, asegúrate de guardar todos los recibos de pagos que hagas por los daños.'
                 f'Finalmente, debes solicitar al municipio el reembolso de dichos gastos por escrito acompañado'
                 f' de una copia de tu identificación y copia de los recibos de tus gastos.”'
                 f'4. Final y llamada a la acción: Comenta “Bache” en este video y recibe gratis más información así '
                 f'como un machote para que puedas usarlo para tu solicitud.'
                 f'Sígueme para más consejos.'
                 f'Genera contenido de calidad, sin tanto rodeo, no trates de endulzar el oído del escuchante con '
                 f'expresiones fantasiosas, quiero un guión concreto, objetivo e interesante.')

        print("Longitud del tema:", len(guion))

        # Obtener el usuario actual
        # usuario = request.user
        usuario = get_object_or_404(UsuarioPersonalizado, id=request.user.id)

        # Verificar si el usuario tiene créditos suficientes
        creditos_usuario = UsuarioPersonalizado.objects.get(id=usuario.id).creditos
        # Comprobar si el usuario tiene créditos suficientes
        if creditos_usuario > 0:

            max_retries = 3  # Número máximo de intentos
            retry_count = 0

            while retry_count < max_retries:
                def remove_patrones(text):
                    # Patrones que deseas eliminar (por ejemplo, texto entre paréntesis o corchetes)
                    patterns_to_remove = [r'\([^)]*\)', r'\[[^\]]*\]', 'Voz en off:', 'VOZ EN OFF:', 'Voz en Off:',
                                          'Comienza la voz en off:', 'Inicia la voz en off:', 'Entra la voz en off:',
                                          'Comienza el guión:', 'Empieza el reloj:', 'Fin.']

                    # Aplicar cada patrón para eliminarlo del texto
                    for pattern in patterns_to_remove:
                        text = re.sub(pattern, '', text)

                    return text.strip()

                try:
                    inicio = time.time()  # Guarda el tiempo actual

                    stream = client.chat.completions.create(
                        model="gpt-4",
                        messages=[{"role": "user", "content": guion}],
                        stream=True,  # No recibir los resultados de la API de forma continua
                        # max_tokens=500,
                    )

                    response = ""  # Inicializar la variable para almacenar la respuesta

                    for chunk in stream:
                        if chunk.choices[0].delta.content is not None:
                            # print(chunk.choices[0].delta.content, end="")
                            response += chunk.choices[0].delta.content  # Concatenar en lugar de sobrescribir

                    # Imprimir la respuesta completa al final
                    print(f"Usuario {usuario.username}: {response}")
                    # Agregar una línea de separación para distinguir las respuestas de diferentes usuarios
                    print("\n--- Fin de respuesta ---\n")
                    generated_response = remove_patrones(response)
                    print("Longitud del guion generado:", len(generated_response))

                    fin = time.time()  # Guarda el tiempo actual
                    tiempo = fin - inicio  # Calcula la diferencia
                    print(f"El tiempo de respuesta del guion fue de {tiempo} segundos.")
                    return JsonResponse({'generated_script': generated_response})

                except requests.exceptions.ConnectionError:
                    retry_count += 1
                    print(f"Error de conexión. Reintentando {retry_count}/{max_retries}...")

                except Exception as e:
                    print(f"Error: {e}")
                    return JsonResponse({'error': 'Error al generar el guión'}, status=500)

            return JsonResponse({'error': 'Se agotaron los intentos de conexión'}, status=500)

        else:
            return JsonResponse({
                'error': 'No tienes créditos suficientes para generar el guión que solicitaste. '
                         'Para obtener créditos, puedes cargar créditos o contactar con '
                         'nuestro soporte técnico si crees que ha habido un error.'},
                status=403)

    return JsonResponse({'error': 'Método no permitido'}, status=405)
