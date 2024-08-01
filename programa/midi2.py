import pyaudio
import rtmidi


# Configuración de PyAudio para el dispositivo de entrada de audio
def select_input_device(p):
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')

    for i in range(num_devices):
        if p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels') > 0:
            print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
    return 1 #indice de input audio device

# Función para manejar mensajes MIDI entrantes y enviarlos a FluidSynth
def midi_callback(message):
    global fluidsynth_process
    #midi_message, _ = message
    print("Mensaje MIDI recibido:", message)
    fluidsynth_note_on(fluidsynth_path, 1,64,127)


def main():
    try:
        # Configuración de PyAudio para capturar audio (si es necesario)
        p = pyaudio.PyAudio()
        input_device_index = select_input_device(p)
        print("Input Device Selected:", input_device_index)
        stream = p.open(
            format=pyaudio.paInt24,
            channels=1,
            rate=44100,
            frames_per_buffer=1024,
            input=True,
            input_device_index=input_device_index
        )
        # Configurar FluidSynth y MIDI
        soundfont_path = r'C:\Users\Alumno\midiproject\soundfonts\Deep_Voice.SF2'  # Reemplaza con la ruta correcta
        midi_file = r'C:\Users\Alumno\midiproject\midifiles\midi.mid'  # Reemplaza con la ruta correcta
        fluidsynth_process = setup_fluidsynth_and_midi(soundfont_path, midi_file)

        # Mantener el programa en ejecución
        print("Presiona Ctrl+C para salir...")
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nSaliendo del programa...")

    except Exception as e:
        print(f"Ocurrió un error: {e}")

    finally:
        # Detener y cerrar todos los recursos
        if 'stream' in locals() and stream.is_active():
            stream.stop_stream()
            stream.close()
        if 'midiin' in locals():
            midiin.close_port()
        if 'fluidsynth_process' in locals():
            fluidsynth_process.kill()

if __name__ == "__main__":
    main()