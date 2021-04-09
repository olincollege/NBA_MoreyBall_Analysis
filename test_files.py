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
    summary = round(float(summary_full['Minutes_Played']), 2)
    return True

def test_playoff_3P_stats():
    """
    This tests that 1. the playoff_3P_round function fetches
    the right data and 2. that the data in our playoffs csvs
    matches real data. We only test one year since all years'
    data is formatted the same and will be consistent with the
    results of this test.
    """
    assert playoff_round_3p(2019, True) == \
    {0: [.35725, .323125], 1: [0.38525, 0.346],\
         2: [0.397, 0.348], 3: [0.38, 0.37200000000000005],\
              4: [0.406, 0.34600000000000003]}

    assert playoff_round_3p(2018, False) == \
    {0: [0.307625, 0.361], 1: [0.34925, 0.36375], \
        2: [0.4295, 0.36950000000000005], 3: [0.379, 0.37200000000000005],\
            4: [0.33899999999999997, 0.391]}


def test_edge_case():
    """
    Tests ability to detect edge cases. Since all years' data is
    formatted the same, we will only test for one year.
    """
    assert list(edge_cases_metric("Field_Goals_3P").iloc[1,:]) == \
        ['2011', 1, 3]
    assert list(edge_cases_metric("Field_Goals_Attempted_3PA").iloc[3,:]) == \
        ['2013', 3, 7]
