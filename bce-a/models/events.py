from db import get_connection

def get_all_events():
    cnx = get_connection()
    cursor = cnx.cursor(dictionary=True)

    query = ("SELECT e.*, es.*, esi.* "
            "FROM events e "
            "JOIN event_specifics es "
            "ON e.event_id = es.event_id "
            "JOIN event_specific_imgs esi "
            "ON es.event_specific_id = esi.event_specific_id "
            "WHERE es.event_specific_start = ( "
            "SELECT MIN(es2.event_specific_start) "
            "FROM event_specifics es2 "
            "WHERE es2.event_id = e.event_id "
            ") "
            "ORDER BY es.event_specific_start;")    
  
    cursor.execute(query)

    events = cursor.fetchall()

    cursor.close()
    cnx.close()

    return events

def get_event_by_id(event_id):
    cnx = get_connection()
    cursor = cnx.cursor(dictionary=True)

    query = ("SELECT e.*, es.*, esi.*, v.* "
            "FROM events e "
            "JOIN event_specifics es ON e.event_id = es.event_id "
            "JOIN event_specific_imgs esi ON es.event_specific_id = esi.event_specific_id "
            "JOIN venues v ON v.venue_id = es.venue_id "
            "WHERE e.event_id = %s")
    
    values = (event_id,)
    
    cursor.execute(query, values)

    event = cursor.fetchall()

    cursor.close()
    cnx.close()

    return event

def get_events_by_date(from_date, to_date):
    cnx = get_connection()
    cursor = cnx.cursor(dictionary=True)

    query = ("SELECT e.*, es.*, esi.*, v.* "
            "FROM events e "
            "JOIN event_specifics es ON e.event_id = es.event_id "
            "JOIN event_specific_imgs esi ON es.event_specific_id = esi.event_specific_id "
            "JOIN venues v ON v.venue_id = es.venue_id "
            "WHERE es.event_specific_start >= %s "
            "AND es.event_specific_end <= %s")
    
    values = (from_date, to_date)
    
    cursor.execute(query, values)
    events = cursor.fetchall()

    cursor.close()
    cnx.close()

    return events

def get_events_by_category(category):
    cnx = get_connection()
    cursor = cnx.cursor(dictionary=True)

    query = ("SELECT e.*, es.*, esi.* "
            "FROM events e "
            "JOIN event_specifics es ON e.event_id = es.event_id "
            "JOIN event_specific_imgs esi ON es.event_specific_id = esi.event_specific_id "
            "JOIN events_categories ec ON ec.event_id = e.event_id "
            "WHERE category_id = %s")
    
    values = (category,)

    cursor.execute(query,values)
    events = cursor.fetchall()

    cursor.close()
    cnx.close()
    return events