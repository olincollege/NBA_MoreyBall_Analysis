from data_analysis import (
    get_season_clean_csv,
    season_full_data,
    season_summary,
    edge_cases_metric,
    playoff_round_3p,
    YEARS_LIST
)

#2) check if season full data matches season_summary
#3) edge case verification


def test_empty():
    for years in YEARS_LIST:
        test_df = season_summary(years, False)
        assert test_df.isnull().values.any() == False

        test_df = season_summary(years, True)
        assert test_df.isnull().values.any() == False

        test_df = season_full_data(years, False)
        assert test_df.isnull().values.any() == False

        test_df = season_full_data(years, True)
        assert test_df.isnull().values.any() == False

def test_check_summary():
    full = season_full_data(2010, False)
    summary_full = season_summary(2010, False)
    full_avg = round(full['Minutes_Played'].mean(), 2)
    summary = round(summary_full['Minutes_Played'], 2)
    return True
