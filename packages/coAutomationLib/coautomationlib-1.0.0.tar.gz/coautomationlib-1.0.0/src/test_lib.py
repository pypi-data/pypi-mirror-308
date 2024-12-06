import co-automation-lib as snow

co = create_change_order("adp-test", "test_token", "Salesforce Service_IAT", "11-11-2024", "11-12-2024", "10", "sudip.nath@adp.com",
                            "DC1", "IAT", "short desc", "desc", "urgent", "test_plan", "critical", "no_rollback", "test_plan", True)
print(co)