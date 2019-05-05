################################################################################
#
# Este é um exercício de avaliação da disciplina de IA.
#
# O código traz um esqueleto para a implementação de um algoritmo genético
# para resolver o problema da mochila (Knapsack).
#
# O Objetivo do exercício é implementar o que falta do algoritmo no código abaixo.
# Os métodos que precisam ser implementados estão com a marcação "TODO" seguida
# de uma descrição do que precisa ser feito.
#
# Leia atentamente todo os comentários no código.
#
# Se o programa estiver executando corretamente, ele deve exibir cada geração
# de soluções criadas, mostrando o fitness de cada indivíduo e o peso da mochila
# para cada solução.
#
################################################################################

from random import sample, randint
from operator import itemgetter


class GA(object):
    """
    Esta é a classe principal do algoritmo genético para resolver o problema da mochila.
    """

    def __init__(self, n_objects, generation_size, max_weight,
                 max_weight_penalty, crossover_point, solutions_per_tournament):

        """
        Construtor.

        No construtor, diversos parâmetros importantes para o algoritmo genético são
        inicializados.

        n_objects - número de objetos que podem ser escolhidos para colocar na mochila.
        generation_size - número de indivíduos por geração.
        max_weight - peso máximo suportado pela mochila.
        max_weight_penalty - constante que penaliza soluções que ultrapassem o peso máximo
                             suportado pela mochila.
        crossover_point - ponto de corte na recombinação de 1 ponto. Por exemplo, se o crossover_point
                          for igual a 2, isso significa que o corte é feito APÓS o segundo gene.
        solutions_per_tournament - número de indivíduos que são escolhidos para seleção por torneio.
        """

        self.n_objects = n_objects
        self.generation_size = generation_size
        self.max_weight = max_weight
        self.max_weight_penalty = max_weight_penalty
        self.crossover_point = crossover_point
        self.solutions_per_tournament = solutions_per_tournament

        # Objetos e indivíduos são inicializados aleatoriamente
        self.objects = self.create_objects()
        self.generation = self.start_generation()

    def create_objects(self):
        # TODO: este método cria os objetos disponíveis para serem colocados na mochila.
        #
        # Um objeto possui valor e peso e essas informações devem ser representadas como
        # um dicionário, por exemplo, {"value": 10, "weight": 5}. Os valores e os pesos
        # devem ser criados aleatoriamente, mas os nomes das chaves "value" e "weight"
        # precisam ser exatamente esses.
        #
        # Por fim, este método deve retornar uma lista com todos os objetos criados.
        # Lembre-se que o número de objetos que deve ser criado está especificado no
        # construtor.

        list_objects = []

        for i in range(self.n_objects):
            list_objects.append({"value": randint(1, self.n_objects), "weight": randint(0, self.max_weight)})

        return list_objects

    def start_generation(self):
        # TODO: este método cria e retorna uma lista com os indivíduos da primeira geração.
        #
        # Nesse problema, os indivíduos são representados como uma lista de 0s e 1s.
        # O tamanho da lista é igual a quantidade de objetos existentes.
        #
        # Um elemento 1 numa determinada posição do indivíduo significa que o objeto
        # daquela posição foi colocado na mochila. Um elemento 0 significa que o objeto
        # daquela posição não foi colocado.
        #
        # Por exemplo, se temos 5 objetos, o indivíduo [1, 0, 1, 0, 0] é uma solução
        # que específica que o primeiro e o terceiro objeto foram colocados na mochila.
        #
        # Na primeira geração, os indivíduos são criados aleatoriamente.
        # Lembre-se que a quantidade de objetos e o tamanho da geração são especificados
        # no construtor.
        
        first_generation_individuals = []
        for i in range(self.generation_size):
            aux_list = []
            for j in range(self.n_objects):
                aux_list.append(randint(0, 1))
            
            try:
                has_put_item = aux_list.index(1)

            except ValueError:
                print(aux_list)
                random_index = randint(0, 4)
                aux_list[random_index] = 1

            first_generation_individuals.append(aux_list)
        
        return first_generation_individuals

    def fitness(self, solution):
        # TODO: este método calcula e retorna o fitness de um indivíduo.
        #
        # Um indivíduo é codificado como uma lista de 0s e 1s e o seu fitness é
        # o valor total dos objetos que ele representa. Os comentários do método
        # start_generation() traz a explicação de como um indivíduo é codificado.
        #
        # A mochila tem um peso máximo suportado, quando os pesos dos objetos passarem desse
        # limite, o fitness deve sofrer uma penalização calculada por:
        # (peso total dos objetos - peso total suportado)*max_weight_penalty
        #
        # O parâmetro solution é o indivíduo que terá seu fitness calculado.

        total_individual_weight = self.weight(solution)

        if(total_individual_weight > self.max_weight):
            last_index = 0
            for i in range(len(solution)):
                if(solution[i]): last_index = i
            
            total_individual_weight = (self.objects[last_index]['value'] - self.max_weight) * self.max_weight_penalty

        return total_individual_weight

    def weight(self, solution):
        # TODO: este método calcula e retorna o peso total de um indivíduo.
        #
        # O parâmetro solution é o indivíduo que terá seu peso calculado.
        
        total_individual_weight = 0

        for i in range(len(solution)):
            if(solution[i]):
                total_individual_weight += self.objects[i]['weight']
            
        return total_individual_weight

    def recombine(self, parent1, parent2):
        # TODO: este método faz a recombinação de 1 ponto dos pais passados como
        # parâmetro (parent1 e parent2). O ponto de corte é especificado pelo
        # parâmetro crossover_point passado no construtor.
        #
        # Após efetuar a recombinação, o método retorna uma lista com os dois
        # filhos gerados.

        children_1 = []
        children_2 = []

        for i in range(len(parent1)):
            if(i >= self.crossover_point):
                children_1.append(parent2[i])
                children_2.append(parent1[i])
            else:
                children_1.append(parent1[i])
                children_2.append(parent2[i])

        return [children_1, children_2]

    def compete(self, solutions):
        # TODO: na seleção por torneio, um conjunto de indivíduos disputa um torneio
        # e apenas o de maior fitness é selecionado. Este método recebe uma lista
        # de indivíduos (parâmetro solutions) e retorna o indivíduo de maior fitness.

        bigger_fitness_value = self.fitness(solutions[0])
        bigger_fitness_individuals = solutions[0]

        for solution in solutions:
            fitness = self.fitness(solution)
            if(fitness >= bigger_fitness_value):
                bigger_fitness_value = fitness
                bigger_fitness_individuals = solution

        return bigger_fitness_individuals

    def next_generation(self):
        """
        Este método cria uma nova geração a partir da geração atual.
        """
        new_generation = []

        for i in range(self.generation_size//2):
            # torneio para selecionar o primeiro pai
            solutions = sample(self.generation, self.solutions_per_tournament)
            parent1 = self.compete(solutions)

            # torneio para selecionar o segundo pai
            solutions = sample(self.generation, self.solutions_per_tournament)
            parent2 = self.compete(solutions)

            children = self.recombine(parent1, parent2)
            new_generation.extend(children)

        self.generation = new_generation

    def print_generation(self):
        """
        Este método exibe a geração atual, mostrando cada indivíduo,
        seu fitness e seu peso total.
        """
        for solution in self.generation:
            fitness = self.fitness(solution)
            weight = self.weight(solution)

            print(f"{solution} - fitness: {fitness} - weight: {weight}")


if __name__ == "__main__":
    # Os parâmetros de inicialização do algoritmo genético podem ser
    # alterados na sua instanciação.
    ga = GA(5, 10, 15, 4, 3, 3)

    # Altere essa variável para mudar o número de gerações que o
    # algoritmo vai gerar.
    N_GENERATIONS = 10
    
    for i in range(N_GENERATIONS):
        ga.print_generation()
        print("---------------------")
        ga.next_generation()

    ga.print_generation()
    
