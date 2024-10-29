from process import find_all_matching_records


def test_filter_campaigns():
    
    query = {
        "TenantId": "100010"
    }
    print(find_all_matching_records("shopifySetting", query))