from terminaltables import AsciiTable


def print_stats_table(stats):
    vacancies_summary_table = [['Language', 'Vacancies Found', 'Vacancies Processed', 'Average Salary']]

    for language, vacancy_details in stats.items():
        vacancies_found = vacancy_details.get('vacancies_found', 0)
        vacancies_processed = vacancy_details.get('vacancies_processed', 0)
        average_salary = vacancy_details.get('average_salary', 'N/A')

        vacancies_summary_table.append([language, vacancies_found, vacancies_processed, average_salary])

    table = AsciiTable(vacancies_summary_table)
    print(table.table)


def calculate_expected_salary(salary_from, salary_to):
    if salary_from is not None and salary_to is not None:
        return (salary_from + salary_to) / 2
    elif salary_from is not None:
        return salary_from
    elif salary_to is not None:
        return salary_to
    else:
        return 0

