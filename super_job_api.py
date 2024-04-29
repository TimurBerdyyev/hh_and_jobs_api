import os
import requests
from dotenv import load_dotenv
from vacancy_analysis_math import print_stats_table, calculate_expected_salary


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
        vacancies_json = response.json()
        jobs = vacancies_json.get('objects', []) 
        if not vacancies_json:
            break 
        vacancy_results.extend(job_list)
        params['page'] += 1 

    found_vacancies = vacancies_json.get('total', 0)
    return vacancy_results, found_vacancies


def analyze_superjob_vacancies():
    languages = ['Python', 'Java', 'JavaScript', 'C#', 'C++', 'Ruby', 'PHP', 'Swift', 'Go']
    stats = {}

    for language in languages:
        vacancies, found_vacancies = fetch_vacancies_from_superJob(superJob_secret_key, language)
        processed_vacancies = [vacancy['salary'] for vacancy in vacancies if vacancy.get('salary')]
        average_salary = int(sum(processed_vacancies) / len(processed_vacancies)) if processed_vacancies else None
        stats[language] = {
            'vacancies_found': found_vacancies,
            'vacancies_processed': len(processed_vacancies),
            'average_salary': average_salary
        }

    return stats


if __name__ == "__main__":
    load_dotenv()
    superJob_secret_key = os.getenv('SUPER_JOB_KEY')
    stats = analyze_superjob_vacancies()
    print_stats_table(stats)
