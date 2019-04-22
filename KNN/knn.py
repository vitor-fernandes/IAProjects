"""
CSV Data Format:

sepallength, sepalwidth, petallength, petalwidth
"""
import operator
import csv
import sys

def get_csv_data(csv_file):
    with open(csv_file) as file:
        data = csv.reader(file)
        data_list = list(data)[1:]
        file.close()

        return data_list
    

def get_result_data(txt_file):
    file = open(txt_file, 'rb')

    tmp_data = []
    for data in file.readlines():
        tmp_data.append(data.decode().strip('\n'))
    
    return tmp_data

def euclidean_distance(data_test, data_train, length_data):
    total_distance = 0
    #              __________                
    # distance = \/(x1 - y1)²
    for i in range(length_data):
        total_distance += (float(data_test[i]) - float(data_train[i])) ** 2

    return total_distance ** (1/2)


def get_near_neighbors(data_test, data_train, k):
    all_distances = []

    data_test_length = len(data_test) - 1
    for x in range(len(data_train)):
        euclid_distance = euclidean_distance(data_test, data_train[x], data_test_length)
        all_distances.append((data_train[x], euclid_distance))

    all_distances.sort(key=operator.itemgetter(1))

    neighbors_for_k_value = []
    for x in range(k):
        neighbors_for_k_value.append(all_distances[x][0])

    return neighbors_for_k_value

def get_response(neighbors):
    classified_flowers = {}
    for x in range(len(neighbors)):
        flower = neighbors[x][-1]
        if(flower in classified_flowers): classified_flowers[flower] += 1
        else: classified_flowers[flower] = 1
    
    sorted_classified_flowers = sorted(classified_flowers.keys(), key=lambda flower: classified_flowers[flower], reverse=True)

    return sorted_classified_flowers[0][0]

def get_accuracy(result_file, data):
    correct_answers = 0
    wrong_answers = 0
    for x in range(len(result_file)):
        if(result_file[x] == data[x]): correct_answers += 1
        else: wrong_answers += 1

    print("Expected Results: {}".format(result_file))
    print("Results Obtained: {}".format(data))
    print("\nWrong Answers: {}".format(wrong_answers))

    return (correct_answers / float(len(result_file))) * 100

def save_results(results, filename):
    tmp_file = open(filename, 'w')
    for item in results:
        tmp_file.write(item + '\n')

    tmp_file.close()

def main():
    csv_data_test = get_csv_data('teste.csv')
    csv_data_train = get_csv_data('treinamento.csv')
    txt_result_data = get_result_data('rotulos-teste.txt')
    
    #Best Value
    k = 7
    #k = int(sys.argv[1])

    results = []
    for x in range(len(csv_data_test)):
        all_neighbors = get_near_neighbors(csv_data_test[x], csv_data_train, k)
        response = get_response(all_neighbors)
        results.append(response)

    corrects_answers_percentage = get_accuracy(txt_result_data, results)
    
    save_results(results, 'resultado.txt')
    
    print("Correct Awnsers Percentage: %.2f%%" %(corrects_answers_percentage))

main()