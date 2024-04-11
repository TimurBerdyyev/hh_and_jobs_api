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
        return None


def fetch_vacancies_from_superJob(secret_key, language, town='Москва', keyword='программист', per_page=100):
    url = 'https://api.superjob.ru/2.0/vacancies/'
    headers = {'X-Api-App-Id': secret_key}
    params = {'town': town, 'keyword': f'{keyword} {language}', 'page': 0, 'count': per_page}
    vacancies = []

    try:
        while True:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status() 
            data = response.json()
            items = data.get('objects', [])
            if not items:
                break 
            vacancies.extend(items)
            params['page'] += 1 
    except requests.exceptions.RequestException as e:
        print(f"Error fetching vacancies: {e}")
        return None

    return vacancies


def predict_average_salary(vacancies):
    processed_vacancies = [predict_salary(vacancy['payment_from'], vacancy['payment_to']) for vacancy in vacancies]
    processed_vacancies = [salary for salary in processed_vacancies if salary]

    return int(sum(processed_vacancies) / len(processed_vacancies)) if processed_vacancies else None


def main():
    superJob_secret_key = os.getenv('SUPER_JOB_API')
    languages = ['Python', 'Java', 'JavaScript', 'C#', 'C++', 'Ruby', 'PHP', 'Swift', 'Go']
    stats = {}

    for language in languages:
        vacancies = fetch_vacancies_from_superJob(superJob_secret_key, language)
        processed_vacancies = [predict_salary(vacancy['payment_from'], vacancy['payment_to']) for vacancy in vacancies]

        found_vacancies = len(vacancies)
        average_salary = predict_average_salary(vacancies)

        stats[language] = {
            'vacancies_found': found_vacancies,
            'vacancies_processed': len(processed_vacancies),
            'average_salary': average_salary
        }

    return stats


if __name__ == "__main__":
    load_dotenv()
    stats = main()
    print_stats_table(stats)
