from pytube import YouTube
import os
import PySimpleGUI as sg
import win32clipboard
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 150)

def talk(text):
    engine.say(text)
    
def get_clipboard_content():
    win32clipboard.OpenClipboard()
    clipboard_content = win32clipboard.GetClipboardData(
        win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()
    return clipboard_content


def download_video(url, output_folder, window):
    try:
        video = YouTube(url)
        stream = video.streams.filter(only_audio=True).first()
        out_path = stream.download(output_folder)

        new_name = os.path.splitext(out_path)
        os.rename(out_path, os.path.join(output_folder, new_name[0] + '.mp3'))
        print(f'Descarga completada para {video.title}')
        window["-STATUS-"].update(f"Descarga completada de {video.title}")
        window.write_event_value(
            '-UPDATE-', f"Descarga completada para {video.title}")
        talk(f"La descarga para {video.title} se ha completado.")
        engine.runAndWait()
    except Exception as e:
        print(f"Error al descargar el video  {e}")
        window.write_event_value(
            '-UPDATE-', f"Error al descargar el video  {e}")
        talk(f"Error al descargar el video {video.title}: {e}")
        engine.runAndWait()


def main():

    last_clipboard_content = None
    engine = pyttsx3.init()

    layout = [
        [sg.Text("Estoy listo para descargar música, copia el enlace de algún video en tu portapapeles o copialo aqui abajo ")],
        [sg.Text("Ingrese la URL de YouTube:")],
        [sg.InputText(key="-URL-")],
        [sg.Text("Seleccione la carpeta de destino:")],
        [sg.InputText(key="-OUTPUT_FOLDER-"), sg.FolderBrowse()],
        [sg.Button("Descargar"), sg.Button("Salir")],
        [sg.Text("", key="-STATUS-", size=(40, 5))]
    ]

    window = sg.Window("Descargador de YouTube", layout)

    while True:

        event, values = window.read(timeout=1000)

        if event == sg.WINDOW_CLOSED or event == "Salir":
            break

        if event == "Descargar":
            url = values["-URL-"]
            output_folder = values["-OUTPUT_FOLDER-"]

            if url and output_folder:
                window["-STATUS-"].update("Descargando...")
                download_video(url, output_folder, window)
                window["-STATUS-"].update("Descarga completada")
            else:
                window["-STATUS-"].update(
                    "Por favor, ingresa la URL y selecciona la carpeta de destino")

        clipboard_content = get_clipboard_content()

        if clipboard_content != last_clipboard_content and "youtube.com" in clipboard_content:
            window["-URL-"].update(clipboard_content)
            last_clipboard_content = clipboard_content
            window["-STATUS-"].update("Descargando...")
            download_video(clipboard_content,
                           values["-OUTPUT_FOLDER-"], window)

    window.close()


if __name__ == "__main__":
    main()
