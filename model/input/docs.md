{% docs user_id %}
The unique user identifier.
{% enddocs %}

{% docs anonymous_id %}
The unique session identifier from segment.
{% enddocs %}

{% docs doctor_id %}
The unique doctor identifier.
{% enddocs %}

{% docs consultation_id %}
The unique consultation identifier.
{% enddocs %}

{% docs treatment_id %}
The unique treatment identifier.
{% enddocs %}

{% docs quiz_application_id %}
The unique quiz application identifier.
{% enddocs %}

{% docs screening_quiz_application_id %}
The unique screening quiz application identifier.
{% enddocs %}

{% docs event_datetime %}
The timestamp (AEST) when the event recorded.
{% enddocs %}

{% docs problem_type %}
The condition identifier.
{% enddocs %}

{% docs trigger %}
The trigger for the event.
{% enddocs %}

{% docs consultation_sku %}
The prescribed sku for the treatment plan.
{% enddocs %}

{% docs consultation_min_completed_datetime %}
The date and time the consulation was first completed to a doctor.
{% enddocs %}

{% docs consultation_initial_completed_doctor_name %}
The name of the doctor that first completed the consultation.
{% enddocs %}

{% docs consultation_max_completed_datetime %}
The date and time the consulation was last completed to a doctor.
{% enddocs %}

{% docs consultation_last_completed_doctor_name %}
The name of the doctor that last completed the consultation.
{% enddocs %}

{% docs consultation_is_approved %}
A boolean describing whether the user was approved for treatment in the consultation.
{% enddocs %}

{% docs consultation_is_re_approved %}
A boolean describing whether the user was re-approved for same treatment they were on prior to the consultation.
{% enddocs %}

{% docs subscription_sk %}
This is the unique surragate key to indentify a user_id & problem_type combination.
{% enddocs %}

{% docs subscription_order_sk %}
This is the unique surragate key to indentify a subscription & order combination, used to check for duplicates.
{% enddocs %}

{% docs treatment_status %}
The current status of the treatment.
{% enddocs %}

{% docs scheduled_datetime %}
The date and time the order is expected to be paid, based on the job scheduler.
{% enddocs %}

{% docs calculated_order_datetime %}
The date and time the order is expected to be paid, based on the job scheduler and the product plan information.
{% enddocs %}

{% docs refills_remaining %}
The number of refills remaining prior to the order.
{% enddocs %}

{% docs rx_sku %}
The prescription sku of the order.
{% enddocs %}

{% docs consult_type %}
The type of consultation e.g. initial, follow up, review.
{% enddocs %}

{% docs product_name %}
The product name related to the SKU.
{% enddocs %}

{% docs consultation_min_order_datetime %}
The date & time of the first order after the consultation, where the order relates to the product prescribed in the consultation.
{% enddocs %}

{% docs consultation_order_conversion_flag %}
A 1 or 0 flag indicating whether the patient has ordered after the consultation. 1 = ordered, 0 = hasn't ordered.
{% enddocs %}

{% docs date_of_birth %}
The users date of birth.
{% enddocs %}

{% docs sex_at_birth %}
The users sex at birth.
{% enddocs %}

{% docs all_doc_msg_count %}
The total number of doctor messages sent in the consultation. This includes both automated and actual sent messages.
{% enddocs %}

{% docs doc_msg_count %}
The total number of actual doctor messages sent in the consultation. Actual meaning non automated messages.
{% enddocs %}

{% docs auto_doc_msg_count %}
The total number of automated doctor messages sent in the consultation.
{% enddocs %}

{% docs min_doc_msg_datetime %}
The date & time of the first actual doctor message sent in the consultation. Actual meaning non automated messages.
{% enddocs %}

{% docs min_auto_doc_msg_datetime %}
The date & time of the first automated doctor message sent in the consultation. 
{% enddocs %}

{% docs max_doc_msg_datetime %}
The date & time of the last actual doctor message sent in the consultation. Actual meaning non automated messages.
{% enddocs %}

{% docs max_auto_doc_msg_datetime %}
The date & time of the last automated doctor message sent in the consultation. 
{% enddocs %}

{% docs age_at_quiz_start %}
The users age at the start of the respective quiz. 
{% enddocs %}

{% docs age_at_consult_complete %}
The users age at the max completed date of the respective consultation.
{% enddocs %}

{% docs quiz_height %}
The users answer to the height quiz question.
{% enddocs %}

{% docs quiz_weight %}
The users answer to the weight quiz question.
{% enddocs %}

{% docs quiz_bmi %}
The calculated bmi from the patients height & weight quiz answers.
{% enddocs %}

{% docs quiz_postcode %}
The answer to the postcode quiz question.
{% enddocs %}

{% docs hdyhau_channels %}
The answer to the 'how did you hear about us?' quiz question.
{% enddocs %}

{% docs type2_diabetes_risk_score %}
The type 2 diabetes risk score when completing the quiz.
{% enddocs %}

{% docs type2_diabetes_risk_level %}
The type 2 diabetes risk level completing the quiz.
{% enddocs %}

{% docs order_refund_amount %}
The amount refunded for the order.
{% enddocs %}

{% docs order_max_refund_datetime %}
The most recent date and time of a refund processed for an order. The reason there can be more than 1 date for a refund, is if it was partially refunded more than once.
{% enddocs %}

{% docs order_min_refund_datetime %}
The first date and time of a refund processed for an order. The reason there can be more than 1 date for a refund, is if it was partially refunded more than once.
{% enddocs %}

{% docs consultation_refund_datetime %}
The date and time of the consultation refund. 
{% enddocs %}

{% docs consultation_refund_amount %}
The amount refunded for the consultation.
{% enddocs %}

{% docs min_response_datetime %}
The first response datetime within a consultation (includes auto messages). This is the least value between minimum consultation completed datetime, minimum doctor message datetime, and minimum auto doctor message datetime.
{% enddocs %}

{% docs min_doctor_response_datetime %}
The first response datetime within a consultation (excludes auto messages). This is the least value between minimum consultation completed datetime and minimum doctor message datetime.
{% enddocs %}

{% docs doctor_first_response_time_hours %}
The time in hours from the minimum doctor assigned datetime to the minimum doctor response datetime. This is the doctor's first response time in the consultation (excludes auto messages).
{% enddocs %}

{% docs first_response_time_hours %}
The time in hours from the minimum doctor assigned datetime to the minimum response datetime. This is the first response time in the consultation (includes auto messages).
{% enddocs %}

{% docs revenue_date_day %}
The day the revenue & refunds where processed. 
{% enddocs %}

{% docs revenue_date_day_by_paid_day %}
The day the order was processed. 
{% enddocs %}

{% docs sum_consult_revenue %}
The sum of the consultation revenue.
{% enddocs %}

{% docs sum_consult_refunded_amount %}
The sum of the consultation refunds.
{% enddocs %}

{% docs sum_rx_revenue %}
The sum of the prescription revenue.
{% enddocs %}

{% docs sum_otc_revenue %}
The sum of the shopfront products revenue.
{% enddocs %}

{% docs sum_order_revenue %}
The sum of the all the revenue in the order (i.e. rx + otc).
{% enddocs %}

{% docs sum_order_refunded_amount %}
The sum of all the refunded amouns for the orders.
{% enddocs %}

{% docs total_revenue %}
The sum of the consultation and order revenue. 
{% enddocs %}

{% docs total_refunded_amount %}
The sum of the consultation and order refunded amounts.
{% enddocs %}

{% docs total_revenue_minus_refunds %}
The total revenue minus refunds.
{% enddocs %}

{% docs true_initial_problem_type %}
The first problem type the user came to the brand for (OTC is included as a problem type).
{% enddocs %}

{% docs true_initial_cohort_datetime %}
The date and time for the first quiz or order for the user ever.
{% enddocs %}

{% docs reactivated_order_flag %}
A 1 or 0 flag indicating if the order was after the user was paused prior to the order.
{% enddocs %}

{% docs country_code %}
The ISO two-letter code that represents the country the order/consultation/event took place in.
{% enddocs %}

{% docs email_id %}
The unique identifier for an email sent to a user.
{% enddocs %}

{% docs psat_datetime %}
The datetime that the PSAT survey response was received.
{% enddocs %}

{% docs psat_doctor_name %}
The name of the doctor being referred to in the PSAT survey.
{% enddocs %}

{% docs psat_overall_satisfaction %}
The overall satisfaction level of the patient with the consultation (1 to 5).
{% enddocs %}

{% docs psat_extended_response %}
The qualitative comment left by the patient about the consultation.
{% enddocs %}

{% docs psat_doctor_quality %}
The quality score provided by the patient about the doctor (1 to 5).
{% enddocs %}