# Projeto 1 - Um simulador super básico de circuitos lógicos

### Universidade Estadual de Campinas

### Instituto de Computação

### MO601 – Arquitetura de Computadores II

### Prof. Rodolfo Jardim de Azevedo

### Aluno: Rubens de Castro Pereira - RA 217146

___

Este repositório contém todos os artefatos do Projeto 1 que implementa um simulador super básico de circuitos lógicos.

O **relatório compacto** do projeto pode ser acessado [aqui](https://github.com/rubenscp/RCP-MO601-Project-01/blob/main/relatorio.pdf).

Siga as instruções abaixo para a execução completa dessa aplicação:

### 1. Clonar repositório do projeto

```
git clone https://github.com/rubenscp/RCP-MO601-Project-01.git
```
	
### 2. Acessar a pasta do projeto Python
	
```
cd RCP-MO601-Project-01
```
	
### 3. Adicionar novos testes ao simulador

```
Copiar os novos testes de simulação dentro da pasta "test".
```

### 4. Criar imagem docker da aplicação Python
	
```
reposicionar novamente na pasta raiz do projeto *RCP-MO601-Project-01*
```
```
docker build -t projeto-01:1.0 .
```

### 5. Criar volume docker para o mapeamento da pasta do projeto no seu computador

```
docker volume create projeto-01-volume
```

### 6. Executar o container docker

```
docker run --name projeto-01 -v projeto-01-volume:/app/test projeto-01:1.0
```
	
### 7. Copiar os arquivos dos resultados para a pasta local

```
docker cp projeto-01:/app/test/. test/.
```
    
### 8. Visualização dos resultados da simulação


Todos os resultados das simulações (*saida0.csv* e *saida1.csv*) estarão posicionados nas pastas específicas dos testes.

___

### Comandos Docker auxiliares para o projeto

#### Remover o container "projeto-01"

```
docker rm projeto-01
```

#### Remover a imagem "projeto-01:1.0"

```
docker rmi projeto-01:1.0
```

#### Remover o volume "projeto-01:volume"

```
docker volume rm projeto-01-volume
```

#### Listar todos os containeres

```
docker container ls -a
```

#### Listar todas as imagens

```
docker images 
```

#### Listar todos os volumes

```
docker volume ls
```
