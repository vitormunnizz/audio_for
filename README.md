# Detecção de Áudios Falsos (DeepFake) com Foco em Aumento de Dados

## Descrição do Projeto

Este projeto tem como objetivo principal desenvolver e avaliar um modelo de aprendizado de máquina robusto para a detecção de áudios sintéticos (DeepFake), com ênfase na utilização de técnicas de aumento de dados para melhorar a generalização e o desempenho do modelo. O crescente avanço das tecnologias de síntese de voz torna cada vez mais difícil diferenciar áudios autênticos de falsificações. Este projeto se concentra em explorar diversas técnicas de aumento de dados como meio de aprimorar a capacidade dos modelos de aprendizado de máquina em identificar áudios DeepFake, garantindo que o modelo seja capaz de generalizar bem para diferentes condições e variações nos dados.

## Dados

### Origem dos Dados
Os dados foram coletados e organizados em dois diretórios principais:

*   `real`: Contém amostras de áudios autênticos.
*   `fake`: Contém amostras de áudios gerados sinteticamente.

### Formato dos Dados
*   Arquivos de áudio no formato `.wav` e `.mp3`.
*   Amostras originais balanceadas para garantir representatividade das classes.

## Técnicas de Aumento de Dados

Um componente central deste projeto é a aplicação de diversas técnicas de aumento de dados para expandir o conjunto de treinamento e aumentar a robustez dos modelos. As seguintes técnicas foram utilizadas:

*   **Ruído:** Adição de ruído aleatório para simular diferentes condições de gravação e aumentar a resistência do modelo a ruídos.
*   **Inversão Temporal:** Inversão da ordem temporal do áudio, criando novas amostras com características temporais invertidas.
*   **Equalização Aleatória:** Aplicação de equalização com ganhos aleatórios para variar o espectro do áudio.

## Modelos Utilizados

Os seguintes modelos de aprendizado de máquina foram implementados e avaliados:

*   Random Forest
*   K-Nearest Neighbors (KNN)
*   XGBoost
*   LightGBM
*   Redes Neurais (DNN)
*   Decision Tree

### Processo de Avaliação

O desempenho dos modelos foi avaliado utilizando as seguintes métricas:

*   Acurácia: A proporção de predições corretas.
*   Precisão: A proporção de instâncias positivas previstas corretamente.
*   Recall: A proporção de instâncias positivas reais que foram previstas corretamente.
*   F1-Score: A média harmônica entre precisão e recall, fornecendo um balanço entre os dois.

## Resultados

A experimentação com diferentes técnicas de aumento de dados forneceu insights importantes sobre a robustez e a generalização dos modelos. Os resultados detalhados para cada modelo e conjunto de dados aumentado podem ser encontrados nos respectivos notebooks. O LightGBM apresentou as maiores métricas, sendo o melhor modelo para o problema de detecção dos áudios fakes neste dataset.

## Contato
Para dúvidas ou sugestões, entre em contato pelo e-mail: vitormunnizz@gmail.com.
