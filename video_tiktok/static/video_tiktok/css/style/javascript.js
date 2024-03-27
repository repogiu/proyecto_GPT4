<!-- Script para generar guion -->
<script>

  function generateScript() {
    //Obtener los valores de los campos de entrada
    const title = $('#videoTitle').val();
    const script = $('#videoScript').val();

    // Obtener el elemento overlay por su id
    var overlay = document.getElementById("overlay");
    // Cambiar el estilo de display a block para mostrarlo
    overlay.style.display = "block";

    //Enviar una solicitud POST
    $.ajax({
      type: 'POST',
      url: '{% url "generate_script" %}',
      data: {
        videoTitle: title,
        videoScript: script,
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
      },
      dataType: 'json',
      success: function (response) {

        // Ocultar el overlay
        overlay.style.display = "none";

        // Manejar la respuesta
        $('#generatedScript').val(response.generated_script);
        // Actualizar la visualización de créditos en el HTML
        //console.log('Créditos actualizados:', response.creditos_actualizados);
        //$('.creditos-container a').html(
        //`<span style="font-weight: bold; font-size: 19px; margin-right: 10px;"> <strong>${response.creditos_actualizados}</strong></span><span class="coin"><i class="fas fa-coins"></i></span><button class="btn btn-primary" style="border-radius: 20px; text-align: center;">Créditos</button>`);
        $('#generatedScriptCheckButton').html('<i class="fas fa-check-square fa-2x text-success"></i>');

      },
      error: function (error) {

        // Ocultar el overlay también en caso de error
        overlay.style.display = "none";

        // Mostrar el modal con el mensaje de error
        $('#exampleModal').modal('show');

        // Usar el argumento responseJSON para acceder al error que devuelves en el return
        $("#modalBody").html(error.responseJSON.error);

        // Log del error
        console.log(error);
      }
    });
  }
</script>


<!-- Script para generar imagenes -->
<script>
    function generateImages() {
        // Obtener el valor del guion generado, que el usuario puede haber editado
        const editedScript = $('#generatedScript').val();
        const title = $('#videoTitle').val();

        // Obtener el elemento overlay por su id
        var overlay = document.getElementById("overlay-imagenes");

        // Cambiar el estilo de display a block para mostrarlo
        overlay.style.display = "block";

        // Enviar una solicitud POST a tu endpoint de Django para generar las imágenes
        $.ajax({
            type: 'POST',
            url: '{% url "generate_prompt" %}',
            data: {
                videoTitle: title,
                editedScript: editedScript,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            dataType: 'json',
            beforeSend: function() {
              // Ocultar la alerta de éxito
              $('#successAlertImg').hide();
            },
            success: function (response) {
                // Ocultar el overlay
                 overlay.style.display = "none";

                $('#generatedPrompt').val(response.generated_prompt);
                console.log(response);

                // Mostrar la alerta de éxito después de generar el video
                $('#successAlertImg').show();

                // Verificar si la respuesta contiene las rutas de las imágenes
                if (response.imagePaths && response.imagePaths.length > 0) {
                    const totalImages = response.imagePaths.length;
                    updateProgress(totalImages);
                } else {
                    console.log('No se generaron imágenes');
                }
            },
            error: function (error) {
                // Ocultar el overlay también en caso de error
                overlay.style.display = "none";
                $('#exampleModal2').modal('show');
                // Usar el argumento responseJSON para acceder al error que devuelves en el return
                $("#modalBody2").html(error.responseJSON.error);
                //$('#modalBody2').text('Error al generar las imágenes. Inténtalo de nuevo más tarde.');

                //alert("Error al generar las imagenes.");
                console.log(error);
            }
        }).done(function() {
                // Mostrar el tilde verde con el mensaje de éxito después de que se haya completado la solicitud
                //$('#generatedPrompt').after('<span class="text-white ml-2"><i class="fas fa-check-circle fa-2x text-success" ></i> Imagenes generadas </span>');
                $('#generatedImageCheckButton').html('<i class="fas fa-check-square fa-2x text-success"></i>');

        });

    }
</script>

<script>
    function updateProgress(totalImages) {
    const progressText = document.getElementById("spinner-text-imagenes");
    let imagesGenerated = 0;

    const intervalId = setInterval(() => {
        progressText.innerText = `[${imagesGenerated}/${totalImages}] Generando imágenes...`;
        imagesGenerated++;

        if (imagesGenerated === totalImages) {
            clearInterval(intervalId);
            progressText.innerText = "Imágenes generadas con éxito!";
        }
    }, 1000); // Actualizar cada segundo (ajusta según sea necesario)
}
</script>

<!-- Script para generar video -->
<script type="text/javascript">
$(document).ready(function() {
    $("#generateVideoBtn").click(function() {
        const editedScript = $('#generatedScript').val();
        const selectedVoice = $('#voiceSelection').val();
        const selectedMusic = $("#musicSelection").val();

        // Obtener el elemento overlay por su id
        var overlay = document.getElementById("overlay-video");
        // Cambiar el estilo de display a block para mostrarlo
        overlay.style.display = "block";

        // Define los mensajes del spinner
        const mensajesSpinner = {
            generandoVoz: 'Generando voz y <br> subtítulos... [1/3]',
            generandoVideo: ' Generando video con <br> efectos y música... [2/3]',
            insertandoSubtitulos: 'Insertando subtítulos <br> al video... [3/3]'
        };

        // Primero, generamos el audio
        $.ajax({
            type: "POST",
            url: "/texto_a_voz/",
            data: {
                'texto': editedScript,
                'voice': selectedVoice,
                csrfmiddlewaretoken: "{{ csrf_token }}"
            },
            beforeSend: function() {
              // Actualiza el texto del spinner a 'Generando video con transiciones, efectos, música y voz'
              $('#spinner-text-video').html(mensajesSpinner.generandoVoz);
            },
            success: function(audioResponse) {
               if (audioResponse.status === 'success') {
                    // Una vez que el audio se ha generado, iniciamos la generación del video
                    $.ajax({
                        type: "POST",
                        url: "/generate_video/",
                        data: {
                            'music': selectedMusic,
                            'audioPath': audioResponse.audioPath,
                            csrfmiddlewaretoken: "{{ csrf_token }}"
                        },
                        beforeSend: function() {
                          // Actualiza el texto del spinner a 'Generando video con transiciones, efectos, música y voz'
                          $('#spinner-text-video').html(mensajesSpinner.generandoVideo);
                        },
                        success: function(response) {
                            console.log(response); // Imprime la respuesta para depurar

                            // Ocultar el overlay
                            overlay.style.display = "none";

                            // Manejar la respuesta de la generación del video

                            if (response.videoPath) {
                                //alert("Video generado con éxito!");
                                // Actualiza la fuente del reproductor de video si es necesario
                                if (response.videoPath) {
                                    //const videoPlayer = $('video')[0]; // Asumiendo que hay un único elemento <video>
                                    //videoPlayer.src = response.videoPath;
                                    //videoPlayer.load();
                                    subtitulos();

                                    // Mensaje de exito
                                    //$('#generateVideoBtn').after('<span class="text-white ml-2"><i class="fas fa-check-circle fa-1x text-success" ></i>Video generado!</span>');
                                    //$('#videoPlayer').after('<span class="text-white ml-2"><i class="fas fa-check-circle fa-2x text-success" style="vertical-align: middle;"></i>Video generado!</span>');


                                }
                            } else if (response.error){
                                // Muestra el modal con un mensaje específico de error
                                $('#exampleModal3').modal('show');
                                //$('#modalBody3').text('Error al generar el video: '+ response.error);
                                $("#modalBody3").html('Error al generar el video');


                            } else {
                                //alert('Respuesta inesperada del servidor');
                                // Respuesta inesperada del servidor
                                $('#exampleModal3').modal('show');
                                $("#modalBody3").html('Respuesta inesperada del servidor);

                            }
                        },
                        error: function(error) {

                            // Ocultar el overlay también en caso de error
                            overlay.style.display = "none";
                            // Error de solicitud Ajax en sí mismo
                            $('#exampleModal3').modal('show');
                            $("#modalBody3").html('Error al generar el video');

                            //alert("Error al generar el video.");
                        }
                    });
                } else {
                    // Ocultar el overlay también en caso de error
                    overlay.style.display = "none";
                    // Muestra el modal de error
                    $('#exampleModal3').modal('show');
                    $("#modalBody3").html('Error al generar el audio');


                    //alert('Error al generar el audio.');
                }
            },
            error: function(error) {
                // Ocultar el overlay también en caso de error
                overlay.style.display = "none";
                //alert('Error al generar el audio.');
                // Error de solicitud Ajax en sí mismo
                $('#exampleModal3').modal('show');
                // Verificar el tipo de error y proporcionar un mensaje descriptivo
                if (error.status === 400) {
                    //$('#modalBody3').text('Hubo un problema con la solicitud. Por favor, verifica los datos proporcionados e inténtalo nuevamente.');
                    $("#modalBody3").html('Hubo un problema con la solicitud. Por favor, verifica los datos proporcionados.');
                } else if (error.status === 500) {
                    //$('#modalBody3').text('Lo sentimos, ha ocurrido un error interno en el servidor. Por favor, inténtalo más tarde.');
                    $("#modalBody3").html('Lo sentimos, ha ocurrido un error interno en el servidor. Por favor, inténtalo más tarde.');
                } else {
                    //$('#modalBody3').text('Lo sentimos, ha ocurrido un error inesperado. Por favor, inténtalo más tarde.');
                    $("#modalBody3").html('Lo sentimos, ha ocurrido un error inesperado.');
                }
            }
        });
    });
});


</script>


<!-- Script para generar subtitulos con consumo de creditos -->

<script>
    function subtitulos() {
    // Obtener el elemento overlay por su id
    var overlay = document.getElementById("overlay-video");
    // Cambiar el estilo de display a block para mostrarlo
    overlay.style.display = "block";
    // Define los mensajes del spinner
    const mensajesSpinner = {
        insertandoSubtitulos: 'Insertando subtítulos <br> al video... [3/3]'
    };

    // Realiza una llamada AJAX para procesar los pasos adicionales
    $.ajax({
        type: "POST",
        url: "/procesar_subtitulos/",
        data: {
            csrfmiddlewaretoken: "{{ csrf_token }}"
        },
        beforeSend: function() {
            // Ocultar la alerta de éxito
            $('#successAlert').hide();
            // Actualiza el texto del spinner a 'Generando video con transiciones, efectos, música y voz'
            $('#spinner-text-video').html(mensajesSpinner.insertandoSubtitulos);
        },
        success: function(response) {
            // Obtener el elemento del reproductor de video
            const videoPlayer = document.getElementById('videoPlayer');

            // Configurar la fuente del video con la ruta proporcionada por el servidor
            videoPlayer.src = response.outputPath;

            // Agregar un evento para ocultar el overlay cuando el video esté cargado
            videoPlayer.addEventListener('loadeddata', function() {
                // Ocultar los spinners después de mostrar la alerta de éxito
                $('#overlay-video').hide();

                // Mostrar la alerta de éxito después de generar el video
                $('#successAlert').show();
                $('#generatedVideoCheckButton').html('<i class="fas fa-check-square fa-2x text-success"></i>');
            });

            // Llamar a la función descontar_creditos() después de completar subtitulos
            $.ajax({
                type: "POST",
                url: "/descontar_creditos/",
                data: {
                    csrfmiddlewaretoken: "{{ csrf_token }}"
                },
                success: function(response) {
                    console.log("Créditos descontados exitosamente");
                    // Actualizar la visualización de créditos en el HTML
                    console.log('Créditos actualizados:', response.creditos_actualizados);
                    $('.creditos-container a').html(
                    `<span style="font-weight: bold; font-size: 19px; margin-right: 10px;"> <strong>${response.creditos_actualizados}</strong></span><span class="coin"><i class="fas fa-coins"></i></span><button class="btn btn-primary" style="border-radius: 20px; text-align: center;">Créditos</button>`);
                },
                error: function(error) {
                    console.error("Error al descontar créditos:", error);
                }
            });
        },
        error: function(error) {
            // Ocultar el overlay también en caso de error
            overlay.style.display = "none";
            // Ocultar los spinners después de mostrar la alerta de éxito
            $('#overlay-video').hide();
            //alert('Error al procesar los subtitulos.');
            //$('#modalBody3').text('Lo sentimos, ha ocurrido un error al insertar los subtítulos al video. Por favor, inténtalo más tarde.');
            $("#modalBody3").html('Lo sentimos, ha ocurrido un error al insertar los subtítulos al video. Por favor, inténtalo más tarde.');
        }
    });
}



</script>

<!-- Script para generar Reintentar nuevo video -->
<script>
    function generateNewVideo() {
    const selectedMusic = $("#musicSelection").val();

    // Obtener el elemento overlay por su id
    var overlay = document.getElementById("overlay-video");
    // Cambiar el estilo de display a block para mostrarlo
    overlay.style.display = "block";

    // Define los mensajes del spinner
    const mensajesSpinner = {
        generandoVideo: ' Generando video con <br> efectos y música... [2/3]',
        insertandoSubtitulos: 'Insertando subtítulos <br> al video... [3/3]'
    };

    // Iniciamos la generación del video directamente
    $.ajax({
        type: "POST",
        url: "/generate_video/",
        data: {
            'music': selectedMusic,
            csrfmiddlewaretoken: "{{ csrf_token }}"
        },
        beforeSend: function() {
            // Actualiza el texto del spinner a 'Generando video con transiciones, efectos, música y voz'
            $('#spinner-text-video').html(mensajesSpinner.generandoVideo);
        },
        success: function(response) {
            console.log(response); // Imprime la respuesta para depurar

            // Ocultar el overlay
            overlay.style.display = "none";

            // Manejar la respuesta de la generación del video

            if (response.videoPath) {
                //const videoPlayer = $('video')[0]; // Asumiendo que hay un único elemento <video>
                //videoPlayer.src = response.videoPath;
                //videoPlayer.load();
                subtitulos2();


            } else if (response.error) {
                // Muestra el modal con un mensaje específico de error
                $('#exampleModal3').modal('show');
                //$('#modalBody3').text('Error al generar el video: '+ response.error);
                $("#modalBody3").html('Error al generar el video');

            } else {
                //alert('Respuesta inesperada del servidor');
                // Respuesta inesperada del servidor
                $('#exampleModal3').modal('show');
                //$('#modalBody3').text('Respuesta inesperada del servidor');
                $("#modalBody3").html('Respuesta inesperada del servidor');

            }
        },
        error: function(error) {

            // Ocultar el overlay también en caso de error
            overlay.style.display = "none";
            // Error de solicitud Ajax en sí mismo
            $('#exampleModal3').modal('show');
            //$('#modalBody3').text('Error al generar el video: ' + error.statusText);
            $("#modalBody3").html('Error al generar el video');

            //alert("Error al generar el video.");
        }
    });
}

</script>

<!-- Script para generar subtitulos SIN consumo de creditos -->
<script>
    function subtitulos2() {
    // Obtener el elemento overlay por su id
    var overlay = document.getElementById("overlay-video");
    // Cambiar el estilo de display a block para mostrarlo
    overlay.style.display = "block";
    // Define los mensajes del spinner
    const mensajesSpinner = {
        insertandoSubtitulos: 'Insertando subtítulos <br> al video... [3/3]'
    };

    // Realiza una llamada AJAX para procesar los pasos adicionales
    $.ajax({
        type: "POST",
        url: "/procesar_subtitulos/",
        data: {
            csrfmiddlewaretoken: "{{ csrf_token }}"
        },
        beforeSend: function() {
          // Ocultar la alerta de éxito
          $('#successAlert').hide();
          // Actualiza el texto del spinner a 'Generando video con transiciones, efectos, música y voz'
          $('#spinner-text-video').html(mensajesSpinner.insertandoSubtitulos);
        },
        success: function(response) {
            $('#generateVideoBtn').val(response.outputPath);
            console.log("Subtitulos generados")
            // Ocultar los spinners después de mostrar la alerta de éxito
            $('#overlay-video').hide();

            // Mostrar la alerta de éxito después de generar el video
            $('#successAlert').show();
            $('#generatedVideoCheckButton').html('<i class="fas fa-check-square fa-2x text-success"></i>');

        },
        error: function(error) {
            // Ocultar el overlay también en caso de error
            overlay.style.display = "none";
            // Ocultar los spinners después de mostrar la alerta de éxito
            $('#overlay-video').hide();
            $("#modalBody3").html('Lo sentimos, ha ocurrido un error al insertar los subtítulos al video. Por favor, inténtalo más tarde.');
        }
    });
}

</script>


</script>

<!-- Script para cargar y reproducir el video automáticamente -->
<script>
    $(document).ready(function() {
        // Obtener el elemento del reproductor de video
        const videoPlayer = document.getElementById('videoPlayer');

        // Generar un parámetro único para evitar la caché
        const cacheBuster = new Date().getTime();

        // Configurar la fuente del video con el parámetro único
        const videoSource = `{% static 'video_tiktok/videos/video_subtitulos/video_con_subtitulo.mp4' %}?v=${cacheBuster}`;

        // Verificar si el video existe
        $.ajax({
            url: videoSource,
            type: 'HEAD',
            success: function() {
                // Configurar la fuente del video si existe
                videoPlayer.src = videoSource;

            },
            error: function() {
                // Mostrar un mensaje de error si el video no está disponible
                console.error("Error al cargar el video.");
            }
        });
    });
</script>


<!-- Script para almacenar y recuperar datos -->
<script>
    // Almacenar datos durante la sesión
    $('#videoTitle, #videoScript, #generatedScript, #voiceSelection, #musicSelection').on('input', function() {
        localStorage.setItem(this.id, this.value);
    });

    // Recuperar datos al cargar la página
    $(document).ready(function() {
        $('#videoTitle').val(localStorage.getItem('videoTitle'));
        $('#videoScript').val(localStorage.getItem('videoScript'));
        $('#generatedScript').val(localStorage.getItem('generatedScript'));
        $('#voiceSelection').val(localStorage.getItem('voiceSelection'));
        $('#musicSelection').val(localStorage.getItem('musicSelection'));
    });

    // Limpiar campos y localStorage al descargar el video
    $('.btn-download-video').click(function() {
        // Restablecer valores de los campos
        $('#videoTitle, #videoScript, #generatedScript, #voiceSelection, #musicSelection').val('');

        // Borrar datos almacenados en localStorage
        localStorage.clear();
    });
</script>

<script>
  // Define una variable global para el audio actualmente en reproducción
  var currentAudio = null;

  function playAudio(audioUrl) {
    // Si hay un audio en reproducción y es diferente al actual, deten la reproducción
    if (currentAudio && currentAudio.src !== audioUrl) {
      currentAudio.pause();
    }

    // Si el audio está en pausa o es diferente, comienza la reproducción
    if (!currentAudio || currentAudio.src !== audioUrl) {
      currentAudio = new Audio(audioUrl);
      currentAudio.play();

    } else {
      // Si el mismo audio está en reproducción, pausa o detiene la reproducción
      if (!currentAudio.paused) {
        currentAudio.pause();
      } else {
        currentAudio.play();
      }
    }
  }

</script>

<script>
    // Define una función que cambie el valor del menú desplegable y marque la tarjeta de la voz
function selectVoice(voiceValue) {

  // Obtiene el elemento del menú desplegable por su id
  var voiceSelection = document.getElementById("voiceSelection");

  // Cambia el valor del menú desplegable al valor de la voz seleccionada
  voiceSelection.value = voiceValue;

  // Obtiene todas las tarjetas de voz por su clase
  var voiceCards = document.getElementsByClassName("voice-card");

  // Recorre todas las tarjetas de voz
  for (var i = 0; i < voiceCards.length; i++) {
    // Obtiene la etiqueta de la tarjeta de voz actual
    var voiceLabel = voiceCards[i].querySelector("label");
    // Comprueba si el valor de la etiqueta coincide con el valor de la voz seleccionada
    if (voiceLabel.getAttribute("data-value") == voiceValue) {
      // Cambia el borde de la tarjeta de voz a azul brillante
      voiceCards[i].style.border = "1px solid blue";
    } else {
      // Cambia el borde de la tarjeta de voz a ninguno
      voiceCards[i].style.border = "none";
    }
  }
}


</script>

<script>
    const voices = [
        { value: 'es-MX-BeatrizNeural', label: 'Beatriz' },
        { value: 'es-MX-CandelaNeural', label: 'Candela' },
        { value: 'es-MX-CarlotaNeural', label: 'Carlota' },
        { value: 'es-MX-LarissaNeural', label: 'Larissa' },
        { value: 'es-MX-MarinaNeural', label: 'Marina' },
        { value: 'es-MX-NuriaNeural', label: 'Nuria' },
        { value: 'es-MX-RenataNeural', label: 'Renata' },
        { value: 'es-MX-CecilioNeural', label: 'Cecilio' },
        { value: 'es-MX-GerardoNeural', label: 'Gerardo' },
        { value: 'es-MX-LibertoNeural', label: 'Liberto' },
        { value: 'es-MX-LucianoNeural', label: 'Luciano' },
        { value: 'es-MX-PelayoNeural', label: 'Pelayo' },
        { value: 'es-MX-YagoNeural', label: 'Yago' },
        // Agrega más voces con el mismo formato
    ];

    const voiceCards = document.getElementById('voiceCards');

    voices.forEach(voice => {
        const voiceCard = document.createElement('div');
        voiceCard.classList.add('voice-card');
        voiceCard.setAttribute('onclick', `selectVoice('${voice.value}')`);
        voiceCard.innerHTML = `
            <li class="media">
                <label data-value="${voice.value}">
                    <button type="button" class="music" onclick="playAudio('https://media.play.ht/voice-samples/${voice.value}.mp3', this)">
                        <i class="fa-solid fa-play"></i>
                    </button>
                    <img class="mr-2 ml-2" src="/media/icons/bandera_mexico.png" alt="" style="width: 25px; vertical-align: middle;">
                    <div class="media-body">
                        <h6 class="mt-3 mb-1">${voice.label}</h6>
                        <p></p>
                    </div>
                </label>
            </li><br><br>
        `;
        voiceCards.appendChild(voiceCard);

    });
</script>

<script>

    const musicData = [
    {
        value: 'ES_Empower_Osoku',
        label: 'Empower - Osoku',
        category: 'Hip-hop'
    },
    {
        value: 'ES_Fight_Club_Cushy',
        label: 'Fight Club - Cushy',
        category: 'Drift Phonk'
    },
    {
        value: 'ES_Neon_Lights_Neon_Dreams_Forever_Sunset',
        label: 'Neon Lights Neon Dreams Forever - Sunset',
        category: 'Synthwave'
    },
    { value: 'ES_Sleepy_Hungry_baegel', label: 'Sleepy Hungry - Baegel' },
    { value: 'ES_Streamer_Bonkers_Beat_Club', label: 'Streamer Bonkers Beat - Club' },
    { value: 'ES_SUPRA_STRLGHT', label: 'Supra - Strlght' }
    // Agrega más pistas con el mismo formato
];

const musicCards = document.getElementById('musicCards');

// Crear las tarjetas de música dinámicamente
musicData.forEach(music => {
    const musicCard = document.createElement('div');
    musicCard.classList.add('music-card');
    musicCard.setAttribute('onclick', `selectMusic('${music.value}')`);
    musicCard.innerHTML = `
        <li class="media">
            <label data-value="${music.value}">
                <button type="button" class="music" onclick="playMusic('/static/video_tiktok/sonidos/music/${music.value}.mp3')">

                    <i class="fa-solid fa-music mr-3"></i>
                </button>
                <div class="media-body">
                    <h6 class="mt-3 mb-1 ml-3">${music.label}</h6>
                    <p class="category ml-3" style="color: rgba(255, 255, 255, 0.5);">${music.category ? music.category : 'No category'}</p>
                </div>
            </label>
        </li><br>
    `;
    musicCards.appendChild(musicCard);
});

</script>

<script>
    // Define una función que cambie el valor del menú desplegable y marque la tarjeta de la música
function selectMusic(musicValue) {
  // Obtiene el elemento del menú desplegable de música por su id
  var musicSelection = document.getElementById("musicSelection");
  // Cambia el valor del menú desplegable al valor de la música seleccionada
  musicSelection.value = musicValue;

  // Obtiene todas las tarjetas de música por su clase
  var musicCards = document.getElementsByClassName("music-card");

  // Recorre todas las tarjetas de música
  for (var i = 0; i < musicCards.length; i++) {
    // Obtiene la etiqueta de la tarjeta de música actual
    var musicLabel = musicCards[i].querySelector("label");
    // Comprueba si el valor de la etiqueta coincide con el valor de la música seleccionada
    if (musicLabel.getAttribute("data-value") == musicValue) {
      // Cambia el borde de la tarjeta de música a azul brillante
      musicCards[i].style.border = "1px solid blue";
    } else {
      // Cambia el borde de la tarjeta de música a ninguno
      musicCards[i].style.border = "none";
    }
  }
}
</script>

<script>
    let currentMusic = null;

    function playMusic(musicUrl) {
        const audio = new Audio(musicUrl);

        if (currentMusic && currentMusic.src === audio.src) {
            if (currentMusic.paused) {
                currentMusic.play().catch(error => {
                    console.error('Error al reanudar audio:', error);
                });
            } else {
                currentMusic.pause();
            }
        } else {
            if (currentMusic) {
                currentMusic.pause();
            }
            currentMusic = audio;
            currentMusic.play().catch(error => {
                console.error('Error al reproducir audio:', error);
            });
        }
    }



</script>

