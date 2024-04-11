import requests
from math_lib import print_stats_table


MOSCOW_AREA_ID = 1


def fetch_programmer_vacancies(language):
    url = 'https://api.hh.ru/vacancies'
    params = {
        'text': f'Программист {language}',
        'area': MOSCOW_AREA_ID,
        'per_page': 100
    }
    vacancies = []

    page = 0
    while True:
        params['page'] = page 
        response = requests.get(url, params=params)
        response.raise_for_status()
        vacancies_data = response.json()
        items = vacancies_data.get('items', [])
        if not items:
            break
        vacancies.extend(items)
        page += 1

    return vacancies


def predict_average_salary(vacancies):
    average_salaries = []
    for vacancy in vacancies:
        salary_data = vacancy.get('salary', {'from': None, 'to': None})
        if salary_data and salary_data.get('currency') == 'RUR':
            salary_from = salary_data['from']
            salary_to = salary_data['to']
            if salary_from and salary_to:
                average_salary = (salary_from + salary_to) / 2
            elif salary_from:
                average_salary = salary_from * 1.2
            elif salary_to:
                average_salary = salary_to * 0.8
            else:
                average_salary = None
        
            if average_salary is not None:
                average_salaries.append(average_salary)

    if average_salaries:
        return int(sum(average_salaries) / len(average_salaries))
    else:
        return None


def main():
    popular_languages = ['Python', 'Java', 'JavaScript', 'C#', 'C++', 'Ruby', 'PHP', 'Swift', 'Go']
    language_stats = {}

    for language in popular_languages:
        vacancies = fetch_programmer_vacancies(language)
        average_salary = predict_average_salary(vacancies)
        total_vacancies_count = len(vacancies)
        language_stats[language] = {
            'total_vacancies_count': total_vacancies_count,
            'vacancies_processed': total_vacancies_count,
            'average_salary': average_salary
        }

    return language_stats


if __name__ == "__main__":
    stats = main()
    print_stats_table(stats)