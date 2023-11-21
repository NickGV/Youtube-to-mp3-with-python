import PySimpleGUI as sg
from pytube import YouTube
import os
import time
import win32clipboard


def get_clipboard_content():
    win32clipboard.OpenClipboard()
    clipboard_content = win32clipboard.GetClipboardData(
        win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()
    return clipboard_content


def download_video(url, output_folder):
    try:
        video = YouTube(url)
        stream = video.streams.filter(only_audio=True).first()
        out_path = stream.download(output_folder)
        
        new_name = os.path.splitext(out_path)
        os.rename(out_path, os.path.join(output_folder, new_name[0] + '.mp3'))
        print(f'Descarga completada para {video.title}')
        sg.popup("Descarga completada", f"El video {video.title} se ha descargado correctamente.")
    except Exception as e:
        print(f"Error al descargar el video {video.title}: {e}")


def main():
    last_clipboard_content = None

    layout = [
        [sg.Text("Ingrese la URL de YouTube:")],
        [sg.InputText(key="-URL-")],
        [sg.Text("Seleccione la carpeta de destino:")],
        [sg.InputText(key="-OUTPUT_FOLDER-"), sg.FolderBrowse()],
        [sg.Button("Descargar"), sg.Button("Salir")]
    ]

    window = sg.Window("Descargador de YouTube", layout)

    while True:
        event, values = window.read(timeout=1000)

        if event == sg.WINDOW_CLOSED or event == "Salir":
            break

        clipboard_content = get_clipboard_content()

        if clipboard_content != last_clipboard_content and "youtube.com" in clipboard_content:
            window["-URL-"].update(clipboard_content)
            download_video(clipboard_content, values["-OUTPUT_FOLDER-"])
            last_clipboard_content = clipboard_content

    window.close()


if __name__ == "__main__":
    main()
