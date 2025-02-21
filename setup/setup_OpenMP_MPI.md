# Instalação MPI e OpenMP

Este documento descreve o processo realizado pelo grupo para instalar e configurar o **MPI** e o **OpenMP**.

## 1. Instalação dos Pacotes Necessários

Antes de iniciar, atualizamos o sistema e instalamos os pacotes essenciais:

```sh
sudo apt update && sudo apt upgrade -y
sudo apt install gcc g++ -y
```

Em seguida, instalamos os pacotes necessários para o **MPI**:

```sh
sudo apt install openmpi-bin openmpi-common libopenmpi-dev -y
```

## 2. Compilando e Executando um Programa OpenMP

O OpenMP já está incluído no **GCC**. Para compilar um programa com OpenMP, utilizamos a flag `-fopenmp`:

### Compilar e Executar

```sh
gcc -fopenmp openmp_exemplo.c -o openmp_exemplo
./openmp_exemplo
```

---

## 3. Compilando e Executando um Programa MPI

Para compilar um programa MPI, utilizamos o compilador `mpicc` e executamos com `mpirun`.

### Compilar e Executar

```sh
mpicc mpi_exemplo.c -o mpi_exemplo
mpirun -np 4 ./mpi_exemplo
```
---

Agora o **MPI** e o **OpenMP** estão configurados e prontos para uso.