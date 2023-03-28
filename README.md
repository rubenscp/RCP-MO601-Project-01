# Projeto 1 - Um simulador super básico de circuitos lógicos

Este repositório tem o propósito de armazenar todos os artefatos do Projeto 1 que implementa 
um simulador super básico de circuito lógico. 

<!-- This repository has the main aim to store the assignments of the discipline Computer Architecture II of the Computer Science Pos-graduation Course of the Institute of Computation of UNICAMP. -->

Siga as instruções abaixo para a execução completa dessa aplicação:

## 1. Clonar repositório do projeto

```
git clone https://github.com/rubenscp/RCP-MO601-Project-01.git
```
	
## 2. Acessar a pasta do projeto Python
	
```
cd RCP-MO601-Project-01
```
	
## 3. Adição de novos testes ao simulador
```
Copiar os novos testes de simulação dentro da pasta "test".
```

## 4. Criação da imagem docker da aplicação Python
	
```
reposicionar novamente  na pasta raiz do projeto "RCP-MO601-Project-01"
```
```
docker build -t projeto-01:1.0 .
```

## 5. Criação do volume docker para mapear pasta no seu computador

```
docker volume create projeto-01-volume
```

## 6. Execução do container docker

```
docker run --name projeto-01 -v projeto-01-volume:/app/test projeto-01:1.0
```
	
## 7. Copiar os arquivos resultados para a pasta local

```
docker cp projeto-01:/app/test/. test/.
```
    
## 8. Resultados da simulação


Todos os resultados das simulações (*saida0.csv* e *saida1.csv*) estarão posicionados nas respectivas pastas de testes.

