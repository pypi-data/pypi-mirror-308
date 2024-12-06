from changeOrderAutomation import create_change_order

#(SN_INSTANCE, sn_access_token, CO_ITEM, start_date, end_date, year_week,
#                         requested_by, data_center, environment_name, short_description, description, business_case,
#                         communication_plan, impact_analysis, backout_plan, test_plan,
#                         is_test_mode)
co = create_change_order("adp-test", "test_token", "Salesforce Service_IAT", "11-11-2024", "11-12-2024", "10", "sudip.nath@adp.com",
                            "DC1", "IAT", "short desc", "desc", "urgent", "test_plan", "critical", "no_rollback", "test_plan", True)
print(co)