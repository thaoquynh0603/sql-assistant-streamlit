from generate_query import model
from extract_data import database_client 

def clean(query):
    return query.content.replace("sql\n","").replace("```","")

def get_data():
    query = model()
    completed_flag = 0
    while completed_flag == 0:
        try:
            query.run()
            result = clean(query.response)
            print(result)
            db = database_client("query-assistant")
            data = db.query_data(result, csv_export=True)
            completed_flag = 1
        except:
            extra = str(input("More Instruction"))
            query.request.prompt += extra
    
    print(data)
    return data

def testing():
    db = database_client("query-assistant")
    query = """WITH UserEvents AS (
        SELECT
            user_id,
            created_at
        FROM
            `query-assistant.Public_Dataset.events`
        ), UserOrders AS (
        SELECT
            user_id,
            created_at
        FROM
            `query-assistant.Public_Dataset.orders`
        ), UserEventsAndOrders AS (
        SELECT
            ue.user_id,
            ue.created_at AS event_created_at,
            uo.created_at AS order_created_at
        FROM
            UserEvents AS ue
        LEFT JOIN
            UserOrders AS uo
        ON
            ue.user_id = uo.user_id
        )
        SELECT
        DATE_TRUNC(event_created_at, week) AS week_of_event,
        COUNT(DISTINCT user_id) AS total_users,
        COUNT(DISTINCT CASE WHEN order_created_at IS NOT NULL THEN user_id END) AS users_with_orders,
        ROUND(
            COUNT(DISTINCT CASE WHEN order_created_at IS NOT NULL THEN user_id END) / COUNT(DISTINCT user_id),
            2
        ) AS conversion_rate
        FROM
        UserEventsAndOrders
        GROUP BY
        week_of_event
        HAVING 
            COUNT(DISTINCT user_id) > 0
        ORDER BY
        week_of_event;
    """
    data = db.query_data(query, csv_export=True)
    print(data)
    return data
if __name__=='__main__':
    get_data()