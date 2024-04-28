import requests
from math_lib import print_stats_table, calculate_expected_salary

MOSCOW_AREA_ID = 1
MAX_ITEMS = 2000


def fetch_programmer_vacancies(language):
    url = 'https://api.hh.ru/vacancies'
    per_page = min(50, MAX_ITEMS)
    params = {
        'text': f'Программист {language}',
        'area': MOSCOW_AREA_ID,
        'per_page': per_page
    }
    vacancies = []

    page = 0
    while page * per_page < MAX_ITEMS:
        params['page'] = page 
        response = requests.get(url, params=params)
        response.raise_for_status()
        requests_data = response.json()
        vacancies_data = requests_data.get('items', [])
        if not vacancies_data:
            break
        vacancies.extend(vacancies_data)
        page += 1

    total_vacancies_count = requests_data.get('found', 0)
    return vacancies, total_vacancies_count


def predict_average_salary(vacancies):
    average_salaries = []
    for vacancy in vacancies:
        salary = vacancy.get('salary', {'from': None, 'to': None})
        if salary and salary.get('currency') == 'RUR':
            salary_from = salary['from']
            salary_to = salary['to']
            average_salary = calculate_expected_salary(salary_from, salary_to)
            if average_salary:
                average_salaries.append(average_salary)

    if average_salaries:
        return int(sum(average_salaries) / len(average_salaries))
    else:
        return None


def analyze_vacancies():
    popular_languages = ['Python', 'Java', 'JavaScript', 'C#', 'C++', 'Ruby', 'PHP', 'Swift', 'Go']
    language_stats = {}

    for language in popular_languages:
        vacancies, total_vacancies_count = fetch_programmer_vacancies(language)
        average_salary = predict_average_salary(vacancies)
        language_stats[language] = {
            'vacancies_found': total_vacancies_count,
            'vacancies_processed': len(vacancies),
            'average_salary': average_salary
        }

    return language_stats


if __name__ == "__main__":
    stats = analyze_vacancies()
    print_stats_table(stats)
