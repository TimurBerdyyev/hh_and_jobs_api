import os
import requests
from dotenv import load_dotenv
from math_lib import print_stats_table, calculate_expected_salary


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


def fetch_vacancies_from_superJob(secret_key, language, town='Москва', keyword='программист', per_page=100):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {'X-Api-App-Id': secret_key}
    params = {'town': town, 'keyword': f'{keyword} {language}', 'page': 0, 'count': per_page}
    vacancy_results = []

    while True:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status() 
        vacancies_data = response.json()
        job_list = vacancies_data.get('objects', []) 
        if not vacancies_data:
            break 
        vacancy_results.extend(job_list)
        params['page'] += 1 

    found_vacancies = vacancies_data.get('total', 0)
    return vacancy_results, found_vacancies


def analyze_superjob_vacancies():
    superJob_secret_key = os.getenv('SUPER_JOB_API')
    
    languages = ['Python', 'Java', 'JavaScript', 'C#', 'C++', 'Ruby', 'PHP', 'Swift', 'Go']
    stats = {}

    for language in languages:
        vacancies, found_vacancies = fetch_vacancies_from_superJob(superJob_secret_key, language)
        processed_vacancies = [predict_average_salary(vacancy['payment_from'], vacancy['payment_to']) for vacancy in vacancies if vacancy.get('salary')]
        average_salary = int(sum(processed_vacancies) / len(processed_vacancies)) if processed_vacancies else None
        stats[language] = {
            'vacancies_found': found_vacancies,
            'vacancies_processed': len(processed_vacancies),
            'average_salary': average_salary
        }

    return stats


if __name__ == "__main__":
    load_dotenv()
    stats = analyze_superjob_vacancies()
    print_stats_table(stats)
