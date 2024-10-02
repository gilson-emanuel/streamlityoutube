import streamlit as st
import yt_dlp as youtube_dl

# Título do app
st.title("Download de Vídeos do YouTube")

# Input para o usuário inserir a URL do vídeo
video_url = st.text_input("Insira a URL do vídeo do YouTube:")

# Inicializa as opções de qualidade
quality_options = []
formats = []

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

            # Preenche a lista de qualidades disponíveis
            for f in formats:
                format_id = f.get('format_id')
                format_note = f.get('format_note', 'Unknown quality')  # Usa 'Unknown quality' se 'format_note' não estiver presente
                ext = f.get('ext', 'Unknown format')  # Usa 'Unknown format' se 'ext' não estiver presente
                quality_options.append(f"{format_id} - {format_note} ({ext})")
    
    except Exception as e:
        st.error(f"Erro ao extrair informações do vídeo: {e}")

# Se houver opções de qualidade disponíveis, mostre para o usuário
if quality_options:
    selected_quality = st.selectbox("Escolha a qualidade do vídeo:", quality_options)

# Checkbox para baixar apenas o áudio (MP3)
download_audio = st.checkbox("Baixar apenas o áudio (MP3)")

# Botão para iniciar o download
if st.button("Baixar"):
    if video_url:
        ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',
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
            # Se o usuário escolheu um formato específico
            if selected_quality:
                format_id = selected_quality.split(" - ")[0]  # Extrair o ID do formato escolhido
                ydl_opts['format'] = format_id

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            st.success("Download concluído com sucesso!")
        except Exception as e:
            st.error(f"Erro ao baixar o vídeo: {e}")
    else:
        st.warning("Por favor, insira uma URL válida.")
