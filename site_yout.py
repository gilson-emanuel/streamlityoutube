import streamlit as st
import yt_dlp as youtube_dl
import os
from io import BytesIO

# Título do app
st.title("Download de Vídeos do YouTube (MP4)")

# Input para o usuário inserir a URL do vídeo
video_url = st.text_input("Insira a URL do vídeo do YouTube:")

# Checkbox para baixar apenas o áudio (MP3)
download_audio = st.checkbox("Baixar apenas o áudio (MP3)")

# Seleção de qualidade do vídeo
quality = st.selectbox(
    "Escolha a qualidade do vídeo:",
    ("Melhor Qualidade", "Qualidade Média", "Baixa Qualidade")
)

# Função para determinar a qualidade com base na escolha
def get_quality_format(quality_choice):
    if quality_choice == "Melhor Qualidade":
        return "bestvideo+bestaudio/best"  # Melhor qualidade de vídeo e áudio
    elif quality_choice == "Qualidade Média":
        return "18"  # Qualidade média, normalmente 360p ou 480p
    elif quality_choice == "Baixa Qualidade":
        return "160"  # Baixa qualidade, normalmente 144p
    return "best"  # Caso padrão, melhor qualidade

# Botão para iniciar o download
if st.button("Baixar"):
    if video_url:
        # Caminho para salvar o vídeo
        output_path = 'downloads/%(title)s.%(ext)s'
        ydl_opts = {
            'outtmpl': output_path,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            },
            'cookiefile': 'cookies.txt',  # Arquivo de cookies para contornar a verificação
        }

        # Se o usuário escolher baixar apenas o áudio
        if download_audio:
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        else:
            # Define a qualidade do vídeo com base na escolha do usuário
            ydl_opts['format'] = get_quality_format(quality)

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                # Baixar o vídeo e armazenar em um buffer
                info = ydl.extract_info(video_url)
                file_name = ydl.prepare_filename(info)  # Nome do arquivo baixado
                with open(file_name, 'rb') as f:
                    video_data = f.read()

                # Download automático pelo navegador
                st.success("Download concluído com sucesso!")
                st.download_button(
                    label="Baixar Arquivo",
                    data=video_data,
                    file_name=os.path.basename(file_name),
                    mime="video/mp4" if not download_audio else "audio/mp3"
                )

        except Exception as e:
            st.error(f"Erro ao baixar o vídeo: {e}")
    else:
        st.warning("Por favor, insira uma URL válida.")
