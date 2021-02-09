"""Test Insurance Model."""

from application.models.insurance import Insurance


def test_create_insurance(test_client):
    """
    GIVEN an insurance instance
    WHEN the create method is called
    THEN save instance to database
    """
    insurance = Insurance('Insurance Type', 100.00)

    count_before = Insurance.query.count()
    ret_insurance = insurance.create()
    count_after = Insurance.query.count()

    assert count_after == count_before + 1
    assert ret_insurance.name == 'Insurance Type'
    assert ret_insurance.monthly_price == 100.00


def test_find_insurance(test_client_with_db):
    """
    GIVEN an insurance type in the database
    WHEN the find_insurance method is called
    THEN return insurance found in the database
    """
    insurance = Insurance.find_insurance('Household Contents Insurance')

    assert insurance.name == 'Household Contents Insurance'
    assert insurance.monthly_price == 10.00


def test_find_insurance_none(test_client):
    """
    GIVEN an insurance type not in the database
    WHEN the find_insurance method is called
    THEN return None
    """
    insurance = Insurance.find_insurance('Household Contents Insurance')

    assert insurance is None


def test_get_recommendation_insurance(test_client_with_db):
    """
    GIVEN an occupation and quantity of children
    WHEN the get_recommendation method is called
    THEN return correct recommendations
    """
    insurance_list = Insurance.get_recommendation('employed', 0)

    assert 'Private' in insurance_list[0].name
    assert 'Household' in insurance_list[1].name

    insurance_list = Insurance.get_recommendation('self-employed', 3)

    assert 'Public' in insurance_list[0].name
    assert 'Legal' in insurance_list[1].name
    assert 'Life' in insurance_list[2].name

    insurance_list = Insurance.get_recommendation('student', 1)

    assert 'Expat' in insurance_list[0].name
    assert 'Life' in insurance_list[1].name
