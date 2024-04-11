import hh_api
import super_job_api


def main():
    hh_stats = hh_api.main()
    super_job_stats = super_job_api.main()

    print("HeadHunter Statistics:")
    hh_api.print_stats_table(hh_stats)
    print("\nSuperJob Statistics:")
    super_job_api.print_stats_table(super_job_stats)


if __name__ == "__main__":
    main()
