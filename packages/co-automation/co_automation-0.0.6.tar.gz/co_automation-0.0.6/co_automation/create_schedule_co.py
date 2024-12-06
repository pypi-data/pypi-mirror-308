from get_sn_token import get_token
from create_sn_co import create_change_order
from get_sn_co_item import get_configuration_item
from risk_assessment import risk_assessment
from conflict_check import conflict_status_check, start_conflict_check
from update_status import cancel_change, move_status, change_status
from date_logic import dates_calculations

def create_schedule_co (SN_INSTANCE, sn_access_token, CO_ITEM, start_date, end_date, year_week,
                       data_center, environment_name, co_properties,
                       is_test_mode=False):

    week_days = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday",
        7: "Monday",
        8: "Tuesday",
        9: "Wednesday",
        10: "Thursday",
        11: "Friday",
        12: "Saturday",
        13: "Sunday"
    }

    # if day of the week was not passed in the job, default to Thursday.
    if days_of_week is None:
        days_of_week = [3]
    else:
        days_of_week = days_of_week.replace(" ",",")
        logging.warning(f"day_of_week:{days_of_week}")
        days_of_week = json.loads(days_of_week)

    # if this is a cron - default to a team member if not provided. For one time job, we make it mandatory from the Jenkins dashboard.
    if requested_by is None:
        requested_by = co_properties.default_requested_by;

    for day in days_of_week:
        logging.warning(f"For day :{day}")
        start_date, end_date, week_year = dates_calculations(day)
        sn_access_token = get_sn_token.get_token(SN_USER, SN_PASSWORD, SN_INSTANCE)

        if sn_access_token is not None:
            access_token = sn_access_token["result"]["access_token"]
            if access_token is not None:
                logging.warning(f"Target date {week_days[day]}, week #{week_year}, Start time: {start_date}, end time: {end_date}")
                # retrieve Configuration item environment specific
                CO_ITEM_T = get_configuration_item(SN_INSTANCE, access_token,configuration_item_name)
                configuration_item_id = (CO_ITEM_T["result"][0])["sys_id"]

                # create CO request
                co = create_sn_co.create_change_order(SN_INSTANCE, access_token, configuration_item_id, start_date, end_date, week_year, requested_by, data_center, environment_name, False)
                co_number = (co["result"][0])["Change ID"]
                current_datetime = f"{datetime.now():%m-%d-%Y %H:%M:%S}"
                logging.warning(f"{current_datetime} - {co_number} Scheduled for: {week_days[day]}, week #{week_year}, Start time: {start_date}, end time: {end_date}")

                # Risk Assessment
                co_ra = risk_assessment.risk_assessment(SN_INSTANCE, access_token, co_number)
                current_datetime = f"{datetime.now():%m-%d-%Y %H:%M:%S}"
                logging.warning(f"{current_datetime} - CO Risk Assessment: {co_ra}")

                # Start Conflict Check
                co_cc = conflict_check.start_conflict_check(SN_INSTANCE, access_token, co_number)
                current_datetime = f"{datetime.now():%m-%d-%Y %H:%M:%S}"
                logging.warning(f"{current_datetime} - CO Conflict check started to trigger conflict detection: {co_cc['result'][0]}")

                # Start waiting time (in seconds). As per SN instructions we should wait 5 minutes before calling the status check
                # Increase by 3 hours to allow operator in charge to update the ticket details
                sleep(5*60)
                current_datetime = f"{datetime.now():%m-%d-%Y %H:%M:%S}"
                logging.warning(f"{current_datetime} - Waiting time is over, checking status now")

                # Conflict Status Check
                co_csc = conflict_check.conflict_status_check(SN_INSTANCE, access_token, co_number)
                co_status = co_csc["result"]["status"]
                current_datetime = f"{datetime.now():%m-%d-%Y %H:%M:%S}"

                # Wait additional 3 hours, before updating status to asses. This will allow operator in charge to update the ticket details
                # sleep(3*60*60)
                if co_status=="Conflict":
                    logging.warning(f"{current_datetime} - Conflict identified, please review it before requesting approval")
                    # if conflict, update Change Exception Type
                    co_cs = update_status.change_status(SN_INSTANCE, access_token, co_number)
                    logging.warning(f"CO Change status result: {co_cs['result']}")
                else:
                    logging.warning(f"{current_datetime} - No conflict, proceed with move status")
                    co_cs = update_status.move_status(SN_INSTANCE, access_token, co_number)
                    logging.warning(f"CO Change status result: {co_cs['result']}")

                # to cancel a ticket
                    canceled = update_status.cancel_change(SN_INSTANCE, access_token, co_number)
                    logging.warning(f"CO Change canceled: {canceled}")