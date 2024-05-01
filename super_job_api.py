import os
import requests
from dotenv import load_dotenv
from vacancy_analysis_math import print_stats_table, calculate_expected_salary


def fetch_vacancies_from_superJob(secret_key, language, town='Москва', keyword='программист', per_page=100):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {'X-Api-App-Id': secret_key}
    params = {'town': town, 'keyword': f'{keyword} {language}', 'page': 0, 'count': per_page}
    fetched_vacancies = []
    vacancies = None

    while True:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        vacancies = response.json()

        jobs = vacancies.get('objects', [])
        if not jobs:
            break

        fetched_vacancies.extend(jobs)
        params['page'] += 1

    found_vacancies = vacancies.get('total', 0) if vacancies else 0
    return fetched_vacancies, found_vacancies


def analyze_superjob_vacancies(superJob_secret_key):
    languages = ['Python', 'Java', 'JavaScript', 'C#', 'C++', 'Ruby', 'PHP', 'Swift', 'Go']
    stats = {}

    for language in languages:
        vacancies, found_vacancies = fetch_vacancies_from_superJob(superJob_secret_key, language)
        processed_vacancies = [calculate_expected_salary(vacancy['payment_from'], vacancy['payment_to']) for vacancy in vacancies if 'payment_from' in vacancy or 'payment_to' in vacancy]
        average_salary = int(sum(processed_vacancies) / len(processed_vacancies)) if processed_vacancies else None
        stats[language] = {
            'vacancies_found': found_vacancies,
            'vacancies_processed': len(processed_vacancies),
            'average_salary': average_salary
        }

    return stats


if __name__ == "__main__":
    load_dotenv()
    superJob_secret_key = os.getenv('SUPERJOB_KEY')
    stats = analyze_superjob_vacancies(superJob_secret_key)
    print_stats_table(stats)
