import hh_api
import super_job_api
import vacancy_analysis_math


def main():
    hh_stats = hh_api.analyze_vacancies()
    super_job_stats = super_job_api.main()

    print("HeadHunter Statistics:")
    vacancy_analysis_math.print_stats_table(hh_stats)
    print("\nSuperJob Statistics:")
    vacancy_analysis_math.print_stats_table(super_job_stats)


if __name__ == "__main__":
    main()
