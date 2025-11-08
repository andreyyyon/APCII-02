# 2° Trabalho APCII

Este é um projeto desenvolvido para a disciplina de **Algoritmos e Programação de Computadores (APC II)** da Univille, que simula um sistema de gerenciamento de informações. O objetivo é aplicar e integrar diversos conceitos fundamentais da programação em Python.

Anteriormente desenvolvido apenas em terminal, agora será refatorado para utilização do framework Flask.

**Tema Escolhido**: Estacionamento

## Classe Veiculo
| Propriedade | Tipo   | Descrição                        | Visibilidade       |
|-------------|--------|----------------------------------|--------------------|
| placa       | String | Chave primaria do veículo		  |  Private           |
| modelo      | String | Modelo  do veículo		          |  Private           |
| cor         | String | Cor do veículo		              |  Private           |
| vaga        | String | Vaga ocupada pelo veículo		  |  Private           |

### Subclasse Carro
| Propriedade | Tipo   | Descrição                        | Visibilidade       |
|-------------|--------|----------------------------------|--------------------|
| tamanho     | String | Porte do veículo (M ou G)	      |  Private           |

### Subclasse Moto
| Propriedade | Tipo    | Descrição                                       | Visibilidade       |
|-------------|---------|-------------------------------------------------|--------------------|
| eletrica    | Boolean | Moto é elétrica? (True - Sim / False - Não)     | Private            | 

## Classe Estadia
| Propriedade  | Tipo    | Descrição                                             | Visibilidade       |
|--------------|---------|-------------------------------------------------------|--------------------|
| vaga         | String  | Vaga utilizada		                                 |  Private           |
| placa        | Boolean | Placa do carro que utilizou a vaga                    |  Private           |
| entrada      | String  | Data e hora da entrada                                |  Private           |
| saida        | String  | Data e hora da saída                                  |  Private           |

## Equipe

* Andrey Rebelatto
* Erick Anderson
* Eduardo Will
