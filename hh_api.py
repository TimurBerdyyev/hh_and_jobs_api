import requests
from vacancy_analysis_math import print_stats_table, calculate_expected_salary

MOSCOW_AREA_ID = 1
PER_PAGE = 50


def fetch_programmer_vacancies(language):
    url = 'https://api.hh.ru/vacancies'
    params = {
        'text': f'Программист {language}',
        'area': MOSCOW_AREA_ID,
        'per_page': PER_PAGE
    }
    vacancies = []
    response = requests.get(url, params=params)
    response.raise_for_status()
    response_data = response.json()
    total_pages = response_data['pages']
    vacancies.extend(response_data.get('items', []))

    for page in range(1, total_pages):
        params['page'] = page
        response = requests.get(url, params=params)
        response.raise_for_status()
        response_data = response.json()
        vacancies.extend(response_data.get('items', []))

    total_vacancies_count = response_data.get('found', 0)
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
        vacancies_processed = sum(1 for vacancy in vacancies if vacancy.get('salary'))
        average_salary = predict_average_salary(vacancies)
        language_stats[language] = {
            'vacancies_found': total_vacancies_count,
            'vacancies_processed': vacancies_processed,
            'average_salary': average_salary
        }

    return language_stats


if __name__ == "__main__":
    stats = analyze_vacancies()
    print_stats_table(stats)
