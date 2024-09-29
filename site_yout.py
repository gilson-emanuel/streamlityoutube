import streamlit as st
import yt_dlp as youtube_dl

# Título do app
st.title("Download de Vídeos do YouTube")

# Input para o usuário inserir a URL do vídeo
video_url = st.text_input("Insira a URL do vídeo do YouTube:")

# Opções de qualidade de vídeo
quality_option = st.selectbox(
    "Escolha a qualidade do vídeo:",
    ("Melhor Qualidade", "Qualidade Média", "Menor Qualidade")
)

# Checkbox para baixar apenas o áudio (MP3)
download_audio = st.checkbox("Baixar apenas o áudio (MP3)")

# Botão para iniciar o download
if st.button("Baixar"):
    if video_url:
        # Configuração inicial das opções de download
        ydl_opts = {
            'format': 'best',  # Padrão: melhor qualidade
            'outtmpl': 'downloads/%(title)s.%(ext)s',  # Onde o arquivo será salvo
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            }
        }

        # Ajustar a qualidade com base na seleção do usuário
        if quality_option == "Melhor Qualidade":
            ydl_opts['format'] = 'best'
        elif quality_option == "Qualidade Média":
            ydl_opts['format'] = '18'  # Código para qualidade média (720p)
        elif quality_option == "Menor Qualidade":
            ydl_opts['format'] = 'worst'

        # Se o usuário escolher baixar apenas o áudio
        if download_audio:
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(video_url, download=True)
                video_title = ydl.prepare_filename(info_dict)

            st.success(f"Download concluído! O arquivo foi salvo como: {video_title}")
        except Exception as e:
            st.error(f"Erro ao baixar o vídeo: {e}")
    else:
        st.warning("Por favor, insira uma URL válida.")
