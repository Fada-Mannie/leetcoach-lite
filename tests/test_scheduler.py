from leetcoach.scheduler import priority

def test_priority_orders_harder_first_at_same_box():
    assert priority(0, "hard") < priority(0, "medium") < priority(0, "easy")
