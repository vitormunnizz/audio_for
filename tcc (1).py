# -*- coding: utf-8 -*-
"""tcc.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Jp9WFHcoUD_UM3dbxURsxJo_2GMfgqjr
"""

import os
import librosa
import librosa.display
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
import random
import shutil

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# Montar o Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Caminho para os dados no Google Drive
file_path_real = '/content/drive/MyDrive/amostra_FOR/real'
file_path_fake = '/content/drive/MyDrive/amostra_FOR/fake'

# Listar os arquivos e subpastas
print(os.listdir(file_path_real))
print(os.listdir(file_path_fake))

# Função para processar os áudios em uma pasta
def process_audio_files(folder_path):

    for audio_file in os.listdir(folder_path):
        audio_path = os.path.join(folder_path, audio_file)

        # Carregar o áudio
        y, sr = librosa.load(audio_path, sr=None)

        # Mostrar informações do áudio
        print(f"Arquivo: {audio_file}, Duração: {len(y) / sr:.2f}s, Taxa de amostragem: {sr}Hz")

        # Plotar waveform
        plt.figure(figsize=(10, 4))
        librosa.display.waveshow(y, sr=sr)
        plt.title(f"Waveform de {audio_file}")
        plt.xlabel("Tempo (s)")
        plt.ylabel("Amplitude")
        plt.show()

# Processar áudios Real
#process_audio_files(file_path_real)

# Processar áudios Fake
#process_audio_files(file_path_fake)

# Função para extrair MFCCs de um arquivo
def extract_features(file_path):
    y, sr = librosa.load(file_path, sr=None)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfccs.T, axis=0)  # Média dos coeficientes

# Carregar dados e rótulos
data = []
labels = []

# Processar Fake
for file_name in os.listdir(file_path_fake):
    file_path = os.path.join(file_path_fake, file_name)
    features = extract_features(file_path)
    data.append(features)
    labels.append(0)  # Rótulo 0 para Fake

# Processar Real
for file_name in os.listdir(file_path_real):
    file_path = os.path.join(file_path_real, file_name)
    features = extract_features(file_path)
    data.append(features)
    labels.append(1)  # Rótulo 1 para Real

# Converter para DataFrame
df = pd.DataFrame(data)
df['label'] = labels

df

# Separar características (X) e rótulos (y)
X = df.drop(columns=['label'])
y = df['label']

# Dividir em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinando um modelo de regressão linear
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# Fazendo previsões no conjunto de teste
y_pred = regressor.predict(X_test)

# Calculando métricas de avaliação
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Erro Absoluto Médio (MAE): {mae:.2f}")
print(f"Coeficiente de Determinação (R²): {r2:.2f}")

def cut_and_resize(audio, sr, target_length, num_versions=3):

    target_samples = int(target_length * sr)  # Convertendo segundos para amostras
    versions = []

    for _ in range(num_versions):
        # Se o áudio for maior, corte em uma posição aleatória
        if len(audio) > target_samples:
            start = np.random.randint(0, len(audio) - target_samples)
            resized_audio = audio[start:start + target_samples]
        else:
            # Se for menor, preencha com zeros
            resized_audio = np.pad(audio, (0, target_samples - len(audio)), 'constant')

        versions.append(resized_audio)

    return versions

def augment_and_create_combined_dir(input_dir, combined_dir, target_length=5, num_versions=3):

    # Criar diretório consolidado
    os.makedirs(combined_dir, exist_ok=True)

    # Iterar sobre os arquivos no diretório de entrada
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".wav"):
            file_path = os.path.join(input_dir, file_name)

            # Copiar o arquivo original para o diretório consolidado
            shutil.copy(file_path, os.path.join(combined_dir, file_name))

            # Carrega o áudio
            audio, sr = librosa.load(file_path, sr=None)

            # Aplicar corte e redimensionamento
            augmented_versions = cut_and_resize(audio, sr, target_length, num_versions=num_versions)

            # Salvar áudios aumentados no diretório consolidado
            base_name = os.path.basename(file_name).split('.')[0]
            for i, augmented_audio in enumerate(augmented_versions):
                augmented_file_name = f"{base_name}_augmented_{i + 1}.wav"
                output_file = os.path.join(combined_dir, augmented_file_name)
                write(output_file, sr, augmented_audio)

# Caminho para os dados no Google Drive
file_path_real = '/content/drive/MyDrive/amostra_FOR/real'
file_path_fake = '/content/drive/MyDrive/amostra_FOR/fake'

# Diretórios para os dados combinados
combined_dir_real = '/content/drive/MyDrive/amostra_FOR_combined/real'
combined_dir_fake = '/content/drive/MyDrive/amostra_FOR_combined/fake'

# Processar ambas as categorias e criar diretórios consolidados com múltiplas versões
augment_and_create_combined_dir(file_path_real, combined_dir_real, target_length=5, num_versions=3)
augment_and_create_combined_dir(file_path_fake, combined_dir_fake, target_length=5, num_versions=3)

# Função para extrair MFCCs de um arquivo
def extract_features(file_path):
    y, sr = librosa.load(file_path, sr=None)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfccs.T, axis=0)  # Média dos coeficientes

# Carregar dados e rótulos
data = []
labels = []

# Processar Fake
for file_name in os.listdir(combined_dir_fake):
    file_path = os.path.join(combined_dir_fake, file_name)
    features = extract_features(file_path)
    data.append(features)
    labels.append(0)  # Rótulo 0 para Fake

# Processar Real
for file_name in os.listdir(combined_dir_real):
    file_path = os.path.join(combined_dir_real, file_name)
    features = extract_features(file_path)
    data.append(features)
    labels.append(1)  # Rótulo 1 para Real

# Converter para DataFrame
df = pd.DataFrame(data)
df['label'] = labels

df

# Separar características (X) e rótulos (y)
X = df.drop(columns=['label'])
y = df['label']

# Dividir em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinando um modelo de regressão linear
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# Fazendo previsões no conjunto de teste
y_pred = regressor.predict(X_test)

# Calculando métricas de avaliação
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Erro Absoluto Médio (MAE): {mae:.2f}")
print(f"Coeficiente de Determinação (R²): {r2:.2f}")

def mix_with_other_audio(audio, sr, input_dir, num_mixes=2):
    """
    Mistura o áudio original com outros áudios do mesmo diretório.
    """
    mixed_versions = []
    audio_files = [f for f in os.listdir(input_dir) if f.endswith(".wav")]

    for _ in range(num_mixes):
        # Escolher um arquivo aleatório para mistura
        other_file = random.choice(audio_files)
        other_path = os.path.join(input_dir, other_file)

        # Carregar o áudio a ser misturado
        other_audio, _ = librosa.load(other_path, sr=sr)

        # Ajustar o tamanho do áudio misturado
        min_length = min(len(audio), len(other_audio))
        audio = audio[:min_length]
        other_audio = other_audio[:min_length]

        # Misturar os áudios com pesos aleatórios
        weight_original = random.uniform(0.5, 0.9)  # Peso para o áudio original
        weight_other = 1.0 - weight_original        # Peso complementar para o outro áudio
        mixed_audio = (weight_original * audio) + (weight_other * other_audio)
        mixed_audio = mixed_audio / np.max(np.abs(mixed_audio))  # Normalizar

        mixed_versions.append(mixed_audio)

    return mixed_versions

def generate_mixed_data(input_dir, output_dir, num_mixes=2):
    """
    Aplica a mistura de áudios e salva os arquivos resultantes em uma nova pasta.
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        print(f"Diretório de saída '{output_dir}' criado com sucesso.")
    except Exception as e:
        print(f"Erro ao criar diretório de saída: {e}")
        return

    for file_name in os.listdir(input_dir):
        if file_name.endswith(".wav"):
            file_path = os.path.join(input_dir, file_name)

            # Carregar o áudio original
            audio, sr = librosa.load(file_path, sr=None)

            # Aplicar mistura com outros áudios do mesmo diretório
            mixed_versions = mix_with_other_audio(audio, sr, input_dir, num_mixes=num_mixes)

            # Salvar versões misturadas no diretório de saída
            base_name = os.path.basename(file_name).split('.')[0]
            for i, mixed_audio in enumerate(mixed_versions):
                mixed_file_name = f"{base_name}_mixed_{i + 1}.wav"
                output_file = os.path.join(output_dir, mixed_file_name)
                write(output_file, sr, mixed_audio)
                print(f"Áudio misturado salvo em: {output_file}")

# Diretórios de áudios redirecionados (cortes e redimensionados)
redirected_real = '/content/drive/MyDrive/amostra_FOR_combined/fake'
redirected_fake = '/content/drive/MyDrive/amostra_FOR_combined/real'

# Diretórios de saída para áudios misturados
output_dir_real_mixed = '/content/drive/MyDrive/amostra_FOR/real_mixed'
output_dir_fake_mixed = '/content/drive/MyDrive/amostra_FOR/fake_mixed'

# Gerar dados misturados a partir dos áudios redirecionados
generate_mixed_data(redirected_real, output_dir_real_mixed, num_mixes=2)
generate_mixed_data(redirected_fake, output_dir_fake_mixed, num_mixes=2)

# Função para extrair MFCCs de um arquivo
def extract_features(file_path):
    y, sr = librosa.load(file_path, sr=None)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfccs.T, axis=0)  # Média dos coeficientes

# Carregar dados e rótulos
data = []
labels = []

# Processar Fake
for file_name in os.listdir(output_dir_fake_mixed):
    file_path = os.path.join(output_dir_fake_mixed, file_name)
    features = extract_features(file_path)
    data.append(features)
    labels.append(0)  # Rótulo 0 para Fake

# Processar Real
for file_name in os.listdir(output_dir_real_mixed):
    file_path = os.path.join(output_dir_real_mixed, file_name)
    features = extract_features(file_path)
    data.append(features)
    labels.append(1)  # Rótulo 1 para Real

# Converter para DataFrame
df = pd.DataFrame(data)
df['label'] = labels

df

import os
import random
import librosa
import numpy as np
from scipy.io.wavfile import write

def mix_with_other_audio(audio, sr, input_dir, num_mixes=2):
    """
    Mistura o áudio original com outros áudios do mesmo diretório.
    """
    mixed_versions = []
    audio_files = [f for f in os.listdir(input_dir) if f.endswith(".wav")]

    for _ in range(num_mixes):
        # Escolher um arquivo aleatório para mistura
        other_file = random.choice(audio_files)
        other_path = os.path.join(input_dir, other_file)

        # Carregar o áudio a ser misturado
        other_audio, _ = librosa.load(other_path, sr=sr)

        # Ajustar o tamanho do áudio misturado
        min_length = min(len(audio), len(other_audio))
        audio = audio[:min_length]
        other_audio = other_audio[:min_length]

        # Misturar os áudios com pesos aleatórios
        weight_original = random.uniform(0.5, 0.9)  # Peso para o áudio original
        weight_other = 1.0 - weight_original        # Peso complementar para o outro áudio
        mixed_audio = (weight_original * audio) + (weight_other * other_audio)
        mixed_audio = mixed_audio / np.max(np.abs(mixed_audio))  # Normalizar

        mixed_versions.append(mixed_audio)

    return mixed_versions

def generate_mixed_data(input_dir, output_dir, num_mixes=2, subfolder_name="amostra_FOR_mixed"):
    """
    Aplica a mistura de áudios e salva os arquivos resultantes em uma nova pasta com subpastas 'fake' e 'real'.
    """
    # Criar a pasta consolidada 'amostra_FOR_mixed' fora de 'amostra_FOR'
    combined_dir = os.path.join(output_dir, subfolder_name)
    os.makedirs(combined_dir, exist_ok=True)  # Criar o diretório consolidado
    print(f"Diretório '{combined_dir}' criado com sucesso.")

    # Subpastas 'fake' e 'real' dentro de 'amostra_FOR_mixed'
    fake_folder = os.path.join(combined_dir, 'fake')
    real_folder = os.path.join(combined_dir, 'real')
    os.makedirs(fake_folder, exist_ok=True)
    os.makedirs(real_folder, exist_ok=True)

    for file_name in os.listdir(input_dir):
        if file_name.endswith(".wav"):
            file_path = os.path.join(input_dir, file_name)

            # Carregar o áudio original
            audio, sr = librosa.load(file_path, sr=None)

            # Aplicar mistura com outros áudios do mesmo diretório
            mixed_versions = mix_with_other_audio(audio, sr, input_dir, num_mixes=num_mixes)

            # Salvar versões misturadas nos diretórios 'fake' ou 'real' dependendo do nome
            base_name = os.path.basename(file_name).split('.')[0]
            for i, mixed_audio in enumerate(mixed_versions):
                mixed_file_name = f"{base_name}_mixed_{i + 1}.wav"
                if 'fake' in file_name.lower():
                    output_file = os.path.join(fake_folder, mixed_file_name)
                else:
                    output_file = os.path.join(real_folder, mixed_file_name)

                write(output_file, sr, mixed_audio)
                print(f"Áudio misturado salvo em: {output_file}")

# Diretórios de áudios redirecionados (cortes e redimensionados)
redirected_real = '/content/drive/MyDrive/amostra_FOR_combined/fake'
redirected_fake = '/content/drive/MyDrive/amostra_FOR_combined/real'

# Diretório de saída para áudios misturados
output_dir = '/content/drive/MyDrive'

# Gerar dados misturados a partir dos áudios redirecionados
generate_mixed_data(redirected_real, output_dir, num_mixes=2)
generate_mixed_data(redirected_fake, output_dir, num_mixes=2)

# Separar características (X) e rótulos (y)
X = df.drop(columns=['label'])
y = df['label']

# Dividir em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinando um modelo de regressão linear
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# Fazendo previsões no conjunto de teste
y_pred = regressor.predict(X_test)

# Calculando métricas de avaliação
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Erro Absoluto Médio (MAE): {mae:.2f}")
print(f"Coeficiente de Determinação (R²): {r2:.2f}")