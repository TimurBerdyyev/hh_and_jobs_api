import os
import requests
from dotenv import load_dotenv
from math_lib import print_stats_table


def predict_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    elif salary_from:
        return salary_from
    elif salary_to:
        return salary_to
    else:
        return 0

def fetch_vacancies_from_superJob(secret_key, language, town='Москва', keyword='программист', per_page=100):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {'X-Api-App-Id': secret_key}
    params = {'town': town, 'keyword': f'{keyword} {language}', 'page': 0, 'count': per_page}
    vacancy_results = []

    while True:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status() 
        vacancies_data = response.json()
        vacancies_data = vacancies_data.get('objects', [])  # Изменено на более описательное название
        if not vacancies_data:
            break 
        vacancy_results.extend(vacancies_data)
        params['page'] += 1 

    found_vacancies = vacancies_data.get('total', 0)
    return vacancy_results, found_vacancies


def main():
    load_dotenv()
    superJob_secret_key = os.getenv('SUPER_JOB_API')
    languages = ['Python', 'Java', 'JavaScript', 'C#', 'C++', 'Ruby', 'PHP', 'Swift', 'Go']
    stats = {}

    for language in languages:
        vacancies, found_vacancies = fetch_vacancies_from_superJob(superJob_secret_key, language)
        processed_vacancies = [predict_salary(vacancy['payment_from'], vacancy['payment_to']) for vacancy in vacancies]
        average_salary = int(sum(processed_vacancies) / len(processed_vacancies)) if processed_vacancies else None
        stats[language] = {
            'vacancies_found': found_vacancies,
            'vacancies_processed': len(processed_vacancies),
            'average_salary': average_salary
        }

    return stats


if __name__ == "__main__":
    stats = main()
    print_stats_table(stats)
