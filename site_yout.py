import streamlit as st
import yt_dlp as youtube_dl
import os
from io import BytesIO

# Título do app
st.title("Download de Vídeos do YouTube (MP4)")

# Input para o usuário inserir a URL do vídeo
video_url = st.text_input("Insira a URL do vídeo do YouTube:")

# Inicializa as opções de qualidade
quality_options = []
formats = []
downloaded_file = None

# Se o vídeo foi inserido, extrair as opções de qualidade disponíveis
if video_url:
    try:
        ydl_opts = {
            'quiet': True,
            'cookiefile': 'cookies.txt',  # Arquivo de cookies, se necessário
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            # Extrai as informações do vídeo, incluindo os formatos
            info_dict = ydl.extract_info(video_url, download=False)
            formats = info_dict.get('formats', None)

            # Preenche a lista de qualidades disponíveis (apenas MP4)
            for f in formats:
                ext = f.get('ext', '')
                resolution = f.get('resolution', 'Unknown resolution')
                format_id = f.get('format_id')
                
                # Filtra apenas formatos em mp4
                if ext == 'mp4':
                    quality_options.append(f"{format_id} - {resolution} ({ext})")
    
    except Exception as e:
        st.error(f"Erro ao extrair informações do vídeo: {e}")

# Se houver opções de qualidade disponíveis, mostre para o usuário
if quality_options:
    selected_quality = st.selectbox("Escolha a qualidade do vídeo (somente MP4):", quality_options)

# Botão para iniciar o download
if st.button("Baixar"):
    if video_url:
        ydl_opts = {
            'format': 'mp4',  # Garantir que o formato será MP4
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            },
            'cookiefile': 'cookies.txt',  # Arquivo de cookies para contornar a verificação
            'outtmpl': '%(title)s.%(ext)s',  # Definir o nome do arquivo de saída
        }

        # Se o usuário escolheu um formato específico
        if selected_quality:
            format_id = selected_quality.split(" - ")[0]  # Extrair o ID do formato escolhido
            ydl_opts['format'] = format_id

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                # Baixar o vídeo para um buffer
                info = ydl.extract_info(video_url, download=False)
                buffer = BytesIO()
                ydl.download([video_url])
                
                file_name = ydl.prepare_filename(info)  # Nome do arquivo
                with open(file_name, 'rb') as f:
                    buffer.write(f.read())
                    buffer.seek(0)

                # Download automático pelo navegador
                st.success(f"Download concluído: {file_name}")
                st.download_button(
                    label="Clique para baixar automaticamente",
                    data=buffer,
                    file_name=os.path.basename(file_name),
                    mime="video/mp4"
                )

        except Exception as e:
            st.error(f"Erro ao baixar o vídeo: {e}")
    else:
        st.warning("Por favor, insira uma URL válida.")
