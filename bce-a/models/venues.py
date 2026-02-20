from db import get_connection

def insert_venue(venue_name, venue_capacity, venue_postcode, venue_address, venue_img_paths, venue_img_alts):
    cnx = get_connection()
    cursor = cnx.cursor(dictionary=True)

    query = ("INSERT INTO venues (venue_name, venue_capacity, venue_postcode, venue_address)"
            "VALUES (%s, %s, %s, %s)")
    values = (venue_name, venue_capacity, venue_postcode, venue_address)
    cursor.execute(query, values)
    cnx.commit()

    venue_id = cursor.lastrowid

    if venue_img_paths:
        for i in range(len(venue_img_paths)):
            if venue_img_paths[i].strip():
                img_query = ("INSERT INTO venue_imgs (venue_img_path, venue_img_alt, venue_id)"
                            "VALUES (%s, %s, %s)")
                
                if i < len(venue_img_alts):
                    alt_text = venue_img_alts[i]
                else:
                    alt_text = None

                cursor.execute(img_query, (venue_img_paths[i], alt_text, venue_id))
                cnx.commit()

    cursor.close()
    cnx.close()

    return venue_id